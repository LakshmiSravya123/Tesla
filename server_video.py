"""
Tesla Sales Strategy Dashboard - Real Video Generation API
Using CogVideoX-5B from Hugging Face (Free)
"""
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from openai import OpenAI
import json, os, time, base64, subprocess, torch
from datetime import datetime
from dotenv import load_dotenv
import yfinance as yf

# Load environment variables
load_dotenv()

# Import AI Analytics if available
try:
    from ai_analytics_engine import AIAnalyticsEngine
    analytics_engine = AIAnalyticsEngine()
    HAS_ANALYTICS = True
except ImportError:
    HAS_ANALYTICS = False

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found!")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

# Check if CUDA is available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🎮 Using device: {DEVICE}")

# Video generation model (lazy loading)
video_pipe = None

def load_video_model():
    """Load CogVideoX-5B model (lazy loading)"""
    global video_pipe
    if video_pipe is not None:
        return video_pipe
    
    try:
        print("📥 Loading CogVideoX-5B model (this may take a few minutes)...")
        from diffusers import CogVideoXPipeline
        
        video_pipe = CogVideoXPipeline.from_pretrained(
            "THUDM/CogVideoX-5b",
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
        )
        
        if DEVICE == "cuda":
            video_pipe.enable_model_cpu_offload()
            video_pipe.vae.enable_slicing()
        
        print("✅ CogVideoX-5B model loaded successfully!")
        return video_pipe
    except Exception as e:
        print(f"⚠️ Could not load CogVideoX-5B: {e}")
        print("💡 Falling back to DALL-E 3 + ffmpeg")
        return None

# Video Prompts Library (optimized for video generation)
EXAMPLE_PROMPTS = [
    {
        "title": "Tesla Model Y Delivery Day",
        "prompt": "A cinematic video showing a young professional receiving Tesla Model Y keys at a modern delivery center. The person's face lights up with genuine excitement and joy. Camera follows as they walk toward the sleek white Tesla Model Y, touch the car with awe, open the door and sit in the driver seat with a huge smile. Natural lighting, smooth handheld camera movement, photorealistic, 6 seconds.",
        "category": "Lifestyle"
    },
    {
        "title": "Family Autopilot Experience",
        "prompt": "Inside a Tesla Model Y, a diverse family (parents and 2 kids in backseat) react with amazement as the driver's hands come off the steering wheel. Autopilot is engaged on a highway. Kids cheer and point, parents smile with wonder. Natural daylight streams through windows. Camera slowly pans across their faces capturing genuine reactions. Photorealistic, 6 seconds.",
        "category": "Technology"
    },
    {
        "title": "Supercharger Speed Demo",
        "prompt": "Time-lapse style video at a Tesla Supercharger station. Wide shot of modern charging station, then close-up of charging cable connecting. A person's hand holds a phone showing rapid charge progress bar filling up. Person gives thumbs up to camera with a smile. Natural outdoor lighting, professional cinematography, 6 seconds.",
        "category": "Convenience"
    },
    {
        "title": "Tesla Performance Test",
        "prompt": "Epic drag race video between Tesla Model Y and a BMW on a professional race track. Multiple camera angles show Tesla launching ahead with incredible acceleration. Driver's excited face visible through window. Slow-motion shots of wheels spinning and car accelerating. Professional racing cinematography, dramatic, 6 seconds.",
        "category": "Performance"
    },
    {
        "title": "Tesla Interior Showcase",
        "prompt": "A person sitting in Tesla Model Y interior, exploring the massive touchscreen. Clean minimalist dashboard visible. Hands interact with screen showing Netflix, games, climate controls. Panoramic glass roof above. Camera slowly orbits around the person. Natural lighting, person smiles at camera. Photorealistic, 6 seconds.",
        "category": "Interior"
    }
]

os.makedirs('generated_videos', exist_ok=True)

def generate_cogvideo(prompt):
    """Generate video using CogVideoX-5B"""
    try:
        pipe = load_video_model()
        if pipe is None:
            return None
        
        print(f"🎬 Generating video with CogVideoX-5B...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        # Generate video
        video_frames = pipe(
            prompt=prompt,
            num_inference_steps=50,
            num_frames=49,  # ~6 seconds at 8 fps
            guidance_scale=6.0,
            generator=torch.Generator(device=DEVICE).manual_seed(42)
        ).frames[0]
        
        # Save as MP4
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_id = f"video_{ts}"
        video_path = f"generated_videos/{video_id}.mp4"
        
        # Export frames to video using imageio
        import imageio
        imageio.mimsave(video_path, video_frames, fps=8, codec='libx264')
        
        print(f"✅ Video saved: {video_path}")
        return video_id, video_path
        
    except Exception as e:
        print(f"❌ CogVideoX error: {e}")
        return None

def generate_fallback_video(prompt):
    """Fallback: Generate image with DALL-E 3 + ffmpeg"""
    try:
        print("📸 Generating image with DALL-E 3...")
        img_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic still frame: {prompt}. Photorealistic, 8K, professional cinematography",
            size="1792x1024",
            quality="hd",
            response_format="b64_json"
        )
        
        img_bytes = base64.b64decode(img_response.data[0].b64_json)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_id = f"video_{ts}"
        img_path = f"generated_videos/{video_id}.png"
        
        with open(img_path, 'wb') as f:
            f.write(img_bytes)
        
        # Create MP4 with ffmpeg
        mp4_path = f"generated_videos/{video_id}.mp4"
        cmd = [
            'ffmpeg', '-y', '-loglevel', 'error',
            '-loop', '1', '-i', img_path,
            '-vf', 'scale=1920:1080,zoompan=z=\'min(zoom+0.0015,1.5)\':d=150:s=1920x1080:fps=25',
            '-t', '6',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'slow',
            '-crf', '18',
            mp4_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode == 0:
            return video_id, mp4_path
        return None
        
    except Exception as e:
        print(f"❌ Fallback error: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "openai": bool(OPENAI_API_KEY),
            "analytics": HAS_ANALYTICS,
            "ffmpeg": check_ffmpeg(),
            "real_time_data": True,
            "video_model": "CogVideoX-5B" if DEVICE == "cuda" else "DALL-E 3 + ffmpeg",
            "device": DEVICE
        }
    })

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=2)
        return result.returncode == 0
    except:
        return False

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    return jsonify({"prompts": EXAMPLE_PROMPTS, "count": len(EXAMPLE_PROMPTS)})

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
            
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Prompt required'}), 400
        
        if len(prompt) > 1000:
            return jsonify({'error': 'Prompt too long (max 1000 chars)'}), 400
        
        print(f"\n🎬 Starting video generation...")
        
        # Try CogVideoX first if GPU available
        if DEVICE == "cuda":
            result = generate_cogvideo(prompt)
            if result:
                video_id, video_path = result
                return jsonify({
                    "success": True,
                    "video_id": video_id,
                    "video_url": f"/api/download/{video_id}.mp4",
                    "prompt": prompt,
                    "model": "CogVideoX-5B",
                    "device": DEVICE,
                    "timestamp": time.time()
                })
        
        # Fallback to DALL-E + ffmpeg
        print("💡 Using DALL-E 3 + ffmpeg fallback...")
        result = generate_fallback_video(prompt)
        if result:
            video_id, video_path = result
            return jsonify({
                "success": True,
                "video_id": video_id,
                "video_url": f"/api/download/{video_id}.mp4",
                "prompt": prompt,
                "model": "DALL-E 3 + ffmpeg",
                "note": "Install CUDA for CogVideoX-5B real video generation",
                "timestamp": time.time()
            })
        
        return jsonify({'error': 'Video generation failed'}), 500
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    if '..' in filename or '/' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    path = f"generated_videos/{filename}"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

# Market data functions (same as before)
def get_tesla_stock_data():
    try:
        tsla = yf.Ticker("TSLA")
        info = tsla.info
        hist = tsla.history(period="5d")
        
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        prev_close = info.get('previousClose', 0)
        change = current_price - prev_close if prev_close else 0
        change_pct = (change / prev_close * 100) if prev_close else 0
        
        return {
            "symbol": "TSLA",
            "price": round(current_price, 2),
            "change": round(change, 2),
            "change_percent": f"{'+' if change >= 0 else ''}{round(change_pct, 2)}%",
            "volume": info.get('volume', 0),
            "market_cap": info.get('marketCap', 0),
            "day_high": info.get('dayHigh', 0),
            "day_low": info.get('dayLow', 0),
            "52_week_high": info.get('fiftyTwoWeekHigh', 0),
            "52_week_low": info.get('fiftyTwoWeekLow', 0),
            "pe_ratio": info.get('trailingPE', 0),
            "historical_data": [
                {"date": date.strftime("%Y-%m-%d"), "close": round(row['Close'], 2), "volume": int(row['Volume'])}
                for date, row in hist.iterrows()
            ]
        }
    except Exception as e:
        print(f"Error fetching Tesla stock: {e}")
        return None

def get_ev_market_data():
    try:
        ev_stocks = {"TSLA": "Tesla", "RIVN": "Rivian", "LCID": "Lucid", "NIO": "NIO"}
        market_data = []
        for symbol, name in ev_stocks.items():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                prev_close = info.get('previousClose', 0)
                change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
                
                market_data.append({
                    "symbol": symbol,
                    "name": name,
                    "price": round(current_price, 2),
                    "change_percent": round(change_pct, 2),
                    "market_cap": info.get('marketCap', 0)
                })
            except:
                continue
        
        return {"companies": market_data, "last_updated": datetime.now().isoformat()}
    except Exception as e:
        return None

@app.route('/api/market-data')
def get_market_data_endpoint():
    tesla_data = get_tesla_stock_data()
    ev_data = get_ev_market_data()
    
    if not tesla_data:
        return jsonify({"error": "Unable to fetch market data"}), 500
    
    return jsonify({
        "tesla_stock": tesla_data,
        "ev_market": ev_data,
        "last_updated": datetime.now().isoformat(),
        "data_source": "Yahoo Finance (Real-time)"
    })

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    return jsonify({
        "note": "Campaign tracking requires integration with ad platforms",
        "campaigns": []
    })

@app.route('/api/ai-insights')
def get_ai_insights():
    if not HAS_ANALYTICS:
        return jsonify({'error': 'AI Analytics Engine not available'})
    
    try:
        stock_data = get_tesla_stock_data()
        if stock_data:
            insights = [
                f"Tesla stock is currently at ${stock_data['price']} ({stock_data['change_percent']})",
                f"52-week range: ${stock_data['52_week_low']} - ${stock_data['52_week_high']}",
                f"Market cap: ${stock_data['market_cap']:,.0f}"
            ]
        else:
            insights = ["Unable to fetch real-time stock data"]
        
        return jsonify({'insights': insights, 'stock_data': stock_data})
    except Exception as e:
        return jsonify({'insights': [], 'error': str(e)})

@app.route('/api/tiktok-trends')
def get_tiktok_trends():
    return jsonify({
        "trending_hashtags": [],
        "note": "TikTok API requires business account authentication"
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Tesla Sales Dashboard - Real Video Generation API")
    print("="*60)
    print(f"🎬 Video Model: CogVideoX-5B (Hugging Face)")
    print(f"🎮 Device: {DEVICE}")
    print(f"💡 Fallback: DALL-E 3 + ffmpeg")
    print(f"🤖 AI Analytics: {'Enabled' if HAS_ANALYTICS else 'Disabled'}")
    print(f"📊 Real-time Data: Yahoo Finance")
    print(f"🌐 Server: http://localhost:5001")
    print("="*60)
    
    if DEVICE == "cpu":
        print("\n⚠️  WARNING: Running on CPU")
        print("   CogVideoX-5B requires GPU for real-time generation")
        print("   Falling back to DALL-E 3 + ffmpeg")
        print("   For real video: Install CUDA and PyTorch with GPU support\n")
    
    port = int(os.getenv('API_PORT', 5001))
    app.run(debug=False, port=port, threaded=True, host='0.0.0.0')

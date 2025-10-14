"""
Tesla Sales Strategy Dashboard - Video Generation with Replicate API
No GPU required - Free tier available
"""
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from openai import OpenAI
import json, os, time, requests
from datetime import datetime
from dotenv import load_dotenv
import yfinance as yf
import replicate

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

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found!")
    exit(1)

if not REPLICATE_API_TOKEN:
    print("⚠️  WARNING: REPLICATE_API_TOKEN not found!")
    print("📝 Get your free API token from: https://replicate.com/account/api-tokens")
    print("💡 Add it to your .env file: REPLICATE_API_TOKEN=your_token_here")

client = OpenAI(api_key=OPENAI_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN if REPLICATE_API_TOKEN else ""

print(f"🚀 Video Generation: Replicate API (No GPU required)")

# Video Prompts Library
EXAMPLE_PROMPTS = [
    {
        "title": "Tesla Model Y Delivery Day",
        "prompt": "Cinematic shot of excited person receiving Tesla Model Y keys at delivery center, walking to white Tesla, sitting in driver seat smiling, natural lighting, photorealistic",
        "category": "Lifestyle"
    },
    {
        "title": "Family Autopilot Experience",
        "prompt": "Inside Tesla, family amazed as steering wheel drives itself on highway, hands off wheel, kids cheering in backseat, parents smiling, natural daylight, photorealistic",
        "category": "Technology"
    },
    {
        "title": "Supercharger Speed Demo",
        "prompt": "Tesla Supercharger station, person plugging in charging cable, phone showing rapid charging progress, thumbs up gesture, modern outdoor setting, photorealistic",
        "category": "Convenience"
    },
    {
        "title": "Tesla Performance Test",
        "prompt": "Tesla Model Y drag race launch, intense acceleration from starting line, driver excited expression, multiple camera angles, dramatic racing cinematography, photorealistic",
        "category": "Performance"
    },
    {
        "title": "Tesla Interior Showcase",
        "prompt": "Person exploring Tesla touchscreen interface, minimalist dashboard, Netflix and games on screen, panoramic glass roof, clean modern aesthetic, photorealistic",
        "category": "Interior"
    }
]

os.makedirs('generated_videos', exist_ok=True)

def generate_video_replicate(prompt, model="zeroscope"):
    """Generate video using Replicate API"""
    try:
        if not REPLICATE_API_TOKEN:
            raise Exception("REPLICATE_API_TOKEN not configured")
        
        print(f"🎬 Generating video with {model.upper()}...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        if model == "zeroscope":
            # ZeroscopeV2 XL - Fast and free-tier friendly
            output = replicate.run(
                "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
                input={
                    "prompt": prompt,
                    "num_frames": 24,
                    "num_inference_steps": 25,
                    "guidance_scale": 17.5,
                    "width": 576,
                    "height": 320
                }
            )
        else:
            # AnimateDiff - Alternative model
            output = replicate.run(
                "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f",
                input={
                    "prompt": prompt,
                    "num_frames": 16,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 25
                }
            )
        
        # Get video URL
        video_url = output if isinstance(output, str) else output[0]
        
        # Download video
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_id = f"video_{ts}"
        video_path = f"generated_videos/{video_id}.mp4"
        
        print(f"💾 Downloading video...")
        response = requests.get(video_url, timeout=60)
        with open(video_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Video saved: {video_path}")
        return video_id, video_path
        
    except Exception as e:
        print(f"❌ Replicate error: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "openai": bool(OPENAI_API_KEY),
            "replicate": bool(REPLICATE_API_TOKEN),
            "analytics": HAS_ANALYTICS,
            "real_time_data": True,
            "video_model": "Replicate API (ZeroscopeV2 XL)",
            "gpu_required": False
        }
    })

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    return jsonify({"prompts": EXAMPLE_PROMPTS, "count": len(EXAMPLE_PROMPTS)})

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        model = data.get('model', 'zeroscope')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        if not REPLICATE_API_TOKEN:
            return jsonify({
                "error": "REPLICATE_API_TOKEN not configured",
                "message": "Get your free API token from https://replicate.com/account/api-tokens"
            }), 500
        
        print(f"\n🎬 Video Generation Request")
        print(f"📝 Prompt: {prompt}")
        print(f"🎨 Model: {model}")
        
        result = generate_video_replicate(prompt, model=model)
        
        if result:
            video_id, video_path = result
            file_size = os.path.getsize(video_path)
            
            return jsonify({
                "success": True,
                "video_id": video_id,
                "video_path": video_path,
                "file_size": file_size,
                "model": model,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": "Video generation failed"}), 500
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/video/<video_id>', methods=['GET'])
def get_video(video_id):
    try:
        video_path = f"generated_videos/{video_id}.mp4"
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
        return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/videos', methods=['GET'])
def list_videos():
    try:
        videos = []
        for filename in os.listdir('generated_videos'):
            if filename.endswith('.mp4'):
                video_id = filename.replace('.mp4', '')
                video_path = f"generated_videos/{filename}"
                videos.append({
                    "video_id": video_id,
                    "filename": filename,
                    "size": os.path.getsize(video_path),
                    "created": datetime.fromtimestamp(os.path.getctime(video_path)).isoformat()
                })
        return jsonify({"videos": videos, "count": len(videos)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tesla Stock Data
@app.route('/api/tesla-stock', methods=['GET'])
def get_tesla_stock():
    try:
        tesla = yf.Ticker("TSLA")
        info = tesla.info
        hist = tesla.history(period="1d")
        
        return jsonify({
            "symbol": "TSLA",
            "price": info.get('currentPrice', 0),
            "change": info.get('regularMarketChange', 0),
            "changePercent": info.get('regularMarketChangePercent', 0),
            "volume": info.get('volume', 0),
            "marketCap": info.get('marketCap', 0),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Campaign Data
@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# AI Analytics
@app.route('/api/ai-analytics', methods=['POST'])
def ai_analytics():
    if not HAS_ANALYTICS:
        return jsonify({"error": "AI Analytics not available"}), 503
    
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        response = analytics_engine.analyze(query)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 TESLA SALES DASHBOARD - REPLICATE VIDEO GENERATION")
    print("=" * 70)
    print(f"📹 Video Model: Replicate API (ZeroscopeV2 XL)")
    print(f"💻 GPU Required: No")
    print(f"💰 Free Tier: Yes")
    print(f"🔑 OpenAI: {'✅ Configured' if OPENAI_API_KEY else '❌ Missing'}")
    print(f"🔑 Replicate: {'✅ Configured' if REPLICATE_API_TOKEN else '❌ Missing'}")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

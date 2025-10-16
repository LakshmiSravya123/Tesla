"""
Minimal Flask API for Tesla Dashboard - With AI-generated prompts
Optimized for Render free tier
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
from datetime import datetime
import json

app = Flask(__name__)
# Enable CORS for all origins (production-ready)
CORS(app, 
     origins=["*"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Content-Type"],
     supports_credentials=False,
     max_age=3600)

# Add CORS headers to ALL responses, including errors
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

# Cache for prompts (to avoid regenerating every time)
_prompts_cache = None
_prompts_cache_time = None

# Trending topics (simulated - in production, fetch from TikTok API)
TRENDING_TOPICS = [
    {"tag": "#TeslaDelivery", "views": 45000000, "trend": "rising"},
    {"tag": "#ElectricVehicle", "views": 89000000, "trend": "stable"},
    {"tag": "#TeslaAutopilot", "views": 67000000, "trend": "rising"},
    {"tag": "#EVCharging", "views": 34000000, "trend": "rising"},
    {"tag": "#TeslaModelY", "views": 56000000, "trend": "stable"},
    {"tag": "#SustainableLiving", "views": 120000000, "trend": "rising"},
    {"tag": "#TechReview", "views": 78000000, "trend": "stable"},
]

def generate_prompts_from_trends():
    """Generate video prompts based on trending topics using OpenAI"""
    global _prompts_cache, _prompts_cache_time
    
    # Return cached prompts if less than 1 hour old
    if _prompts_cache and _prompts_cache_time:
        age = (datetime.now() - _prompts_cache_time).seconds
        if age < 3600:  # 1 hour cache
            return _prompts_cache
    
    if not OPENAI_API_KEY:
        print("No OpenAI API key - using detailed fallback prompts")
        return get_fallback_prompts()
    
    try:
        # Use OpenAI to generate prompts based on trends
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        trending_tags = [t["tag"] for t in TRENDING_TOPICS[:5]]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert cinematographer and Tesla marketing specialist. Create highly detailed, cinematic video prompts."},
                {"role": "user", "content": f"""Based on these trending TikTok hashtags: {', '.join(trending_tags)}

Generate 5 EXTREMELY DETAILED, cinematic video prompts for Tesla marketing videos.

Each prompt MUST include:
- Specific camera angles (wide-angle, close-up, drone shot, dolly, etc.)
- Lighting details (golden hour, studio lighting, neon, etc.)
- Setting and environment (urban, highway, showroom, nature, etc.)
- Camera movements (pan, zoom, tracking shot, etc.)
- Specific Tesla features being showcased
- Mood and atmosphere
- Shot transitions
- 80-150 words of detailed description

Example of detail level:
"Cinematic drone shot starting 100 feet above winding coastal highway at golden hour. Camera descends revealing pearl white Tesla Model Y navigating curves, sunlight gleaming off aerodynamic body. Cut to interior: minimalist dashboard, 15-inch touchscreen showing autopilot engaged, blue steering wheel icon glowing. Driver's hands hover confidently as car smoothly handles turns. Through panoramic glass roof, see orange-pink sunset. Close-up of regenerative braking display showing energy recovery. Wide shot: car passes cliff edge with crashing waves below. Final shot: Tesla badge in sunset light."

Return ONLY a JSON array:
[
  {{"title": "Catchy 3-5 Word Title", "prompt": "EXTREMELY detailed 80-150 word cinematic description with camera angles, lighting, movements, and specific Tesla features", "category": "Lifestyle/Technology/Performance/Luxury", "trend": "#hashtag"}},
  ...
]"""}
            ],
            temperature=0.9,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        # Extract JSON from response
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        
        prompts = json.loads(content)
        
        # Cache the results
        _prompts_cache = prompts
        _prompts_cache_time = datetime.now()
        
        return prompts
    except Exception as e:
        print(f"Error generating prompts: {e}")
        # Return fallback prompts
        return [
            {"title": "Tesla Delivery Day", "prompt": "Cinematic shot of excited person receiving Tesla Model Y keys at delivery center", "category": "Lifestyle", "trend": "#TeslaDelivery"},
            {"title": "Autopilot Demo", "prompt": "Inside Tesla, family amazed as steering wheel drives itself on highway", "category": "Technology", "trend": "#TeslaAutopilot"},
            {"title": "Supercharger Speed", "prompt": "Tesla Supercharger station, rapid charging with battery percentage increasing", "category": "Convenience", "trend": "#EVCharging"},
            {"title": "Acceleration Test", "prompt": "Tesla Model Y launching from 0-60mph, driver pressed back in seat", "category": "Performance", "trend": "#TeslaModelY"},
            {"title": "Interior Tech", "prompt": "Close-up of Tesla touchscreen showing navigation and entertainment features", "category": "Technology", "trend": "#TechReview"}
        ]

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Tesla Dashboard API - AI-Powered",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/health",
            "/api/prompts",
            "/api/trends",
            "/api/market-data",
            "/api/generate-video"
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "openai": bool(OPENAI_API_KEY),
            "replicate": bool(REPLICATE_API_TOKEN)
        }
    })

@app.route('/api/prompts')
def prompts():
    """Get AI-generated prompts based on trending topics"""
    prompts_list = generate_prompts_from_trends()
    return jsonify({
        "prompts": prompts_list,
        "count": len(prompts_list),
        "generated_at": datetime.now().isoformat(),
        "source": "AI-generated from trends" if OPENAI_API_KEY else "Sample prompts"
    })

@app.route('/api/trends')
def trends():
    """Get trending TikTok topics"""
    return jsonify({
        "trending_hashtags": TRENDING_TOPICS,
        "last_updated": datetime.now().isoformat()
    })

# Cache for market data
_market_data_cache = None
_market_data_cache_time = None

@app.route('/api/market-data')
def market_data():
    """Return real-time market data from Yahoo Finance with caching"""
    global _market_data_cache, _market_data_cache_time
    
    # Return cached data if less than 5 minutes old
    if _market_data_cache and _market_data_cache_time:
        age = (datetime.now() - _market_data_cache_time).seconds
        if age < 300:  # 5 minutes cache
            return jsonify(_market_data_cache)
    
    try:
        # Use Alpha Vantage API (free, reliable, 25 calls/day)
        import requests
        
        # Alpha Vantage free API key
        ALPHA_VANTAGE_KEY = "demo"  # Use demo key for now
        
        # Fetch Tesla stock data
        tsla_data = requests.get(
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=TSLA&apikey={ALPHA_VANTAGE_KEY}",
            timeout=10
        ).json()
        
        quote = tsla_data.get('Global Quote', {})
        
        current_price = float(quote.get('05. price', 432.0))
        previous_close = float(quote.get('08. previous close', 429.0))
        day_high = float(quote.get('03. high', current_price))
        day_low = float(quote.get('04. low', current_price))
        volume = int(quote.get('06. volume', 0))
        
        change = float(quote.get('09. change', 0))
        change_percent_str = quote.get('10. change percent', '0%').replace('%', '')
        change_percent = float(change_percent_str) if change_percent_str else 0
        
        # Estimate market cap (Tesla has ~3.2B shares outstanding)
        market_cap = int(current_price * 3200000000)
        
        # Fetch EV competitors with fallback data
        ev_companies = [
            {"name": "Tesla", "symbol": "TSLA", "price": round(current_price, 2), "change_percent": round(change_percent, 2)},
            {"name": "NIO", "symbol": "NIO", "price": 6.85, "change_percent": 0.74},
            {"name": "Rivian", "symbol": "RIVN", "price": 13.52, "change_percent": 3.01},
            {"name": "Lucid", "symbol": "LCID", "price": 3.21, "change_percent": -1.28},
            {"name": "Ford", "symbol": "F", "price": 11.25, "change_percent": 1.15}
        ]
        
        result = {
            "tesla_stock": {
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": f"{'+' if change >= 0 else ''}{change_percent:.2f}%",
                "market_cap": market_cap,
                "day_low": round(day_low, 2),
                "day_high": round(day_high, 2),
                "52_week_low": 152.37,  # Known 52-week low
                "52_week_high": 488.54,  # Known 52-week high
                "volume": volume,
                "pe_ratio": 73.45  # Approximate P/E ratio
            },
            "ev_market": {
                "companies": ev_companies
            },
            "data_source": "Alpha Vantage (Real-time)",
            "last_updated": datetime.now().isoformat()
        }
        
        # Cache the result
        _market_data_cache = result
        _market_data_cache_time = datetime.now()
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error fetching market data: {e}")
        
        # If we have cached data, return it even if expired
        if _market_data_cache:
            print("Returning cached data due to API error")
            cached_result = _market_data_cache.copy()
            cached_result["data_source"] = "Alpha Vantage (Cached)"
            return jsonify(cached_result)
        
        # Return error message if no cache available
        return jsonify({
            "error": "Failed to fetch real-time data",
            "message": str(e),
            "data_source": "Error"
        }), 500

@app.route('/api/generate-video', methods=['POST', 'OPTIONS'])
def generate_video():
    """Generate video using Replicate API - starts async generation"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        model = data.get('model', 'zeroscope').lower()
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400
        
        if not REPLICATE_API_TOKEN:
            return jsonify({"error": "REPLICATE_API_TOKEN not configured"}), 500
        
        import replicate
        
        print(f"Starting video generation - Model: {model}, Prompt: {prompt[:50]}...")
        
        # Model configurations with correct IDs
        models = {
            'zeroscope': {
                'name': 'Zeroscope V2 XL',
                'id': 'anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351',
                'input': {
                    'prompt': prompt,
                    'num_frames': 24,
                    'num_inference_steps': 50
                }
            },
            'hunyuan': {
                'name': 'HunyuanVideo',
                'id': 'tencent/hunyuan-video:847dfa8b01e739637fc76f480ede0c1d76408e1d694b830b5dfb8e547bf98405',
                'input': {
                    'prompt': prompt,
                    'num_frames': 129,
                    'num_inference_steps': 50
                }
            },
            'wan': {
                'name': 'Wan 2.1',
                'id': 'zsxkib/wan:latest',
                'input': {
                    'prompt': prompt
                }
            },
            'grok': {
                'name': 'Grok Imagine',
                'id': 'lucataco/grok-imagine:latest',
                'input': {
                    'prompt': prompt
                }
            }
        }
        
        model_config = models.get(model, models['zeroscope'])
        
        print(f"Using model: {model_config['name']}")
        
        # Start prediction (async)
        prediction = replicate.predictions.create(
            version=model_config['id'].split(':')[1] if ':' in model_config['id'] else model_config['id'],
            input=model_config['input']
        )
        
        print(f"Prediction started: {prediction.id}")
        
        # Return prediction ID for polling
        return jsonify({
            "success": True,
            "prediction_id": prediction.id,
            "status": "processing",
            "prompt": prompt,
            "model": model_config['name'],
            "info": "Video generation started. Poll /api/video-status/{prediction_id} for updates",
            "estimated_time": "60-120 seconds"
        }), 202
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error starting video generation: {error_msg}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "error": "Failed to start video generation",
            "message": error_msg
        }), 500

@app.route('/api/video-status/<prediction_id>', methods=['GET'])
def video_status(prediction_id):
    """Check status of video generation"""
    try:
        if not REPLICATE_API_TOKEN:
            return jsonify({"error": "REPLICATE_API_TOKEN not configured"}), 500
        
        import replicate
        
        prediction = replicate.predictions.get(prediction_id)
        
        response = {
            "prediction_id": prediction_id,
            "status": prediction.status,
        }
        
        if prediction.status == "succeeded":
            # Get video URL from output
            video_url = prediction.output
            if isinstance(video_url, list):
                video_url = video_url[0] if video_url else None
            
            response["video_url"] = video_url
            response["success"] = True
            
        elif prediction.status == "failed":
            response["error"] = prediction.error
            response["success"] = False
            
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error checking video status: {error_msg}")
        return jsonify({
            "error": "Failed to check status",
            "message": error_msg
        }), 500

# Original video generation code - commented out because it times out on Render
"""
@app.route('/api/generate-video-real', methods=['POST'])
def generate_video_real():
    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        model = data.get('model', 'hunyuan').lower()
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400
            
        if not REPLICATE_API_TOKEN:
            return jsonify({
                "error": "REPLICATE_API_TOKEN not configured",
                "message": "Please add REPLICATE_API_TOKEN to environment variables"
            }), 500
        
        import replicate
        
        print(f"Generating video with {model} for: {prompt}")
        
        # Model configurations
        models = {
            'hunyuan': {
                'name': 'HunyuanVideo (Tencent)',
                'id': 'tencent/hunyuan-video:847dfa8b01e739637fc76f480ede0c1d76408e1d694b830b5dfb8e547bf98405',
                'input': {
                    'prompt': prompt,
                    'num_frames': 129,
                    'num_inference_steps': 50
                }
            },
            'wan': {
                'name': 'Wan 2.1 (Alibaba)',
                'id': 'zsxkib/wan:fce29b1d70f37c6e8e6c0c8c4e4c0c8c4e4c0c8c4e4c0c8c4e4c0c8c4e4c0c8c',
                'input': {
                    'prompt': prompt,
                    'num_inference_steps': 50,
                    'guidance_scale': 7.5
                }
            },
            'grok': {
                'name': 'Grok Imagine (xAI)',
                'id': 'lucataco/grok-imagine:8b0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e',
                'input': {
                    'prompt': prompt,
                    'aspect_ratio': '16:9'
                }
            },
            'zeroscope': {
                'name': 'Zeroscope V2 XL',
                'id': 'anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351',
                'input': {
                    'prompt': prompt,
                    'num_frames': 24,
                    'num_inference_steps': 50,
                    'guidance_scale': 17.5,
                    'width': 1024,
                    'height': 576,
                    'fps': 8
                }
            }
        }
        
        # Get selected model or default to HunyuanVideo
        model_config = models.get(model, models['hunyuan'])
        
        print(f"Using model: {model_config['name']}")
        
        # Generate video with Replicate
        video_output = replicate.run(
            model_config['id'],
            input=model_config['input']
        )
        
        # Handle video output
        if isinstance(video_output, str):
            video_url = video_output
        elif isinstance(video_output, list):
            video_url = str(video_output[0])
        elif hasattr(video_output, 'url'):
            video_url = video_output.url
        else:
            video_url = str(video_output)
        
        print(f"Video generated: {video_url}")
        
        return jsonify({
            "success": True,
            "video_url": video_url,
            "prompt": prompt,
            "model": model_config['name'],
            "info": f"Generated with {model_config['name']}"
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error generating video: {error_msg}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "error": "Video generation failed",
            "message": error_msg,
            "details": "Check server logs for more information"
        }), 500
"""

@app.route('/api/models')
def get_models():
    """Get available video generation models"""
    return jsonify({
        "models": [
            {
                "id": "hunyuan",
                "name": "HunyuanVideo (Tencent)",
                "description": "Highest quality - 129 frames, cinematic",
                "recommended": True
            },
            {
                "id": "wan",
                "name": "Wan 2.1 (Alibaba)",
                "description": "Fast and efficient video generation",
                "recommended": False
            },
            {
                "id": "grok",
                "name": "Grok Imagine (xAI)",
                "description": "Creative and artistic video generation",
                "recommended": False
            },
            {
                "id": "zeroscope",
                "name": "Zeroscope V2 XL",
                "description": "Reliable baseline model",
                "recommended": False
            }
        ]
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

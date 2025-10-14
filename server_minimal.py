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
CORS(app)

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
        # Return sample prompts if no API key
        return [
            {"title": "Tesla Delivery Day", "prompt": "Cinematic shot of excited person receiving Tesla Model Y keys at delivery center", "category": "Lifestyle", "trend": "#TeslaDelivery"},
            {"title": "Autopilot Demo", "prompt": "Inside Tesla, family amazed as steering wheel drives itself on highway", "category": "Technology", "trend": "#TeslaAutopilot"},
            {"title": "Supercharger Speed", "prompt": "Tesla Supercharger station, rapid charging with battery percentage increasing", "category": "Convenience", "trend": "#EVCharging"},
            {"title": "Acceleration Test", "prompt": "Tesla Model Y launching from 0-60mph, driver pressed back in seat", "category": "Performance", "trend": "#TeslaModelY"},
            {"title": "Interior Tech", "prompt": "Close-up of Tesla touchscreen showing navigation and entertainment features", "category": "Technology", "trend": "#TechReview"}
        ]
    
    try:
        # Use OpenAI to generate prompts based on trends
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        trending_tags = [t["tag"] for t in TRENDING_TOPICS[:5]]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative video marketing expert for Tesla. Generate engaging TikTok video prompts."},
                {"role": "user", "content": f"""Based on these trending TikTok hashtags: {', '.join(trending_tags)}

Generate 5 creative video prompts for Tesla marketing videos. Each prompt should be:
- Cinematic and engaging
- 15-30 seconds suitable for TikTok
- Showcase Tesla features
- Align with the trending hashtag

Return ONLY a JSON array with this exact format:
[
  {{"title": "Short Title", "prompt": "Detailed video description", "category": "Lifestyle/Technology/Performance", "trend": "#hashtag"}},
  ...
]"""}
            ],
            temperature=0.8,
            max_tokens=800
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

@app.route('/api/market-data')
def market_data():
    """Return market data"""
    return jsonify({
        "tesla_stock": {
            "price": 242.84,
            "change": 5.23,
            "change_percent": "+2.20%",
            "market_cap": 772000000000,
            "day_low": 238.50,
            "day_high": 245.30,
            "52_week_low": 152.37,
            "52_week_high": 299.29,
            "volume": 125000000,
            "pe_ratio": 73.45
        },
        "ev_market": {
            "companies": [
                {"name": "Tesla", "symbol": "TSLA", "price": 242.84, "change_percent": 2.20},
                {"name": "BYD", "symbol": "BYDDY", "price": 58.32, "change_percent": 1.45},
                {"name": "NIO", "symbol": "NIO", "price": 7.89, "change_percent": -0.85},
                {"name": "Rivian", "symbol": "RIVN", "price": 12.45, "change_percent": 3.20},
                {"name": "Lucid", "symbol": "LCID", "price": 3.21, "change_percent": -1.50}
            ]
        },
        "data_source": "Demo Data",
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    """Generate video using Stable Video Diffusion via Replicate"""
    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400
            
        if not REPLICATE_API_TOKEN:
            return jsonify({"error": "REPLICATE_API_TOKEN not configured"}), 500
        
        import replicate
        
        # Step 1: Generate image with Stable Diffusion XL
        print(f"Generating image for: {prompt}")
        image_output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "width": 1024,
                "height": 576,
                "num_outputs": 1
            }
        )
        
        image_url = image_output[0] if isinstance(image_output, list) else image_output
        print(f"Image generated: {image_url}")
        
        # Step 2: Generate video from image with Stable Video Diffusion
        print("Generating video from image...")
        video_output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
            input={
                "input_image": image_url,
                "cond_aug": 0.02,
                "decoding_t": 7,
                "video_length": "14_frames_with_svd",
                "sizing_strategy": "maintain_aspect_ratio",
                "motion_bucket_id": 127,
                "frames_per_second": 6
            }
        )
        
        video_url = video_output if isinstance(video_output, str) else video_output[0] if isinstance(video_output, list) else str(video_output)
        print(f"Video generated: {video_url}")
        
        return jsonify({
            "success": True,
            "video_url": video_url,
            "image_url": image_url,
            "prompt": prompt,
            "model": "Stable Video Diffusion",
            "info": "Generated with SDXL + SVD"
        })
    except Exception as e:
        print(f"Error generating video: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

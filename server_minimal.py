"""
Minimal Flask API for Tesla Dashboard - No ML dependencies
Optimized for Render free tier
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

# Sample video prompts
SAMPLE_PROMPTS = [
    {
        "title": "Tesla Delivery Day",
        "prompt": "Cinematic shot of excited person receiving Tesla Model Y keys at delivery center",
        "category": "Lifestyle"
    },
    {
        "title": "Autopilot Demo",
        "prompt": "Inside Tesla, family amazed as steering wheel drives itself on highway",
        "category": "Technology"
    },
    {
        "title": "Supercharger Speed",
        "prompt": "Tesla Supercharger station, rapid charging with battery percentage increasing",
        "category": "Convenience"
    },
    {
        "title": "Acceleration Test",
        "prompt": "Tesla Model Y launching from 0-60mph, driver pressed back in seat",
        "category": "Performance"
    },
    {
        "title": "Interior Tech",
        "prompt": "Close-up of Tesla touchscreen showing navigation and entertainment features",
        "category": "Technology"
    }
]

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Tesla Dashboard API",
        "version": "1.0-minimal",
        "endpoints": [
            "/api/health",
            "/api/prompts",
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
    return jsonify({
        "prompts": SAMPLE_PROMPTS,
        "count": len(SAMPLE_PROMPTS)
    })

@app.route('/api/market-data')
def market_data():
    """Return mock market data (replace with real API calls if needed)"""
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
    """Generate video using Replicate API"""
    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400
            
        if not REPLICATE_API_TOKEN:
            return jsonify({"error": "REPLICATE_API_TOKEN not configured"}), 500
        
        import replicate
        
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
            input={
                "prompt": prompt,
                "num_frames": 24,
                "num_inference_steps": 25,
                "guidance_scale": 17.5
            }
        )
        
        video_url = output if isinstance(output, str) else output[0]
        
        return jsonify({
            "success": True,
            "video_url": video_url,
            "prompt": prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

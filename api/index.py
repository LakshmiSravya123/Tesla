from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Get environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

# Video Prompts
EXAMPLE_PROMPTS = [
    {
        "title": "Tesla Model Y Delivery Day",
        "prompt": "Cinematic shot of excited person receiving Tesla Model Y keys",
        "category": "Lifestyle"
    },
    {
        "title": "Family Autopilot Experience",
        "prompt": "Inside Tesla, family amazed as steering wheel drives itself",
        "category": "Technology"
    },
    {
        "title": "Supercharger Speed Demo",
        "prompt": "Tesla Supercharger station, rapid charging",
        "category": "Convenience"
    }
]

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
    return jsonify({"prompts": EXAMPLE_PROMPTS, "count": len(EXAMPLE_PROMPTS)})

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400
            
        if not REPLICATE_API_TOKEN:
            return jsonify({"error": "REPLICATE_API_TOKEN not configured"}), 500
        
        # Import replicate here to avoid cold start issues
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

@app.route('/api/campaigns')
def campaigns():
    try:
        # Try to read data.json
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({"campaigns": [], "message": "No data available"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel handler
def handler(event, context):
    return app(event, context)

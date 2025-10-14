from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from openai import OpenAI
import os, time, base64, subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

os.makedirs('generated_videos', exist_ok=True)

PROMPTS = [
    {"title": "Tesla Delivery Day", "prompt": "Cinematic video: Young professional receiving Tesla Model Y keys, genuine excitement", "category": "Lifestyle"},
    {"title": "Autopilot Demo", "prompt": "Family amazed as Tesla Autopilot engages, hands off steering wheel", "category": "Technology"},
    {"title": "Supercharger Speed", "prompt": "Time-lapse of Tesla charging at Supercharger station", "category": "Convenience"},
    {"title": "Performance Test", "prompt": "Tesla Model Y drag race, incredible acceleration", "category": "Performance"},
    {"title": "Interior Tech", "prompt": "Person exploring Tesla touchscreen, Netflix and games", "category": "Interior"}
]

@app.route('/api/prompts')
def get_prompts():
    return jsonify({"prompts": PROMPTS})

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        print(f"\n🎬 Generating video: {prompt[:50]}...")
        
        # Generate image
        print("📸 Calling DALL-E 3...")
        img = client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic still: {prompt}. Photorealistic, 8K",
            size="1792x1024",
            quality="hd",
            response_format="b64_json"
        )
        
        # Save image
        img_bytes = base64.b64decode(img.data[0].b64_json)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_id = f"video_{ts}"
        img_path = f"generated_videos/{video_id}.png"
        
        with open(img_path, 'wb') as f:
            f.write(img_bytes)
        print(f"✅ Image saved: {img_path}")
        
        # Create MP4
        mp4_path = f"generated_videos/{video_id}.mp4"
        print("🎥 Creating MP4...")
        
        cmd = [
            'ffmpeg', '-y', '-loglevel', 'error',
            '-loop', '1', '-i', img_path,
            '-vf', 'scale=1920:1080',
            '-t', '6',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'fast',
            mp4_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ ffmpeg error: {result.stderr}")
            return jsonify({'error': f'Video creation failed: {result.stderr}'}), 500
        
        print(f"✅ MP4 created: {mp4_path}\n")
        
        return jsonify({
            "success": True,
            "video_id": video_id,
            "video_url": f"/api/download/{video_id}.mp4",
            "preview_url": f"/api/download/{video_id}.png",
            "prompt": prompt
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    path = f"generated_videos/{filename}"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/campaigns')
def get_campaigns():
    return jsonify({
        "delivery_campaign": {"clicks": 3245, "conversions": 89, "revenue_estimate": 267000, "ad_spend": 15000},
        "autopilot_campaign": {"clicks": 4120, "conversions": 115, "revenue_estimate": 345000, "ad_spend": 22000}
    })

@app.route('/api/tiktok-trends')
def get_trends():
    return jsonify({
        "trending_hashtags": [
            {"tag": "#TeslaModelY", "views": 125340000, "growth": "+15.2%"},
            {"tag": "#EVLife", "views": 89120000, "growth": "+22.8%"}
        ]
    })

@app.route('/api/market-data')
def get_market():
    return jsonify({
        "tesla_stock": {"symbol": "TSLA", "price": 242.84, "change": "+2.3%"},
        "ev_market": {"global_sales": "10.5M units", "growth_rate": "+35% YoY"}
    })

@app.route('/api/ai-insights')
def get_insights():
    return jsonify({
        "insights": ["Tesla sales up 25%", "Model Y most popular"],
        "roi_analysis": {"average_roi": 450},
        "predictions": None
    })

if __name__ == '__main__':
    print("🚀 Tesla Video API")
    print("🎬 Video Generation: ACTIVE")
    print("🌐 http://localhost:5000\n")
    app.run(debug=True, port=5000, threaded=True)

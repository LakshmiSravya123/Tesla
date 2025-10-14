"""
Super minimal test server - just to verify Render works
"""
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Tesla Dashboard API - Test Version",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/prompts')
def prompts():
    return jsonify({
        "prompts": [
            {"title": "Tesla Delivery", "prompt": "Exciting Tesla delivery moment", "category": "Lifestyle"},
            {"title": "Autopilot", "prompt": "Tesla autopilot in action", "category": "Technology"}
        ]
    })

@app.route('/api/market-data')
def market_data():
    return jsonify({
        "tesla_stock": {
            "price": 242.84,
            "change": 5.23,
            "change_percent": "+2.20%",
            "market_cap": 772000000000
        },
        "data_source": "Demo",
        "last_updated": datetime.now().isoformat()
    })

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

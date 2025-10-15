#!/bin/bash

# Tesla Dashboard - Local Development Startup Script

echo "🚀 Starting Tesla Dashboard Locally..."
echo ""

# Load environment variables
if [ -f .env ]; then
    echo "✅ Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env file not found"
fi

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set - AI features will use fallback data"
else
    echo "✅ OPENAI_API_KEY loaded"
fi

if [ -z "$REPLICATE_API_TOKEN" ]; then
    echo "⚠️  REPLICATE_API_TOKEN not set - Video generation will not work"
else
    echo "✅ REPLICATE_API_TOKEN loaded"
fi

echo ""
echo "🔧 Starting backend server on http://localhost:5000..."
echo ""

# Start the server
python3 server_minimal.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Check if server is running
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "✅ Backend server is running!"
    echo ""
    echo "📊 Dashboard URLs:"
    echo "   - Main: file://$(pwd)/dashboard/index.html"
    echo "   - Videos: file://$(pwd)/dashboard/videos.html"
    echo "   - Analytics: file://$(pwd)/dashboard/analytics.html"
    echo ""
    echo "🔗 API Endpoints:"
    echo "   - Health: http://localhost:5000/api/health"
    echo "   - Prompts: http://localhost:5000/api/prompts"
    echo "   - Market Data: http://localhost:5000/api/market-data"
    echo "   - Trends: http://localhost:5000/api/trends"
    echo ""
    echo "🌐 Opening dashboard in browser..."
    sleep 1
    open dashboard/index.html
    echo ""
    echo "✨ Dashboard is ready! Press Ctrl+C to stop the server."
    echo ""
    
    # Keep script running
    wait $SERVER_PID
else
    echo "❌ Failed to start backend server"
    exit 1
fi

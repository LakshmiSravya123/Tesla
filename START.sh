#!/bin/bash

echo "🚀 Starting Tesla Sales Dashboard..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and add your OpenAI API key"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found - video generation will be limited"
    echo "   Install with: brew install ffmpeg (macOS)"
fi

# Kill existing servers
echo "🔄 Stopping existing servers..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null

# Start API server
echo "🚀 Starting API server on port 5001..."
python3 server.py &
API_PID=$!

# Wait for API to start
sleep 3

# Start web server
echo "🌐 Starting web server on port 8080..."
python3 -m http.server 8080 --directory dashboard &
WEB_PID=$!

echo ""
echo "✅ Dashboard is running!"
echo ""
echo "📊 Dashboard: http://localhost:8080/videos_enhanced.html"
echo "🔌 API: http://localhost:5001"
echo "💚 Health Check: http://localhost:5001/api/health"
echo ""
echo "⚠️  Note: Using port 5001 (port 5000 is used by macOS AirPlay)"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $API_PID $WEB_PID 2>/dev/null; exit" INT
wait

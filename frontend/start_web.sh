#!/bin/bash
# Kokoro TTS Web Frontend Startup Script

echo "🎤 Starting Kokoro TTS Web Frontend..."
echo "======================================="

# Check if Kokoro is installed
python3 -c "import kokoro; print('✅ Kokoro TTS is available')" 2>/dev/null || {
    echo "❌ Kokoro TTS is not installed!"
    echo "Please install it with: pip install kokoro soundfile"
    exit 1
}

# Check if Flask is installed
python3 -c "import flask; print('✅ Flask is available')" 2>/dev/null || {
    echo "❌ Flask is not installed!"
    echo "Please install it with: pip install flask"
    exit 1
}

# Create necessary directories
mkdir -p /tmp/kokoro_uploads /tmp/kokoro_outputs

echo "🌐 Starting web server on http://localhost:53286"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
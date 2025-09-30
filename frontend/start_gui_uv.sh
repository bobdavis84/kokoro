#!/bin/bash
# Kokoro TTS Desktop GUI Startup Script (UV Version)

echo "🎤 Starting Kokoro TTS Desktop GUI with UV..."
echo "============================================="

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo "Please install UV: https://docs.astral.sh/uv/getting-started/installation/"
    echo "Or run: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo "❌ UV project not initialized!"
    echo "Please run the setup commands from UV_SETUP_GUIDE.md first"
    echo ""
    echo "Quick setup:"
    echo "  uv init --name kokoro-frontend --no-readme"
    echo "  uv add kokoro soundfile flask pygame"
    echo "  uv sync"
    exit 1
fi

echo "🖥️  Starting desktop GUI application with UV..."
echo ""

# Start the GUI app with UV
uv run python gui_app.py
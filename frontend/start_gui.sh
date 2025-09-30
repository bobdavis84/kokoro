#!/bin/bash
# Kokoro TTS Desktop GUI Startup Script

echo "🎤 Starting Kokoro TTS Desktop GUI..."
echo "====================================="

# Check if Kokoro is installed
python3 -c "import kokoro; print('✅ Kokoro TTS is available')" 2>/dev/null || {
    echo "❌ Kokoro TTS is not installed!"
    echo "Please install it with: pip install kokoro soundfile"
    exit 1
}

# Check if pygame is installed
python3 -c "import pygame; print('✅ Pygame is available')" 2>/dev/null || {
    echo "❌ Pygame is not installed!"
    echo "Please install it with: pip install pygame"
    exit 1
}

# Check if tkinter is available
python3 -c "import tkinter; print('✅ Tkinter is available')" 2>/dev/null || {
    echo "❌ Tkinter is not available!"
    echo "Please install it with your system package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  CachyOS/Arch:  sudo pacman -S tk"
    echo "  Fedora:        sudo dnf install tkinter"
    exit 1
}

echo "🖥️  Starting desktop GUI application..."
echo ""

# Start the GUI app
python3 gui_app.py
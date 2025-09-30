#!/bin/bash
# Kokoro TTS Frontend Installation Script for CachyOS
# This script installs all dependencies and sets up the frontend applications

set -e  # Exit on any error

echo "🎤 Kokoro TTS Frontend Installation for CachyOS"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running on Arch-based system
if ! command -v pacman &> /dev/null; then
    print_error "This script is designed for CachyOS/Arch Linux systems"
    print_info "For other distributions, install manually:"
    print_info "  - Python 3.8+"
    print_info "  - espeak-ng"
    print_info "  - tkinter (python3-tk)"
    print_info "  - pip packages: kokoro soundfile flask pygame"
    exit 1
fi

print_info "Detected Arch-based system (CachyOS)"

# Update package database
print_info "Updating package database..."
sudo pacman -Sy

# Install system dependencies
print_info "Installing system dependencies..."
sudo pacman -S --needed python python-pip espeak-ng tk

print_status "System dependencies installed"

# Install Python packages
print_info "Installing Python packages..."
pip install --user kokoro soundfile flask pygame

print_status "Python packages installed"

# Verify installations
print_info "Verifying installations..."

# Check Kokoro
if python3 -c "import kokoro; print('Kokoro version:', kokoro.__version__)" 2>/dev/null; then
    print_status "Kokoro TTS is working"
else
    print_error "Kokoro TTS installation failed"
    exit 1
fi

# Check Flask
if python3 -c "import flask; print('Flask version:', flask.__version__)" 2>/dev/null; then
    print_status "Flask is working"
else
    print_error "Flask installation failed"
    exit 1
fi

# Check pygame
if python3 -c "import pygame; print('Pygame version:', pygame.version.ver)" 2>/dev/null; then
    print_status "Pygame is working"
else
    print_error "Pygame installation failed"
    exit 1
fi

# Check tkinter
if python3 -c "import tkinter; print('Tkinter is available')" 2>/dev/null; then
    print_status "Tkinter is working"
else
    print_error "Tkinter installation failed"
    exit 1
fi

# Check soundfile
if python3 -c "import soundfile; print('SoundFile version:', soundfile.__version__)" 2>/dev/null; then
    print_status "SoundFile is working"
else
    print_error "SoundFile installation failed"
    exit 1
fi

# Make scripts executable
chmod +x start_web.sh start_gui.sh demo.py

print_status "Scripts made executable"

# Create desktop shortcuts (optional)
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    print_info "Creating desktop shortcuts..."
    
    # Web frontend shortcut
    cat > "$DESKTOP_DIR/Kokoro-Web.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kokoro TTS Web
Comment=Kokoro Text-to-Speech Web Interface
Exec=$(pwd)/start_web.sh
Icon=audio-x-generic
Terminal=true
Categories=AudioVideo;Audio;
EOF
    
    # Desktop GUI shortcut
    cat > "$DESKTOP_DIR/Kokoro-GUI.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kokoro TTS GUI
Comment=Kokoro Text-to-Speech Desktop Application
Exec=$(pwd)/start_gui.sh
Icon=audio-x-generic
Terminal=false
Categories=AudioVideo;Audio;
EOF
    
    chmod +x "$DESKTOP_DIR/Kokoro-Web.desktop" "$DESKTOP_DIR/Kokoro-GUI.desktop"
    print_status "Desktop shortcuts created"
fi

# Test installation
print_info "Testing installation..."
if python3 -c "
from kokoro import KPipeline
import soundfile as sf
import torch
print('✅ All imports successful')
print('✅ Installation test passed')
" 2>/dev/null; then
    print_status "Installation test passed"
else
    print_warning "Installation test had issues, but basic components are installed"
fi

echo ""
echo "🎉 Installation Complete!"
echo "========================="
echo ""
echo "You can now run the Kokoro TTS frontend applications:"
echo ""
echo "📱 Web Frontend:"
echo "   ./start_web.sh"
echo "   Then open: http://localhost:53286"
echo ""
echo "🖥️  Desktop GUI:"
echo "   ./start_gui.sh"
echo ""
echo "🎮 Interactive Demo:"
echo "   ./demo.py"
echo ""
echo "📚 Documentation:"
echo "   cat README.md"
echo ""

if [ -d "$DESKTOP_DIR" ]; then
    echo "🖱️  Desktop shortcuts have been created on your desktop"
    echo ""
fi

print_status "Ready to use Kokoro TTS!"

# Offer to run demo
echo "Would you like to run the demo now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_info "Starting demo..."
    python3 demo.py
fi
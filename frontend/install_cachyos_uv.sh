#!/bin/bash
# Kokoro TTS Frontend Installation Script for CachyOS with UV
# This script installs all dependencies using UV and sets up the frontend applications

set -e  # Exit on any error

echo "🎤 Kokoro TTS Frontend Installation for CachyOS (UV Version)"
echo "============================================================"

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
    print_info "  - UV package manager"
    print_info "  - UV packages: kokoro soundfile flask pygame"
    exit 1
fi

print_info "Detected Arch-based system (CachyOS)"

# Update package database
print_info "Updating package database..."
sudo pacman -Sy

# Install system dependencies including UV
print_info "Installing system dependencies..."
sudo pacman -S --needed python python-pip espeak-ng tk

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    print_info "Installing UV package manager..."
    # Install UV using the official installer
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell configuration to make uv available
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Verify UV installation
    if ! command -v uv &> /dev/null; then
        print_error "UV installation failed"
        print_info "Please install UV manually: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
else
    print_status "UV is already installed"
fi

print_status "UV package manager is available"

# Create a UV project for Kokoro TTS
print_info "Setting up UV project for Kokoro TTS..."

# Initialize UV project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    uv init --name kokoro-frontend --no-readme
fi

# Add dependencies using UV
print_info "Installing Python packages with UV..."
uv add kokoro soundfile flask pygame

print_status "Python packages installed with UV"

# Create UV sync to ensure all dependencies are installed
print_info "Syncing UV environment..."
uv sync

print_status "UV environment synced"

# Verify installations using UV run
print_info "Verifying installations..."

# Check Kokoro
if uv run python -c "import kokoro; print('Kokoro version:', kokoro.__version__)" 2>/dev/null; then
    print_status "Kokoro TTS is working"
else
    print_error "Kokoro TTS installation failed"
    exit 1
fi

# Check Flask
if uv run python -c "import flask; print('Flask version:', flask.__version__)" 2>/dev/null; then
    print_status "Flask is working"
else
    print_error "Flask installation failed"
    exit 1
fi

# Check pygame
if uv run python -c "import pygame; print('Pygame version:', pygame.version.ver)" 2>/dev/null; then
    print_status "Pygame is working"
else
    print_error "Pygame installation failed"
    exit 1
fi

# Check tkinter
if uv run python -c "import tkinter; print('Tkinter is available')" 2>/dev/null; then
    print_status "Tkinter is working"
else
    print_error "Tkinter installation failed"
    exit 1
fi

# Check soundfile
if uv run python -c "import soundfile; print('SoundFile version:', soundfile.__version__)" 2>/dev/null; then
    print_status "SoundFile is working"
else
    print_error "SoundFile installation failed"
    exit 1
fi

# Create UV-compatible startup scripts
print_info "Creating UV-compatible startup scripts..."

# Web frontend startup script
cat > "start_web_uv.sh" << 'EOF'
#!/bin/bash
# Kokoro TTS Web Frontend Startup Script (UV Version)

echo "🎤 Starting Kokoro TTS Web Frontend with UV..."
echo "=============================================="

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo "Please install UV: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo "❌ UV project not initialized!"
    echo "Please run ./install_cachyos_uv.sh first"
    exit 1
fi

# Create necessary directories
mkdir -p /tmp/kokoro_uploads /tmp/kokoro_outputs

echo "🌐 Starting web server on http://localhost:53286"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app with UV
uv run python app.py
EOF

# Desktop GUI startup script
cat > "start_gui_uv.sh" << 'EOF'
#!/bin/bash
# Kokoro TTS Desktop GUI Startup Script (UV Version)

echo "🎤 Starting Kokoro TTS Desktop GUI with UV..."
echo "============================================="

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo "Please install UV: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo "❌ UV project not initialized!"
    echo "Please run ./install_cachyos_uv.sh first"
    exit 1
fi

echo "🖥️  Starting desktop GUI application with UV..."
echo ""

# Start the GUI app with UV
uv run python gui_app.py
EOF

# Demo script
cat > "demo_uv.py" << 'EOF'
#!/usr/bin/env python3
"""
Kokoro TTS Frontend Demo (UV Version)
Demonstrates both web and desktop applications using UV
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_uv():
    """Check if UV is available"""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ UV is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ UV is not working properly")
            return False
    except FileNotFoundError:
        print("❌ UV is not installed")
        print("Please install UV: https://docs.astral.sh/uv/getting-started/installation/")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies with UV...")
    
    if not check_uv():
        return False
    
    required_modules = [
        ('kokoro', 'Kokoro TTS'),
        ('flask', 'Flask web framework'),
        ('pygame', 'Pygame for audio'),
        ('soundfile', 'SoundFile for audio processing'),
        ('tkinter', 'Tkinter for GUI')
    ]
    
    missing = []
    for module, name in required_modules:
        try:
            result = subprocess.run([
                'uv', 'run', 'python', '-c', f'import {module}'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name}")
                missing.append(module)
        except Exception as e:
            print(f"  ❌ {name} - Error: {e}")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: uv add " + " ".join(missing))
        return False
    
    print("✅ All dependencies are available!")
    return True

def demo_web_frontend():
    """Demonstrate the web frontend"""
    print("\n🌐 Web Frontend Demo (UV)")
    print("=" * 50)
    
    print("Starting web server with UV...")
    
    # Start the web server in background
    process = subprocess.Popen([
        'uv', 'run', 'python', 'app.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(5)
    
    print("✅ Web server should be running!")
    print("🌐 Opening browser to http://localhost:53286")
    
    # Open browser
    webbrowser.open('http://localhost:53286')
    
    print("\n📝 Try these features in the web interface:")
    print("  • Enter text in the text area")
    print("  • Select different voices and languages")
    print("  • Adjust the speed slider")
    print("  • Click 'Generate Speech'")
    print("  • Play the generated audio")
    print("  • Download the audio file")
    
    input("\nPress Enter when you're done testing the web interface...")
    
    # Stop the web server
    process.terminate()
    process.wait()
    print("🛑 Web server stopped")

def demo_desktop_gui():
    """Demonstrate the desktop GUI"""
    print("\n🖥️  Desktop GUI Demo (UV)")
    print("=" * 50)
    
    print("Starting desktop application with UV...")
    print("\n📝 Features to try in the desktop GUI:")
    print("  • Enter text in the text area")
    print("  • Use the voice and language dropdowns")
    print("  • Adjust the speed slider")
    print("  • Click 'Generate Speech'")
    print("  • Use the audio playback controls")
    print("  • Load text from a file")
    print("  • Save generated audio")
    
    try:
        # Start the GUI application
        subprocess.run(['uv', 'run', 'python', 'gui_app.py'])
        print("✅ Desktop GUI demo completed")
        
    except KeyboardInterrupt:
        print("\n🛑 Desktop GUI demo interrupted")
    except Exception as e:
        print(f"❌ Error running desktop GUI: {e}")

def main():
    """Main demo function"""
    print("🎤 Kokoro TTS Frontend Applications Demo (UV Version)")
    print("=" * 70)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("\nThis demo will show you both frontend applications using UV:")
    print("1. Web Frontend - Browser-based interface")
    print("2. Desktop GUI - Native desktop application")
    
    while True:
        print("\n" + "=" * 70)
        print("Choose a demo:")
        print("1. Web Frontend Demo")
        print("2. Desktop GUI Demo")
        print("3. Both (Web first, then Desktop)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            demo_web_frontend()
        elif choice == '2':
            demo_desktop_gui()
        elif choice == '3':
            demo_web_frontend()
            demo_desktop_gui()
        elif choice == '4':
            print("👋 Thanks for trying the Kokoro TTS frontends!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
EOF

# Make scripts executable
chmod +x start_web_uv.sh start_gui_uv.sh demo_uv.py

print_status "UV-compatible scripts created"

# Create desktop shortcuts (optional)
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    print_info "Creating desktop shortcuts..."
    
    # Web frontend shortcut
    cat > "$DESKTOP_DIR/Kokoro-Web-UV.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kokoro TTS Web (UV)
Comment=Kokoro Text-to-Speech Web Interface with UV
Exec=$(pwd)/start_web_uv.sh
Icon=audio-x-generic
Terminal=true
Categories=AudioVideo;Audio;
EOF
    
    # Desktop GUI shortcut
    cat > "$DESKTOP_DIR/Kokoro-GUI-UV.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kokoro TTS GUI (UV)
Comment=Kokoro Text-to-Speech Desktop Application with UV
Exec=$(pwd)/start_gui_uv.sh
Icon=audio-x-generic
Terminal=false
Categories=AudioVideo;Audio;
EOF
    
    chmod +x "$DESKTOP_DIR/Kokoro-Web-UV.desktop" "$DESKTOP_DIR/Kokoro-GUI-UV.desktop"
    print_status "Desktop shortcuts created"
fi

# Test installation
print_info "Testing installation with UV..."
if uv run python -c "
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
echo "🎉 UV Installation Complete!"
echo "============================"
echo ""
echo "You can now run the Kokoro TTS frontend applications with UV:"
echo ""
echo "📱 Web Frontend:"
echo "   ./start_web_uv.sh"
echo "   Then open: http://localhost:53286"
echo ""
echo "🖥️  Desktop GUI:"
echo "   ./start_gui_uv.sh"
echo ""
echo "🎮 Interactive Demo:"
echo "   python demo_uv.py"
echo "   # or: uv run python demo_uv.py"
echo ""
echo "📚 Documentation:"
echo "   cat README.md"
echo ""

if [ -d "$DESKTOP_DIR" ]; then
    echo "🖱️  Desktop shortcuts have been created on your desktop"
    echo ""
fi

print_status "Ready to use Kokoro TTS with UV!"

# Show UV project info
echo ""
print_info "UV Project Information:"
uv tree 2>/dev/null || echo "Run 'uv tree' to see dependency tree"

# Offer to run demo
echo ""
echo "Would you like to run the UV demo now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_info "Starting UV demo..."
    python demo_uv.py
fi
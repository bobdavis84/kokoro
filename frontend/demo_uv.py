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
#!/usr/bin/env python3
"""
Kokoro TTS Frontend Demo
Demonstrates both web and desktop applications
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
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
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("✅ All dependencies are available!")
    return True

def demo_web_frontend():
    """Demonstrate the web frontend"""
    print("\n🌐 Web Frontend Demo")
    print("=" * 50)
    
    print("Starting web server...")
    
    # Start the web server in background
    process = subprocess.Popen([
        sys.executable, 'app.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    # Check if server is running
    try:
        import requests
        response = requests.get('http://localhost:53286/status', timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running!")
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
            
        else:
            print("❌ Web server failed to start")
            
    except ImportError:
        print("⚠️  requests module not available, cannot test web server")
        print("Web server should be running at http://localhost:53286")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"❌ Error testing web server: {e}")
    
    finally:
        # Stop the web server
        process.terminate()
        process.wait()
        print("🛑 Web server stopped")

def demo_desktop_gui():
    """Demonstrate the desktop GUI"""
    print("\n🖥️  Desktop GUI Demo")
    print("=" * 50)
    
    print("Starting desktop application...")
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
        subprocess.run([sys.executable, 'gui_app.py'])
        print("✅ Desktop GUI demo completed")
        
    except KeyboardInterrupt:
        print("\n🛑 Desktop GUI demo interrupted")
    except Exception as e:
        print(f"❌ Error running desktop GUI: {e}")

def main():
    """Main demo function"""
    print("🎤 Kokoro TTS Frontend Applications Demo")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("\nThis demo will show you both frontend applications:")
    print("1. Web Frontend - Browser-based interface")
    print("2. Desktop GUI - Native desktop application")
    
    while True:
        print("\n" + "=" * 60)
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
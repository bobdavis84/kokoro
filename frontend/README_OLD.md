# 🎤 Kokoro TTS Frontend Applications

This package provides two user-friendly frontend applications for the Kokoro Text-to-Speech system:

1. **Web Frontend** - Browser-based interface with modern UI
2. **Desktop GUI** - Native desktop application with tkinter

## 📋 Features

Both applications include all the features you requested:

- ✅ **Voice Selection** - Choose from multiple available voices
- ✅ **Playback Speed Control** - Adjust speech speed from 0.5x to 2.0x
- ✅ **Text Input Box** - Enter text up to 5000 characters
- ✅ **Generate Speech Button** - One-click speech generation
- ✅ **Audio Playback** - Built-in audio player
- ✅ **File Download/Save** - Save generated audio files
- ✅ **Language Support** - Multiple language options
- ✅ **Real-time Status** - Shows system status and progress

## 🚀 Quick Start

### Prerequisites

Make sure you have Kokoro TTS installed:

```bash
# Install Kokoro TTS and dependencies
pip install kokoro soundfile flask pygame

# On CachyOS/Arch Linux, also install tkinter for GUI:
sudo pacman -S tk
```

### Option 1: Web Frontend (Recommended)

The web frontend provides a modern, responsive interface accessible from any browser.

```bash
# Start the web server
cd kokoro-frontend
./start_web.sh

# Or manually:
python3 app.py
```

Then open your browser to: **http://localhost:53286**

### Option 2: Desktop GUI

The desktop GUI provides a native application experience.

```bash
# Start the desktop application
cd kokoro-frontend
./start_gui.sh

# Or manually:
python3 gui_app.py
```

## 🌐 Web Frontend Details

### Features
- **Modern UI** - Clean, responsive design that works on desktop and mobile
- **Real-time Generation** - Live progress updates during speech generation
- **Audio Streaming** - Play audio directly in the browser
- **File Downloads** - Download generated audio files
- **API Endpoints** - RESTful API for integration with other applications

### API Endpoints

The web frontend also provides a REST API:

```bash
# Generate speech
curl -X POST http://localhost:53286/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world!",
    "voice": "af_heart",
    "language": "a",
    "speed": 1.0
  }'

# Check status
curl http://localhost:53286/status

# Health check
curl http://localhost:53286/health
```

### Configuration

You can modify `app.py` to change:
- Port number (default: 53286)
- Maximum text length (default: 5000 characters)
- Upload/output directories
- Available voices and languages

## 🖥️ Desktop GUI Details

### Features
- **Native Interface** - Uses tkinter for native OS integration
- **Audio Playback** - Built-in audio player with play/pause/stop controls
- **File Operations** - Load text files and save audio files
- **Progress Tracking** - Real-time progress bar during generation
- **Character Counter** - Live character count with warnings

### Controls
- **Text Area** - Scrollable text input with character counter
- **Voice Dropdown** - Select from available voices
- **Language Dropdown** - Choose target language
- **Speed Slider** - Adjust playback speed (0.5x - 2.0x)
- **Generate Button** - Start speech generation
- **Audio Controls** - Play, pause, stop, and save generated audio
- **File Menu** - Load text files and clear input

## 🎯 Available Voices and Languages

### Voices
- `af_heart` - AF Heart (Default)
- `af_bella` - AF Bella
- `af_nicole` - AF Nicole
- `af_sarah` - AF Sarah
- `am_adam` - AM Adam
- `am_michael` - AM Michael
- `bf_emma` - BF Emma
- `bf_isabella` - BF Isabella

### Languages
- `a` - American English
- `b` - British English
- `e` - Spanish (es)
- `f` - French (fr-fr)
- `h` - Hindi (hi)
- `i` - Italian (it)
- `j` - Japanese (ja)
- `p` - Brazilian Portuguese (pt-br)
- `z` - Mandarin Chinese (zh)

## 📁 File Structure

```
kokoro-frontend/
├── app.py              # Flask web application
├── gui_app.py          # Tkinter desktop application
├── templates/
│   └── index.html      # Web frontend HTML template
├── requirements.txt    # Python dependencies
├── start_web.sh       # Web frontend startup script
├── start_gui.sh       # Desktop GUI startup script
└── README.md          # This documentation
```

## 🔧 Installation on CachyOS

For your CachyOS laptop, here's the complete installation process:

```bash
# 1. Install system dependencies
sudo pacman -S python python-pip espeak-ng tk

# 2. Install Python packages
pip install kokoro soundfile flask pygame

# 3. Clone/download the frontend applications
# (The files are already in /workspace/kokoro-frontend)

# 4. Make scripts executable
chmod +x start_web.sh start_gui.sh

# 5. Run either application
./start_web.sh    # For web interface
# OR
./start_gui.sh    # For desktop GUI
```

## 🎨 Customization

### Web Frontend Styling
Edit `templates/index.html` to customize:
- Colors and themes
- Layout and responsive design
- Additional features

### Desktop GUI Appearance
Modify `gui_app.py` to change:
- Window size and layout
- Fonts and colors
- Additional controls

### Adding New Voices
To add new voices, update the `voices` dictionary in both applications:

```python
self.voices = {
    'af_heart': 'AF Heart (Default)',
    'your_voice': 'Your Custom Voice',
    # ... other voices
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"Kokoro TTS is not available"**
   ```bash
   pip install kokoro soundfile
   ```

2. **"No module named 'flask'"**
   ```bash
   pip install flask
   ```

3. **"No module named 'pygame'"**
   ```bash
   pip install pygame
   ```

4. **"No module named 'tkinter'" (Desktop GUI)**
   ```bash
   # CachyOS/Arch Linux
   sudo pacman -S tk
   
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   ```

5. **Audio playback issues**
   - Make sure your system has audio drivers installed
   - Check volume settings
   - Try different audio formats

6. **Port already in use (Web Frontend)**
   - Change the port in `app.py`: `app.run(host='0.0.0.0', port=YOUR_PORT)`
   - Or kill existing processes: `pkill -f "python.*app.py"`

### Performance Tips

1. **First Run** - The first generation will be slower as models are downloaded
2. **GPU Acceleration** - CUDA will be used automatically if available
3. **Memory Usage** - Each language pipeline uses ~1GB RAM when loaded
4. **Concurrent Users** - The web frontend can handle multiple users simultaneously

## 🔒 Security Notes

- The web frontend runs in development mode by default
- For production use, configure a proper WSGI server (gunicorn, uwsgi)
- File uploads are limited to 16MB
- Text input is limited to 5000 characters

## 📞 Support

If you encounter any issues:

1. Check that Kokoro TTS is properly installed
2. Verify all dependencies are installed
3. Check the console output for error messages
4. Ensure audio system is working
5. Try both web and desktop versions to isolate issues

## 🎉 Success!

You now have two fully functional frontend applications for Kokoro TTS! 

- **Web Frontend**: Modern, accessible, multi-user capable
- **Desktop GUI**: Native, offline, single-user focused

Both applications provide all the features you requested and are ready to use on your CachyOS laptop.
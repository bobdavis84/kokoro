# Kokoro TTS Frontend Setup with UV for CachyOS

This guide will help you install and run the Kokoro TTS frontend applications using UV on your CachyOS system.

## Quick Setup Commands

Since your system has externally managed Python, we'll use UV to handle the Python environment properly.

### 1. Install System Dependencies

```bash
# Update package database
sudo pacman -Sy

# Install required system packages
sudo pacman -S --needed python python-pip espeak-ng tk
```

### 2. Install UV (if not already installed)

```bash
# Install UV using the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to your PATH (add this to your ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.cargo/bin:$PATH"

# Reload your shell or run:
source ~/.bashrc  # or source ~/.zshrc
```

### 3. Navigate to Frontend Directory

```bash
cd /path/to/kokoro/frontend  # Replace with actual path
```

### 4. Initialize UV Project

```bash
# Initialize UV project
uv init --name kokoro-frontend --no-readme

# Add required dependencies
uv add kokoro soundfile flask pygame

# Sync environment
uv sync
```

### 5. Test Installation

```bash
# Test Kokoro TTS
uv run python -c "import kokoro; print('Kokoro version:', kokoro.__version__)"

# Test Flask
uv run python -c "import flask; print('Flask version:', flask.__version__)"

# Test pygame
uv run python -c "import pygame; print('Pygame version:', pygame.version.ver)"

# Test tkinter
uv run python -c "import tkinter; print('Tkinter is available')"

# Test soundfile
uv run python -c "import soundfile; print('SoundFile version:', soundfile.__version__)"
```

## Running the Applications

### Web Frontend

```bash
# Start web frontend
uv run python app.py
```

Then open your browser to: http://localhost:53286

### Desktop GUI

```bash
# Start desktop GUI
uv run python gui_app.py
```

### Interactive Demo

```bash
# Run the demo script
uv run python demo.py
```

## Alternative: Using UVX (Isolated Execution)

If you prefer to use uvx for isolated execution:

```bash
# Note: This may have limitations with some dependencies
uvx --from kokoro kokoro --help

# For the frontend apps, UV project mode is recommended
```

## Troubleshooting

### If you get "externally-managed-environment" error:
- ✅ **Solution**: Use UV as shown above - it handles virtual environments automatically
- ❌ **Don't use**: `pip install` directly on CachyOS

### If UV is not found:
```bash
# Make sure UV is in your PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### If dependencies fail to install:
```bash
# Try updating UV
uv self update

# Clear UV cache
uv cache clean

# Retry installation
uv sync --reinstall
```

### If Kokoro models don't download:
```bash
# Test model download
uv run python -c "
from kokoro import KPipeline
pipeline = KPipeline()
print('Models downloaded successfully')
"
```

## Features Available

✅ **Web Frontend Features:**
- Voice Selection (8 voices)
- Language Selection (9 languages)  
- Speed Control (0.5x - 2.0x)
- Text Input (up to 5000 characters)
- Generate Speech Button
- Audio Playback Controls
- File Download/Save
- Real-time Status Updates

✅ **Desktop GUI Features:**
- All web features plus:
- Native file dialogs
- Drag & drop text files
- Better audio controls
- System integration

## File Structure

```
kokoro/frontend/
├── app.py                 # Flask web application
├── gui_app.py            # Tkinter desktop GUI
├── demo.py               # Interactive demo
├── requirements.txt      # Dependencies list
├── templates/
│   └── index.html       # Web interface template
├── start_web.sh         # Web startup script (pip version)
├── start_gui.sh         # GUI startup script (pip version)
└── README.md            # Full documentation
```

## UV Project Files (Created After Setup)

```
pyproject.toml           # UV project configuration
uv.lock                  # Dependency lock file
.venv/                   # Virtual environment (auto-created)
```

## Next Steps

1. Follow the setup commands above
2. Test the installation
3. Run either the web frontend or desktop GUI
4. Enjoy using Kokoro TTS!

For more detailed information, see the main README.md file.
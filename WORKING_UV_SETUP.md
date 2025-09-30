# Working UV Setup for Kokoro TTS

## Current Status

✅ **Kokoro is successfully installed and working** with regular pip installation
❌ **uvx has issues** due to spacy model installation requiring pip in isolated environments

## Working Solutions for CachyOS

### Method 1: Use Regular Installation (Recommended)

Since Kokoro is already installed and working perfectly:

```bash
# Direct usage (already working)
echo "Hello world!" | kokoro -m af_heart -o output.wav

# With text parameter
kokoro -t "Your text here" -m af_heart -o output.wav

# From file
kokoro -i input.txt -m af_heart -o output.wav
```

### Method 2: Create UV Project (For Development)

If you want to use uv for development, create a new project:

```bash
# Create a new uv project
uv init my-kokoro-project
cd my-kokoro-project

# Add kokoro as dependency
uv add kokoro soundfile

# Create a simple script
cat > tts.py << 'EOF'
#!/usr/bin/env python3
from kokoro import KPipeline
import soundfile as sf
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python tts.py 'text to speak' [output.wav]")
        return
    
    text = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "output.wav"
    
    # Initialize pipeline
    pipeline = KPipeline(lang_code='a')
    
    # Generate speech
    generator = pipeline(text, voice='af_heart')
    
    # Save first segment
    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(output, audio, 24000)
        print(f"Generated: {output}")
        break

if __name__ == "__main__":
    main()
EOF

# Run with uv
uv run python tts.py "Hello from UV project!"
```

### Method 3: System-wide Installation on CachyOS

For your CachyOS laptop, install system-wide:

```bash
# Install system dependencies
sudo pacman -S python python-pip espeak-ng

# Install kokoro
pip install kokoro soundfile

# Use directly
kokoro -t "Hello CachyOS!" -m af_heart -o cachyos_test.wav
```

## Available Commands

### Basic Usage
```bash
# Text to speech
kokoro -t "Your text here" -m af_heart -o output.wav

# From file
kokoro -i input.txt -m af_heart -o output.wav

# From stdin
echo "Hello!" | kokoro -m af_heart -o output.wav
```

### Voice Options
- `af_heart` - Default voice (American English)
- Use `-l` flag for different languages:
  - `a` - American English
  - `b` - British English
  - `e` - Spanish
  - `f` - French
  - `h` - Hindi
  - `i` - Italian
  - `j` - Japanese
  - `p` - Portuguese
  - `z` - Chinese

### Speed Control
```bash
# Slower speech
kokoro -t "Slow speech" -m af_heart -s 0.8 -o slow.wav

# Faster speech  
kokoro -t "Fast speech" -m af_heart -s 1.2 -o fast.wav
```

## Python API Usage

```python
from kokoro import KPipeline
import soundfile as sf

# Initialize
pipeline = KPipeline(lang_code='a')

# Generate
text = "Hello, this is Kokoro TTS!"
generator = pipeline(text, voice='af_heart')

# Save
for i, (graphemes, phonemes, audio) in enumerate(generator):
    sf.write(f'output_{i}.wav', audio, 24000)
    break
```

## Why UVX Currently Has Issues

The issue with `uvx` is that Kokoro tries to install spacy language models at runtime using pip, but uvx creates isolated environments without pip. This is a limitation of the current Kokoro package design.

## Recommended Approach for CachyOS

1. **For regular use**: Use the system-wide pip installation (already working)
2. **For development**: Create a uv project as shown in Method 2
3. **For scripting**: Use the Python API in your own scripts

The installation is complete and fully functional!
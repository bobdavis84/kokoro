# Running Kokoro with UV and UVX

This guide shows you how to run Kokoro using `uv` and `uvx` on your CachyOS laptop.

## Prerequisites

First, make sure you have `uv` installed:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Also ensure you have the system dependency:

```bash
# On CachyOS/Arch Linux
sudo pacman -S espeak-ng

# On Ubuntu/Debian
sudo apt-get install espeak-ng
```

## Method 1: Using `uvx` (Recommended for one-time usage)

`uvx` is perfect for running Kokoro without installing it permanently:

```bash
# Basic usage - generate speech from text
uvx kokoro -t "Hello, this is Kokoro TTS!" -m af_heart -o output.wav

# Read from a file
uvx kokoro -i input.txt -m af_heart -o output.wav

# Use different voices and languages
uvx kokoro -t "Bonjour le monde!" -m af_heart -l f -o french.wav

# Adjust speech speed
uvx kokoro -t "This is slower speech" -m af_heart -s 0.8 -o slow.wav
```

### Available Voices and Languages

- `a` - American English
- `b` - British English  
- `e` - Spanish (es)
- `f` - French (fr-fr)
- `h` - Hindi (hi)
- `i` - Italian (it)
- `j` - Japanese (requires: `uvx --with misaki[ja] kokoro ...`)
- `p` - Brazilian Portuguese (pt-br)
- `z` - Mandarin Chinese (requires: `uvx --with misaki[zh] kokoro ...`)

### Examples with Different Languages

```bash
# Spanish
uvx kokoro -t "Hola mundo, esto es una prueba." -m af_heart -l e -o spanish.wav

# French  
uvx kokoro -t "Bonjour le monde, ceci est un test." -m af_heart -l f -o french.wav

# Japanese (with additional dependency)
uvx --with misaki[ja] kokoro -t "こんにちは世界" -m af_heart -l j -o japanese.wav

# Chinese (with additional dependency)
uvx --with misaki[zh] kokoro -t "你好世界" -m af_heart -l z -o chinese.wav
```

## Method 2: Using `uv run` (For development)

If you're working with the source code:

```bash
# Clone the repository
git clone https://github.com/hexgrad/kokoro.git
cd kokoro

# Install dependencies
uv sync

# Run with uv
uv run kokoro -t "Hello from development version!" -m af_heart -o dev_output.wav
```

## Method 3: Python API with uvx

You can also use the Python API:

```bash
# Create a script
cat > tts_script.py << 'EOF'
from kokoro import KPipeline
import soundfile as sf

# Initialize pipeline
pipeline = KPipeline(lang_code='a')  # American English

# Generate speech
text = "Hello, this is the Kokoro TTS system running via uvx!"
generator = pipeline(text, voice='af_heart')

# Save audio
for i, (graphemes, phonemes, audio) in enumerate(generator):
    print(f"Generated: {graphemes}")
    print(f"Phonemes: {phonemes}")
    sf.write(f'output_{i}.wav', audio, 24000)
    break

print("Audio generated successfully!")
EOF

# Run the script with uvx
uvx --with soundfile --from kokoro python tts_script.py
```

## Troubleshooting

### Common Issues

1. **Missing espeak-ng**: Install with your system package manager
2. **CUDA warnings**: These are normal if you don't have a NVIDIA GPU
3. **Model downloads**: First run will download models (~327MB)

### Performance Tips

1. **GPU Acceleration**: On systems with NVIDIA GPUs, CUDA will be used automatically
2. **Apple Silicon**: Set `PYTORCH_ENABLE_MPS_FALLBACK=1` for GPU acceleration on M1/M2/M3/M4 Macs
3. **Memory**: The model requires ~1GB RAM when loaded

## Voice Options

The default voice is `af_heart`, but you can explore other voices by checking the voices directory after first run:

```bash
# List available voices (after first run)
ls ~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices/
```

## Advanced Usage

### Batch Processing

```bash
# Process multiple files
for file in *.txt; do
    uvx kokoro -i "$file" -m af_heart -o "${file%.txt}.wav"
done
```

### Custom Speed and Voice

```bash
# Slower, more dramatic speech
uvx kokoro -t "This is a dramatic announcement." -m af_heart -s 0.7 -o dramatic.wav

# Faster speech
uvx kokoro -t "Quick announcement!" -m af_heart -s 1.3 -o quick.wav
```

### Reading from stdin

```bash
# Pipe text directly
echo "Hello from stdin!" | uvx kokoro -m af_heart -o stdin_output.wav

# From a command output
date | uvx kokoro -m af_heart -o current_time.wav
```

## Integration Examples

### Shell Script

```bash
#!/bin/bash
# tts.sh - Simple TTS wrapper

TEXT="$1"
OUTPUT="${2:-output.wav}"
VOICE="${3:-af_heart}"

if [ -z "$TEXT" ]; then
    echo "Usage: $0 'text to speak' [output.wav] [voice]"
    exit 1
fi

uvx kokoro -t "$TEXT" -m "$VOICE" -o "$OUTPUT"
echo "Generated: $OUTPUT"
```

### Python Integration

```python
#!/usr/bin/env python3
import subprocess
import sys

def text_to_speech(text, output_file="output.wav", voice="af_heart"):
    """Convert text to speech using uvx kokoro"""
    cmd = ["uvx", "kokoro", "-t", text, "-m", voice, "-o", output_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Successfully generated: {output_file}")
        return True
    else:
        print(f"Error: {result.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tts_wrapper.py 'text to speak'")
        sys.exit(1)
    
    text_to_speech(sys.argv[1])
```

This guide should help you get started with Kokoro using `uv` and `uvx` on your CachyOS system!
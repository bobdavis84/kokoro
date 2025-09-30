#!/usr/bin/env python3
"""
Kokoro TTS Web Frontend
A Flask-based web interface for Kokoro Text-to-Speech
"""

import os
import tempfile
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import soundfile as sf
import torch

# Import Kokoro
try:
    from kokoro import KPipeline
    KOKORO_AVAILABLE = True
except ImportError:
    KOKORO_AVAILABLE = False
    print("Warning: Kokoro not available. Install with: pip install kokoro")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kokoro-tts-frontend-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories
UPLOAD_FOLDER = '/tmp/kokoro_uploads'
OUTPUT_FOLDER = '/tmp/kokoro_outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Voice and language configurations
VOICES = {
    'af_heart': 'AF Heart (Default)',
    'af_bella': 'AF Bella',
    'af_nicole': 'AF Nicole',
    'af_sarah': 'AF Sarah',
    'am_adam': 'AM Adam',
    'am_michael': 'AM Michael',
    'bf_emma': 'BF Emma',
    'bf_isabella': 'BF Isabella',
}

LANGUAGES = {
    'a': 'American English',
    'b': 'British English',
    'e': 'Spanish (es)',
    'f': 'French (fr-fr)',
    'h': 'Hindi (hi)',
    'i': 'Italian (it)',
    'j': 'Japanese (ja)',
    'p': 'Brazilian Portuguese (pt-br)',
    'z': 'Mandarin Chinese (zh)',
}

# Global pipeline cache
pipeline_cache = {}

def get_pipeline(lang_code):
    """Get or create a pipeline for the given language"""
    if not KOKORO_AVAILABLE:
        raise RuntimeError("Kokoro is not available")
    
    if lang_code not in pipeline_cache:
        pipeline_cache[lang_code] = KPipeline(lang_code=lang_code)
    return pipeline_cache[lang_code]

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         voices=VOICES, 
                         languages=LANGUAGES,
                         kokoro_available=KOKORO_AVAILABLE)

@app.route('/generate', methods=['POST'])
def generate_speech():
    """Generate speech from text"""
    if not KOKORO_AVAILABLE:
        return jsonify({'error': 'Kokoro TTS is not available'}), 500
    
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice = data.get('voice', 'af_heart')
        language = data.get('language', 'a')
        speed = float(data.get('speed', 1.0))
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_filename = f'kokoro_output_{file_id}.wav'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Get pipeline
        pipeline = get_pipeline(language)
        
        # Generate speech
        generator = pipeline(text, voice=voice, speed=speed)
        
        # Collect all audio segments
        audio_segments = []
        for i, (gs, ps, audio) in enumerate(generator):
            audio_segments.append(audio)
        
        if not audio_segments:
            return jsonify({'error': 'No audio generated'}), 500
        
        # Concatenate audio segments
        if len(audio_segments) == 1:
            final_audio = audio_segments[0]
        else:
            final_audio = torch.cat(audio_segments, dim=0)
        
        # Save audio file
        sf.write(output_path, final_audio.numpy(), 24000)
        
        # Return success response
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': output_filename,
            'download_url': url_for('download_file', file_id=file_id),
            'text': text,
            'voice': voice,
            'language': language,
            'speed': speed
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/download/<file_id>')
def download_file(file_id):
    """Download generated audio file"""
    try:
        filename = f'kokoro_output_{file_id}.wav'
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, 
                        as_attachment=True, 
                        download_name=f'kokoro_speech_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav',
                        mimetype='audio/wav')
    
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/status')
def status():
    """Get system status"""
    return jsonify({
        'kokoro_available': KOKORO_AVAILABLE,
        'voices': list(VOICES.keys()),
        'languages': list(LANGUAGES.keys()),
        'max_text_length': 5000
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("Starting Kokoro TTS Web Frontend...")
    print(f"Kokoro available: {KOKORO_AVAILABLE}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    
    # Run the app
    app.run(host='0.0.0.0', port=53286, debug=True)
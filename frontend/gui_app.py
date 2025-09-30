#!/usr/bin/env python3
"""
Kokoro TTS Desktop GUI
A tkinter-based desktop application for Kokoro Text-to-Speech
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import os
import tempfile
import uuid
from datetime import datetime
import pygame
import soundfile as sf
import torch

# Import Kokoro
try:
    from kokoro import KPipeline
    KOKORO_AVAILABLE = True
except ImportError:
    KOKORO_AVAILABLE = False

class KokoroTTSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kokoro TTS - Text to Speech")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Pipeline cache
        self.pipeline_cache = {}
        self.current_audio_file = None
        self.is_generating = False
        
        # Voice and language configurations
        self.voices = {
            'af_heart': 'AF Heart (Default)',
            'af_bella': 'AF Bella',
            'af_nicole': 'AF Nicole',
            'af_sarah': 'AF Sarah',
            'am_adam': 'AM Adam',
            'am_michael': 'AM Michael',
            'bf_emma': 'BF Emma',
            'bf_isabella': 'BF Isabella',
        }
        
        self.languages = {
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
        
        self.setup_ui()
        self.check_kokoro_status()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎤 Kokoro TTS", 
                               font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status indicator
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.status_label = ttk.Label(self.status_frame, text="🔴 Checking status...", 
                                     font=('Arial', 10))
        self.status_label.pack(side=tk.LEFT)
        
        # Text input
        text_label = ttk.Label(main_frame, text="Text to Convert:", font=('Arial', 12, 'bold'))
        text_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(main_frame, height=8, width=60, 
                                                   font=('Arial', 11), wrap=tk.WORD)
        self.text_input.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.text_input.bind('<KeyRelease>', self.update_char_count)
        
        # Character counter
        self.char_count_label = ttk.Label(main_frame, text="0 / 5000 characters", 
                                         font=('Arial', 9))
        self.char_count_label.grid(row=4, column=1, sticky=tk.E, pady=(0, 15))
        
        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Voice Settings", padding="15")
        controls_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(3, weight=1)
        controls_frame.columnconfigure(5, weight=1)
        
        # Voice selection
        ttk.Label(controls_frame, text="Voice:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.voice_var = tk.StringVar(value='af_heart')
        voice_combo = ttk.Combobox(controls_frame, textvariable=self.voice_var, 
                                  values=list(self.voices.keys()), state='readonly', width=15)
        voice_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Language selection
        ttk.Label(controls_frame, text="Language:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.language_var = tk.StringVar(value='a')
        language_combo = ttk.Combobox(controls_frame, textvariable=self.language_var, 
                                     values=list(self.languages.keys()), state='readonly', width=15)
        language_combo.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Speed control
        ttk.Label(controls_frame, text="Speed:", font=('Arial', 10, 'bold')).grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        speed_frame = ttk.Frame(controls_frame)
        speed_frame.grid(row=0, column=5, sticky=(tk.W, tk.E))
        
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(speed_frame, from_=0.5, to=2.0, 
                                    variable=self.speed_var, orient=tk.HORIZONTAL,
                                    command=self.update_speed_label)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x", font=('Arial', 9))
        self.speed_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=(0, 20))
        
        # Generate button
        self.generate_btn = ttk.Button(buttons_frame, text="🎵 Generate Speech", 
                                      command=self.generate_speech, style='Accent.TButton')
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load text file button
        load_btn = ttk.Button(buttons_frame, text="📁 Load Text File", 
                             command=self.load_text_file)
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(buttons_frame, text="🗑️ Clear", 
                              command=self.clear_text)
        clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var, 
                                       font=('Arial', 10))
        self.progress_label.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Audio controls frame
        audio_frame = ttk.LabelFrame(main_frame, text="Audio Playback", padding="15")
        audio_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Audio control buttons
        audio_buttons_frame = ttk.Frame(audio_frame)
        audio_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.play_btn = ttk.Button(audio_buttons_frame, text="▶️ Play", 
                                  command=self.play_audio, state='disabled')
        self.play_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.pause_btn = ttk.Button(audio_buttons_frame, text="⏸️ Pause", 
                                   command=self.pause_audio, state='disabled')
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(audio_buttons_frame, text="⏹️ Stop", 
                                  command=self.stop_audio, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(audio_buttons_frame, text="💾 Save As...", 
                                  command=self.save_audio, state='disabled')
        self.save_btn.pack(side=tk.RIGHT)
        
        # Audio info
        self.audio_info_label = ttk.Label(audio_frame, text="No audio generated", 
                                         font=('Arial', 9), foreground='gray')
        self.audio_info_label.pack()
    
    def check_kokoro_status(self):
        """Check if Kokoro is available"""
        if KOKORO_AVAILABLE:
            self.status_label.config(text="🟢 Kokoro TTS Ready", foreground='green')
            self.generate_btn.config(state='normal')
        else:
            self.status_label.config(text="🔴 Kokoro TTS Not Available", foreground='red')
            self.generate_btn.config(state='disabled')
            messagebox.showerror("Error", 
                               "Kokoro TTS is not available!\n\n"
                               "Please install it with:\n"
                               "pip install kokoro soundfile")
    
    def update_char_count(self, event=None):
        """Update character count"""
        text = self.text_input.get('1.0', tk.END).strip()
        count = len(text)
        self.char_count_label.config(text=f"{count} / 5000 characters")
        
        if count > 4500:
            self.char_count_label.config(foreground='red')
        elif count > 4000:
            self.char_count_label.config(foreground='orange')
        else:
            self.char_count_label.config(foreground='black')
    
    def update_speed_label(self, value):
        """Update speed label"""
        speed = float(value)
        self.speed_label.config(text=f"{speed:.1f}x")
    
    def get_pipeline(self, lang_code):
        """Get or create a pipeline for the given language"""
        if not KOKORO_AVAILABLE:
            raise RuntimeError("Kokoro is not available")
        
        if lang_code not in self.pipeline_cache:
            self.pipeline_cache[lang_code] = KPipeline(lang_code=lang_code)
        return self.pipeline_cache[lang_code]
    
    def generate_speech(self):
        """Generate speech in a separate thread"""
        if self.is_generating:
            return
        
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter some text to convert.")
            return
        
        if len(text) > 5000:
            messagebox.showerror("Error", "Text is too long (max 5000 characters).")
            return
        
        # Start generation in separate thread
        self.is_generating = True
        self.generate_btn.config(state='disabled')
        self.progress_var.set("Generating speech...")
        self.progress_bar.start()
        
        thread = threading.Thread(target=self._generate_speech_thread, 
                                 args=(text, self.voice_var.get(), 
                                      self.language_var.get(), self.speed_var.get()))
        thread.daemon = True
        thread.start()
    
    def _generate_speech_thread(self, text, voice, language, speed):
        """Generate speech in background thread"""
        try:
            # Get pipeline
            pipeline = self.get_pipeline(language)
            
            # Generate speech
            generator = pipeline(text, voice=voice, speed=speed)
            
            # Collect all audio segments
            audio_segments = []
            for i, (gs, ps, audio) in enumerate(generator):
                audio_segments.append(audio)
            
            if not audio_segments:
                raise RuntimeError("No audio generated")
            
            # Concatenate audio segments
            if len(audio_segments) == 1:
                final_audio = audio_segments[0]
            else:
                final_audio = torch.cat(audio_segments, dim=0)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            sf.write(temp_file.name, final_audio.numpy(), 24000)
            temp_file.close()
            
            # Update UI in main thread
            self.root.after(0, self._generation_complete, temp_file.name, text, voice, language, speed)
            
        except Exception as e:
            self.root.after(0, self._generation_error, str(e))
    
    def _generation_complete(self, audio_file, text, voice, language, speed):
        """Handle successful generation"""
        self.current_audio_file = audio_file
        self.is_generating = False
        self.generate_btn.config(state='normal')
        self.progress_bar.stop()
        self.progress_var.set("Generation complete!")
        
        # Enable audio controls
        self.play_btn.config(state='normal')
        self.save_btn.config(state='normal')
        
        # Update audio info
        voice_name = self.voices.get(voice, voice)
        lang_name = self.languages.get(language, language)
        self.audio_info_label.config(
            text=f"Generated: {voice_name} | {lang_name} | {speed:.1f}x speed",
            foreground='black'
        )
        
        messagebox.showinfo("Success", "Speech generated successfully!")
    
    def _generation_error(self, error_msg):
        """Handle generation error"""
        self.is_generating = False
        self.generate_btn.config(state='normal')
        self.progress_bar.stop()
        self.progress_var.set("Generation failed!")
        
        messagebox.showerror("Error", f"Speech generation failed:\n{error_msg}")
    
    def play_audio(self):
        """Play the generated audio"""
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                self.play_btn.config(state='disabled')
                self.pause_btn.config(state='normal')
                self.stop_btn.config(state='normal')
                self._check_playback()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play audio:\n{str(e)}")
    
    def pause_audio(self):
        """Pause audio playback"""
        pygame.mixer.music.pause()
        self.play_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
    
    def stop_audio(self):
        """Stop audio playback"""
        pygame.mixer.music.stop()
        self.play_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
        self.stop_btn.config(state='disabled')
    
    def _check_playback(self):
        """Check if audio is still playing"""
        if pygame.mixer.music.get_busy():
            self.root.after(100, self._check_playback)
        else:
            self.play_btn.config(state='normal')
            self.pause_btn.config(state='disabled')
            self.stop_btn.config(state='disabled')
    
    def save_audio(self):
        """Save the generated audio file"""
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showerror("Error", "No audio file to save.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
            title="Save Audio File"
        )
        
        if filename:
            try:
                import shutil
                shutil.copy2(self.current_audio_file, filename)
                messagebox.showinfo("Success", f"Audio saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio:\n{str(e)}")
    
    def load_text_file(self):
        """Load text from a file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Load Text File"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if len(content) > 5000:
                    if messagebox.askyesno("Warning", 
                                         f"The file contains {len(content)} characters, "
                                         "which exceeds the 5000 character limit. "
                                         "Do you want to load only the first 5000 characters?"):
                        content = content[:5000]
                    else:
                        return
                
                self.text_input.delete('1.0', tk.END)
                self.text_input.insert('1.0', content)
                self.update_char_count()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def clear_text(self):
        """Clear the text input"""
        self.text_input.delete('1.0', tk.END)
        self.update_char_count()
    
    def on_closing(self):
        """Handle application closing"""
        # Clean up temporary files
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                os.unlink(self.current_audio_file)
            except:
                pass
        
        # Stop audio
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        self.root.destroy()

def main():
    """Main function"""
    root = tk.Tk()
    app = KokoroTTSGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
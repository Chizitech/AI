import subprocess
import wave
import pyaudio
import numpy as np
import whisper
import torch
import os

class VoiceSystem:
    def __init__(self):
        self.sample_rate = 16000
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.audio = pyaudio.PyAudio()
        
        # Load Whisper for STT (tiny model for CPU)
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("tiny")
        
        # Use Piper TTS for local voice synthesis
        self.voice_model = "en_US-lessac-medium"  # Download from Piper releases
        
    def record_audio(self, duration=5):
        stream = self.audio.open(format=self.format, channels=self.channels,
                                rate=self.sample_rate, input=True,
                                frames_per_buffer=self.chunk)
        
        print("Listening...")
        frames = []
        for _ in range(0, int(self.sample_rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Save to file
        wf = wave.open("input.wav", 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return "input.wav"
    
    def speech_to_text(self, audio_file):
        result = self.whisper_model.transcribe(audio_file)
        return result["text"]
    
    def text_to_speech(self, text, output_file="output.wav"):
        # Using Piper TTS - install from GitHub releases
        try:
            subprocess.run([
                "piper", "--model", self.voice_model,
                "--output_file", output_file,
                "--text", text
            ], check=True)
            return output_file
        except:
            # Fallback to pyttsx3
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            return output_file
    
    def play_audio(self, file):
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

voice = VoiceSystem()
import subprocess
import json
import os

class LocalLLM:
    def __init__(self):
        self.model_path = "llama3.2:1b"  # Will use ollama
        self.check_model()
        
    def check_model(self):
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if self.model_path not in result.stdout:
                print(f"Pulling {self.model_path}...")
                subprocess.run(['ollama', 'pull', self.model_path])
        except:
            print("Ollama not installed. Please install from ollama.ai")
    
    def generate(self, prompt, max_tokens=256):
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model_path, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}. I'm still learning to communicate."

llm = LocalLLM()
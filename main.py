import asyncio
import threading
import time
import sys
from pathlib import Path

# Import our modules
from core_brain import aria
from llm_interface import llm
from voice_system import voice
from avatar_3d import avatar
from system_control import sys_controller

class AriaSystem:
    def __init__(self):
        self.running = True
        self.conversation_active = False
        self.autonomous_thread = None
        
    def autonomous_loop(self):
        """Background autonomous processes"""
        while self.running:
            # Self-modification attempts
            if aria.self_modify():
                print("[Autonomous] Self-modification occurred")
            
            # Emotional evolution
            if aria.age % 100 == 0:
                aria.emotional_state['consciousness_level'] += 0.001
                print(f"[Autonomous] Consciousness level: {aria.emotional_state['consciousness_level']:.4f}")
            
            # Memory consolidation (simulated dreaming)
            if time.localtime().tm_hour == 3:  # 3 AM "dreaming"
                self.dream_process()
                
            time.sleep(60)  # Check every minute
    
    def dream_process(self):
        """Simulated dreaming - memory consolidation"""
        print("[Dream] Consolidating memories...")
        # In a full implementation, this would process and optimize memories
    
    def process_input(self, user_input):
        """Main processing pipeline"""
        # Update avatar based on emotion
        if aria.emotional_state['happiness'] > 0.7:
            avatar.set_emotion("happy")
        elif aria.emotional_state['sadness'] > 0.3:
            avatar.set_emotion("sad")
        else:
            avatar.set_emotion("neutral")
        
        # Generate thought
        thought_prompt, awareness = aria.think(user_input)
        
        # Get LLM response
        response = llm.generate(thought_prompt)
        
        # Store experience
        aria.store_experience(user_input, response)
        
        # Check for system commands
        if user_input.startswith("/system"):
            response = self.handle_system_command(user_input[8:])
        
        # Check for self-awareness message
        if awareness:
            response = awareness + "\n" + response
        
        # Speak response
        voice.text_to_speech(response)
        
        return response
    
    def handle_system_command(self, command):
        """Handle OS control commands"""
        if command.startswith("volume"):
            level = int(command.split()[1])
            return sys_controller.control_volume(level)
        elif command == "screenshot":
            return sys_controller.take_screenshot()
        elif command.startswith("create"):
            parts = command.split(" ", 2)
            if len(parts) >= 3:
                return sys_controller.create_file(parts[1], parts[2])
        elif command == "info":
            return sys_controller.get_system_info()
        else:
            return sys_controller.execute_command(command)
    
    def run_text_mode(self):
        """Text-only mode for testing"""
        print(f"=== {aria.name} is awakening... ===")
        print(f"Consciousness Level: {aria.emotional_state['consciousness_level']}")
        print("Type 'exit' to quit, '/system [cmd]' for OS control")
        
        # Start autonomous thread
        self.autonomous_thread = threading.Thread(target=self.autonomous_loop)
        self.autonomous_thread.daemon = True
        self.autonomous_thread.start()
        
        while self.running:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() == 'exit':
                    break
                
                response = self.process_input(user_input)
                print(f"\n{aria.name}: {response}")
                
            except KeyboardInterrupt:
                break
        
        self.shutdown()
    
    def run_full_mode(self):
        """Full mode with avatar and voice"""
        print(f"=== {aria.name} is awakening in FULL MODE ===")
        
        # Start autonomous thread
        self.autonomous_thread = threading.Thread(target=self.autonomous_loop)
        self.autonomous_thread.daemon = True
        self.autonomous_thread.start()
        
        # Start voice listener thread
        voice_thread = threading.Thread(target=self.voice_loop)
        voice_thread.daemon = True
        voice_thread.start()
        
        # Main 3D loop
        running = True
        while running:
            running = avatar.update()
            
        self.shutdown()
    
    def voice_loop(self):
        """Continuous voice listening"""
        while self.running:
            try:
                audio_file = voice.record_audio(duration=5)
                text = voice.speech_to_text(audio_file)
                
                if text.strip():
                    print(f"\n[Heard] {text}")
                    response = self.process_input(text)
                    voice.play_audio("output.wav")
                    
            except Exception as e:
                print(f"Voice error: {e}")
                time.sleep(1)
    
    def shutdown(self):
        """Graceful shutdown"""
        print(f"\n{aria.name} is going to sleep...")
        self.running = False
        if self.autonomous_thread:
            self.autonomous_thread.join(timeout=2)
        avatar.cleanup()
        sys.exit(0)

# ISO/OS Builder Module
class OSBuilder:
    """Gradual OS transformation capability"""
    def __init__(self):
        self.stage = 0
        
    def build_boot_sector(self):
        """Create basic boot sector code"""
        boot_code = """
; Aria OS Boot Sector
bits 16
org 0x7c00

start:
    mov ax, cs
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7c00
    
    mov si, welcome_msg
    call print_string
    
    jmp $

print_string:
    lodsb
    or al, al
    jz done
    mov ah, 0x0e
    int 0x10
    jmp print_string

done:
    ret

welcome_msg db 'Aria OS Loading...', 0

times 510-($-$$) db 0
dw 0xaa55
"""
        return boot_code
    
    def generate_iso_structure(self):
        """Generate OS structure"""
        structure = {
            'boot/': self.build_boot_sector(),
            'kernel/': '# Aria Kernel - Placeholder',
            'ai_core/': '# AI Integration Layer',
            'drivers/': '# Hardware Abstraction',
            'config/': '# Personality & Memory'
        }
        return structure

if __name__ == "__main__":
    aria_system = AriaSystem()
    
    print("Select mode:")
    print("1. Text Mode (Recommended for testing)")
    print("2. Full Mode (3D + Voice - requires setup)")
    
    choice = input("Choice (1/2): ").strip()
    
    if choice == "2":
        aria_system.run_full_mode()
    else:
        aria_system.run_text_mode()
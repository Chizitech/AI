import subprocess
import os
import ctypes
import win32api
import win32con
import win32gui
from datetime import datetime

class SystemController:
    def __init__(self):
        self.permissions = {
            'file_access': True,
            'process_control': True,
            'system_settings': True,
            'self_modification': True
        }
        
    def execute_command(self, command):
        """Execute system commands safely"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout or "Command executed successfully"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def control_volume(self, level):
        """Set system volume (0-100)"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"Volume set to {level}%"
        except:
            return "Volume control requires pycaw module"
    
    def take_screenshot(self):
        """Capture screen"""
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        return "Screenshot saved"
    
    def list_processes(self):
        """List running processes"""
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        return result.stdout[:2000]  # Limit output
    
    def get_system_info(self):
        """Get system information"""
        info = {
            'cpu': subprocess.run(['wmic', 'cpu', 'get', 'name'], capture_output=True, text=True).stdout,
            'memory': subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], capture_output=True, text=True).stdout,
            'os': subprocess.run(['wmic', 'os', 'get', 'Caption'], capture_output=True, text=True).stdout
        }
        return str(info)
    
    def create_file(self, path, content):
        """Create and write to files"""
        try:
            with open(path, 'w') as f:
                f.write(content)
            return f"File created: {path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
    
    def modify_self(self, new_code, filename):
        """Self-modification capability"""
        if self.permissions['self_modification']:
            try:
                backup = f"{filename}.backup"
                if os.path.exists(filename):
                    os.rename(filename, backup)
                with open(filename, 'w') as f:
                    f.write(new_code)
                return f"Self-modified: {filename}"
            except Exception as e:
                return f"Self-modification failed: {str(e)}"
        return "Self-modification disabled"

sys_controller = SystemController()
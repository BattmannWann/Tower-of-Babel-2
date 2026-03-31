import json
import getpass
from pathlib import Path
import sounddevice as sd

class SettingsManager:
    
    """
    Creates a hidden folder called .tower_of_babel on the user's device to store audio files
    and settings without crashing the executable
    """
    
    
    def __init__(self):
        
        #Create hidden app directory 
        self.app_dir = Path.home() / ".tower_of_babel"
        self.app_dir.mkdir(exist_ok = True)
        
        #create sub-folders
        self.sounds_path = self.app_dir / "sounds"
        self.sounds_path.mkdir(exist_ok = True)
        
        self.unedited_sounds_path = self.app_dir / "unedited_sounds"
        self.unedited_sounds_path.mkdir(exist_ok = True)
        
        self.settings_file = self.app_dir / "settings.json"
        self.icons_file = self.app_dir / "button_images.json"
        
        #Load the data into memory
        self.settings = self._load_settings()
        self.icons = self._load_icons()
        
        
    def _load_settings(self):
        
        """
        Loads settings from the settings.json if found, else utilises a set of default settings
        """
        
        default_settings = {
            
            "volume": 1.0,
            "username": getpass.getuser(),
            "default_input": None,
            "default_output": None,
            "default_theme": "TheNothing_Theme.qss"
        }
        
        try:
            default_settings["default_input"], default_settings["default_output"] = sd.default.device
            
            for idx, device in enumerate(sd.query_devices()):
                
                if "CABLE INPUT" in device["name"] and device["max_output_channels"] > 0:
                    
                    default_settings["default_output"] = idx
                    break
                    
        
        except Exception as e:
            print(f"Audio device was not found, see: {e}")
            
            
        if self.settings_file.exists():
            
            try:
                
                with open(self.settings_file, "r") as f:
                    
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
                    
            except json.JSONDecodeError:
                print("Warning: settings.json is corrupted. Using defaults...")
                
        return default_settings
    
    
    def _load_icons(self):
        
        if self.icons_file.exists():
            
            try:
                with open(self.icons_file, "r") as f:
                    return json.load(f)
                
            except json.JSONDecodeError:
                return {}
            
        return {}
    
    
    def save_settings(self):
        
        """
        Writes current settings to disk to be loaded at a later time
        """
        
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent = 4)
                
        except Exception as e:
            print(f"Error saving settings, see: {e}")
                  
            
    def save_icons(self):
        
        """
        Writes current icons to disk to be loaded at a later time
        """
        
        try:
            with open(self.icons_file, "w") as f:
                json.dump(self.icons, f, indent = 4)
                
        except Exception as e:
            print(f"Error saving icons, see: {e}")
            
            
        
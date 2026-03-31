import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path
from core.settings_manager import SettingsManager
from core.utils import get_resource_path

def main():
    
    app = QApplication(sys.argv)
    
    settings_manager = SettingsManager()
    theme_filename = settings_manager.settings.get("default_theme")
    
    try:

        if theme_filename:
            
            theme_path = get_resource_path(f"resources/themes/{theme_filename}")
            
            if theme_path.exists():

                with open(theme_path, "r") as style_file:
                    app.setStyleSheet(style_file.read())
                    
            else:
                print(f"Warning: Could not find theme at: {theme_path}")
                
    except Exception as e:
        
        print(f"Error loading theme, see: {e}")

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    
    main()
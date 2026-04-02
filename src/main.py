import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path
from core.settings_manager import SettingsManager
from core.utils import get_resource_path, set_theme

def main():
    
    app = QApplication(sys.argv)
    
    settings_manager = SettingsManager(app)
    theme_filename = settings_manager.settings.get("default_theme")
    
    set_theme(theme_filename, app)

    window = MainWindow(app)
    window.show()
    
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    
    main()
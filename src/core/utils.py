import sys
from pathlib import Path

def get_resource_path(relative_path: str) -> Path:
    
    """
    Get the absolute path to a resource.
    """
    
    try:
        #PyInstaller will create a temp folder and store the path in _MEIPASS
        base_path = Path(sys._MEIPASS)
        
    except AttributeError:
        
        #Else, if it is not the executable running, use the project root
        base_path = Path(__file__).resolve().parent.parent.parent
        
    return base_path / relative_path


def set_theme(theme_filename, app):
    
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
    
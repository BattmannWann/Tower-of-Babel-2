import os
import sys
import pathlib

APP_NAME = "TowerOfBabel2"

def get_appdata_dir():
    """Return %APPDATA%\TowerOfBabel2"""
    appdata = pathlib.Path(os.getenv("APPDATA", pathlib.Path.home()))
    cfg = appdata / APP_NAME
    cfg.mkdir(parents=True, exist_ok=True)
    return cfg

def get_localappdata_dir():
    """Return %LOCALAPPDATA%\TowerOfBabel2 (for cache/logs)"""
    local = pathlib.Path(os.getenv("LOCALAPPDATA", pathlib.Path.home()))
    cfg = local / APP_NAME
    cfg.mkdir(parents=True, exist_ok=True)
    return cfg

def resource_path(relative_path: str) -> pathlib.Path:
    """
    Get absolute path to bundled resource (works for frozen exe and script).
    """
    if getattr(sys, "frozen", False):
        # Running as compiled exe
        base_path = pathlib.Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else pathlib.Path(sys.executable).parent
    else:
        # Running from source
        base_path = pathlib.Path(__file__).parent
    return base_path / relative_path

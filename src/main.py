import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path

def main():
    
    app = QApplication(sys.argv)

    # style_path_dir = Path(__file__).parent / "assets"
    # style_paths = list(style_path_dir.rglob("*.qss"))

    # if style_paths:

    #     with open(style_paths[0], "r") as style_file:
    #         app.setStyleSheet(style_file.read())

    # else:
    #     print(f"Styling warning: could not find any .qss files in {style_path_dir}")

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    
    main()
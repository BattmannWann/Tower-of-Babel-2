import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path

def main():
    
    app = QApplication(sys.argv)

    style_path = Path(__file__).parent / "assets" / "styles.qss"

    if style_path.exists():

        with open(style_path, "r") as style_file:
            app.setStyleSheet(style_file.read())

    else:
        print(f"Styling warning: could not find: {style_path}")

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    
    main()
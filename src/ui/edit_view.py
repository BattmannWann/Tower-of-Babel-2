from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QScrollArea, QMessageBox, QInputDialog, QFileDialog, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pathlib import Path


class EditView(QWidget):
    
    def __init__(self, settings_manager):
        
        super().__init__()
        self.settings_manager = settings_manager
        
        #Main Layout
        self.layout = QVBoxLayout(self)
        
        title = QLabel("Edit Sounds")
        font = title.font()
        
        font.setPointSize(24)
        font.setBold(True)
        
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)
        self.layout.addSpacing(20)
        
        
        #Scroll Area for the list of sounds
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        
        #Grid inside scroll area to hold the sounds
        self.grid_container = QWidget()
        self.grid = QGridLayout(self.grid_container)
        
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.grid_container)
        self.layout.addWidget(self.scroll_area)
        
        self.load_sounds()
        
        
    def load_sounds(self):
        
        """
        Scans the folder and builds a row for each sound
        """
        
        #Clears the grid list such that on events such as renaming the list is correct
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            
            if widget:
                widget.deleteLater()
                
        headers = ["Icon", "Sound Name", "Options"]
        
        for col, text in enumerate(headers):
            
            label = QLabel(text)
            
            font = label.font()
            font.setBold(True)
            font.setPointSize(24)
            
            
            label.setFont(font)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.grid.addWidget(label, 0, col)
            
            
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.grid.addWidget(line, 1, 0, 1, 3)
        
        sounds_dir = self.settings_manager.sounds_path
        valid_extensions = {".wav", ".mp3"}
        
        files = [file for file in sounds_dir.iterdir() if file.is_file() and file.suffix.lower() in valid_extensions]
        
        
        for row, file_path in enumerate(files, start = 2):
            
            name = file_path.stem
            
            #COLUMNS: 0 = Icon, 1 = Name, 2 = Options Button
            icon_label = QLabel()
            icon_path = self.settings_manager.icons.get(name)
            
            if icon_path and Path(icon_path).exists():
                icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
                
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid.addWidget(icon_label, row, 0)
            
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid.addWidget(name_label, row, 1)
            
            options_widget = QWidget()
            options_layout = QHBoxLayout(options_widget)
            options_layout.setContentsMargins(0, 0, 0, 0)
            
            icon_btn = QPushButton("Change Icon")
            icon_btn.clicked.connect(lambda checked, n=name: self._change_icon(n))
            
            rename_btn = QPushButton("Rename")
            rename_btn.clicked.connect(lambda checked, p=file_path: self._rename_sound(p))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, p=file_path: self._delete_sound(p))
            
            options_layout.addWidget(icon_btn)
            options_layout.addWidget(rename_btn)
            options_layout.addWidget(delete_btn)
            
            self.grid.addWidget(options_widget, row, 2)
            
            
    def _change_icon(self, name):
        
        """
        Opens file picker and saved the new icon path
        """
        
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select Icon for {name}", "", "Images (*.png *.jpg *jpeg)")
        
        if file_path:

            self.settings_manager.icons[name] = file_path
            self.settings_manager.save_icons()
            self.load_sounds()

        
    def _rename_sound(self, file_path):

        """
        Safely renames a file using PySide6's built-in text dialogue
        """

        old_name = file_path.stem
        new_name, ok = QInputDialog.getText(self, "Rename Sound", f"Enter a new name for: {old_name}")

        if ok and new_name.strip() and new_name.strip() != old_name:

            new_path = file_path.with_name(f"{new_name.strip()}{file_path.suffix}")

            if new_path.exists():

                QMessageBox.warning(self, "Error", "A sound with this name already exists.")
                return
            
            try:
                file_path.rename(new_path)

                if old_name in self.settings_manager.icons:

                    self.settings_manager.icons[new_name.strip()] = self.settings_manager.icons.pop(old_name)
                    self.settings_manager.save_icons()


                self.load_sounds()

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not rename file, see: {e}")

        
    def _delete_sound(self, file_path):

        """
        Deletes a file, asking for confirmation before deleting a file
        """

        reply = QMessageBox.question(self, 
            "Confirm Deletion", 
            f"Are you sure you want to delete '{file_path.stem}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:

            try:
                #Safely removes the file
                file_path.unlink()

                #Also removes the icon
                if file_path.stem in self.settings_manager.icons:

                    del self.settings_manager.icons[file_path.stem]
                    self.settings_manager.save_icons()

                self.load_sounds()

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete the file: {file_path.stem}, see: {e}")



                





from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QScrollArea
)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class HomeView(QWidget):
    
    def __init__(self, settings_manager, audio_player):
        
        super().__init__()
        
        self.settings_manager = settings_manager
        self.audio_player = audio_player
        
        self.layout = QVBoxLayout(self)
        
        self.welcome_label = QLabel(f"Welcome {self.settings_manager.settings['username']}!")
        
        font = self.welcome_label.font()
        font.setPointSize(28)
        font.setBold(True)
        
        self.welcome_label.setFont(font)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.welcome_label)
        
        #Create the scroll area in the case of many many sounds
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        #Where the buttons will live
        self.grid_container = QWidget()
        self.grid = QGridLayout(self.grid_container)
        self.grid.setSpacing(20)
        
        #Add buttons grid to the scroll area
        self.scroll_area.setWidget(self.grid_container)
        self.layout.addWidget(self.scroll_area)
        
        #Populates the buttons
        self.load_sounds()
        
        
    def load_sounds(self):
        
        """
        Scans the sounds folder and creates a button for each file
        """
        
        #Clear the grid on view refresh
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            
            if widget:
                widget.deleteLater()
                
                
        sounds_dir = self.settings_manager.sounds_path
        
        #retrieve all valid audio files
        valid_extensions = {".wav", ".mp3"}
        files = [f for f in sounds_dir.iterdir() if f.is_file() and f.suffix.lower() in valid_extensions]
        
        #if no files....
        if not files:
            
            no_files_label = QLabel("Looks like we don't have any files yet. \nGo to 'Add File(s) to add some sounds!")
            
            font = no_files_label.font()
            font.setPointSize(16)
            
            no_files_label.setFont(font)
            no_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.grid.addWidget(no_files_label, 0, 0)
            
            return
        
        #else...
        icons = self.settings_manager.icons
        
        for idx, file_path in enumerate(files):
            
            #file name with NO extension
            name = file_path.stem
            
            btn = QPushButton(f"  {name[:30]}...")
            btn.setFixedHeight(75)
            
            font = btn.font()
            font.setPointSize(12)
            
            btn.setFont(font)
            
            # TODO: Add custom icon logic
            
            
            devices = [
                self.settings_manager.settings.get("default_input"),
                self.settings_manager.settings.get("default_output")
            ]
            
            volume = self.settings_manager.settings.get("volume", 1.0)
            
            btn.clicked.connect(lambda checked = False, p = file_path, d = devices, v = volume: 
                self.audio_player.play_sound(p, d, v))
            
            #Place buttons in a 3-column grid
            row, col = divmod(idx, 3)
            self.grid.addWidget(btn, row, col)
            
        
        
        
        
        
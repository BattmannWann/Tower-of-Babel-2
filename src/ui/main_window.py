import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout, 
    QLabel, QToolBar, QFileDialog)

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QAction

from core.settings_manager import SettingsManager
from core.utils import get_resource_path
from core.audio_player import AudioPlayer

from ui.home_view import HomeView


"""
Main Window Class:
    
    This inherits from QMainWindow which provides a neat little widget 
    that allows us to personalise the main window with ease.
    
    This will be developed in a deck of cards layout, such that the application has a modern look and feel.
"""



class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        #Create a settings manager object - handles all settings needs
        self.settings_manager = SettingsManager()
        
        #Create the audio engine
        self.audio_player = AudioPlayer()
        
        self.setWindowTitle(f"Tower of Babel 2.0 - Welcome {self.settings_manager.settings['username']}")
        self.setMinimumSize(QSize(800, 500))
        
        
        #Fetch the app icon
        icon_path = get_resource_path("resources/icons/cassette.png")
        
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            
        
        #Build the toolbar
        self._setup_toolbar()
        
        # Central stacked widget, set as the app's main widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Application views
        self.home_view = HomeView(self.settings_manager, self.audio_player)
        
        
        self.settings_view = self._create_placeholder_view("Settings View\Config goes here")
        self.edit_view = self._create_placeholder_view("Edit View\nTrimming goes here")
        
        # Add views onto the stack
        self.stacked_widget.addWidget(self.home_view)       # Index 0
        self.stacked_widget.addWidget(self.settings_view)   # Index 1
        self.stacked_widget.addWidget(self.edit_view)       # Index 2
        
        self.stacked_widget_indexes = {self.home_view: 0, self.settings_view: 1, self.edit_view: 2}
        
        
        self.stacked_widget.setCurrentIndex(0)
        
        
    def _create_placeholder_view(self, text):
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        font = label.font()
        font.setPointSize(24)
        
        label.setFont(font)
        layout.addWidget(label)
        
        widget.setLayout(layout)
        return widget
    
    
    def _setup_toolbar(self):
        
        """
        Builds the top menu bar for navigation and actions
        """
        
        toolbar = QToolBar("Main Navigation")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        #Home Button (switches the stacked layout index to 0)
        home_action = QAction("Home", self)
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget_indexes[self.home_view]))
        toolbar.addAction(home_action)
        
        #Settings Button (Switches to Index 1)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget_indexes[self.settings_view]))
        toolbar.addAction(settings_action)
        
        toolbar.addSeparator()
        
        #Add File(s) Button
        add_files_action = QAction("Add File(s)", self)
        add_files_action.triggered.connect(self._add_files)
        toolbar.addAction(add_files_action)
        
        #Stop Sound(s) Button
        stop_sounds_action = QAction("Stop Sound(s)", self)
        stop_sounds_action.triggered.connect(self.audio_player.stop)
        toolbar.addAction(stop_sounds_action)
        
        
    def _add_files(self):
        
        """
        Opens a file dialogue, copies the files to the hidden folder, and refreshes the UI
        """
        
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav)"
        )
        
        if file_paths:
            
            for path in file_paths:
                
                source = Path(path)
                destination = self.settings_manager.sounds_path / source.name
                
                try:
                    #preserves file metadata
                    shutil.copy2(source, destination)
                    
                except Exception as e:
                    print(f"Failed to copy {source.name}, see: {e}")
                    
            self.home_view.load_sounds()
        
        
        
        
    def closeEvent(self, event):
        
        self.audio_player.stop()
        super().closeEvent(event)
        
        
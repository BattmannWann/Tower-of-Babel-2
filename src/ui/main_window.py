from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon

from core.settings_manager import SettingsManager
from core.utils import get_resource_path

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
        
        self.setWindowTitle(f"Tower of Babel 2.0 - Welcome {self.settings_manager.settings['username']}")
        self.setMinimumSize(QSize(800, 500))
        
        
        #Fetch the app icon
        icon_path = get_resource_path("resources/icons/cassette.png")
        
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            
        
        # Central stacked widget, set as the app's main widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Application views
        self.home_view = HomeView(self.settings_manager)
        
        
        self.settings_view = self._create_placeholder_view("Settings View\Config goes here")
        self.edit_view = self._create_placeholder_view("Edit View\nTrimming goes here")
        
        # Add views onto the stack
        self.stacked_widget.addWidget(self.home_view)       # Index 0
        self.stacked_widget.addWidget(self.settings_view)   # Index 1
        self.stacked_widget.addWidget(self.edit_view)       # Index 2
        
        
        self.stacked_widget.setCurrentIndex(0)
        
        
    def _create_placeholder_view(self, text):
        
        """
        A temporary helper function to create blank pages
        """
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        font = label.font()
        font.setPointSize(24)
        
        return widget
        
        
        
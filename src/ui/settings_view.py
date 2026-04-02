from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QSlider, QMessageBox
)

from PySide6.QtCore import Qt
import sounddevice as sd
from pathlib import Path
from core.utils import get_resource_path, set_theme

class SettingsView(QWidget):
    
    def __init__(self, settings_manager):
        
        super().__init__()
        
        self.settings_manager = settings_manager
        
        #Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        #Title
        title = QLabel("Application Settings")
        font = title.font()
        
        font.setPointSize(24)
        font.setBold(True)
        
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(title)
        self.layout.addSpacing(30)
        
        #Grid for the form
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(20)
        
        self.grid.setHorizontalSpacing(20)
        self.layout.addLayout(self.grid)
        
        self._build_form()
        
        
    def _build_form(self):
        
        """
        Constructs the settings inputs and populates current data
        """
        
        settings = self.settings_manager.settings
        
        #Username
        self.grid.addWidget(QLabel("Username: "), 0, 0, Qt.AlignmentFlag.AlignRight)
        self.username_input = QLineEdit()
        
        self.username_input.setText(settings.get("username", ""))
        self.username_input.setPlaceholderText("Enter your display name...")
        
        self.username_input.setFixedWidth(300)
        self.grid.addWidget(self.username_input, 0, 1)
        
        
        #Volume Slider
        self.grid.addWidget(QLabel("Default Volume: "), 1, 0, Qt.AlignmentFlag.AlignRight)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        
        self.volume_slider.setRange(0, 100)
        
        #Volume is a float from 0.0 to 1.0, so convert to an integer
        self.volume_slider.setValue(int(settings.get("volume", 1.0) * 100))
        
        self.volume_slider.setFixedWidth(300)
        
        self.volume_label = QLabel(f"{self.volume_slider.value()}%")
        self.volume_slider.valueChanged.connect(lambda v: self.volume_label.setText(f"{v}%"))
        
        self.grid.addWidget(self.volume_slider, 1, 1)
        self.grid.addWidget(self.volume_label, 1, 2)
        
        
        #Audio Devices
        self.grid.addWidget(QLabel("Primary Output (Headphones): "), 2, 0, Qt.AlignmentFlag.AlignRight)
        self.input_combo = QComboBox()
        self.input_combo.setFixedWidth(300)
        self.grid.addWidget(self.input_combo, 2, 1)
        
        self.grid.addWidget(QLabel("Secondary Output (Virtual Cable): "), 3, 0, Qt.AlignmentFlag.AlignRight)
        self.output_combo = QComboBox()
        self.output_combo.setFixedWidth(300)
        self.grid.addWidget(self.output_combo, 3, 1)
        
        self._populate_audio_devices()
        
        
        #Application Theme
        self.grid.addWidget(QLabel("Theme: "), 4, 0, Qt.AlignmentFlag.AlignRight)
        self.theme_combo = QComboBox()
        self.theme_combo.setFixedWidth(300)
        self.grid.addWidget(self.theme_combo, 4, 1)
        
        self._populate_themes()
        
        
    
        #Save button
        self.layout.addSpacing(30)
        save_btn = QPushButton("Save Settings")
        
        save_btn.setFixedWidth(150)
        save_btn.clicked.connect(self.save_settings)
        
        self.layout.addWidget(save_btn, alignment = Qt.AlignmentFlag.AlignCenter)
        
        
        
    def _populate_themes(self):
    
        style_path_dir = get_resource_path("resources/themes/")
        style_paths = {file.name.strip(".qss").replace("_", " "): file.name for file in list(style_path_dir.rglob("*.qss"))}
        
        if style_paths:
            
            for key, value in style_paths.items():
                self.theme_combo.addItem(key, userData = value)

        saved_theme = self.settings_manager.settings.get("default_theme")
        
        if saved_theme:
            index = self.theme_combo.findData(saved_theme)
            
            if index != -1:
                self.theme_combo.setCurrentIndex(index)
                
        
    def _populate_audio_devices(self):
        
        """
        Fetches hardware devices and attaches their real IDs.
        """
        
        try:
            devices = sd.query_devices()
            
        except Exception as e:
            
            print(f"Warning: Could not query audio devices, see: {e}")
            return
        
        saved_input = self.settings_manager.settings.get("default_input")
        saved_output = self.settings_manager.settings.get("default_output")
        
        #Add a default option
        self.input_combo.addItem("System Default", userData = None)
        self.output_combo.addItem("System Default", userData = None)
        
        for idx, device in enumerate(devices):
            
            try:
            
                hostapi_name = sd.query_devices(device["hostapi"])["name"]
                display_name = f"{device['name']} ({hostapi_name})"
                
                #user userData = i to securely store hardware index
                if device["max_output_channels"] > 0:
                    
                    self.input_combo.addItem(display_name, userData = idx)
                    
                    if idx == saved_input:
                        self.input_combo.setCurrentIndex(self.input_combo.count() - 1)
                        
                    self.output_combo.addItem(display_name, userData = idx)
                    
                    if idx == saved_output:
                        self.output_combo.setCurrentIndex(self.output_combo.count() - 1)
                        
            except Exception as e:
                print(f"Skipping device {idx} due to an error, see: {e}")
                    
                    
    def save_settings(self):
        
        """
        Updates Memory and rewrites to the JSON file settings
        """
        
        #Retrieve the REAL hardware IDs from userData
        selected_input = self.input_combo.currentData()
        selected_output = self.output_combo.currentData()
        
        #Update the dictionary
        self.settings_manager.settings["username"] = self.username_input.text().strip()
        self.settings_manager.settings["volume"] = self.volume_slider.value() / 100
        
        self.settings_manager.settings["default_input"] = selected_input
        self.settings_manager.settings["default_output"] = selected_output
        
        self.settings_manager.settings["default_theme"] = self.theme_combo.currentData()
        
        #Write to disk
        self.settings_manager.save_settings()
        
        set_theme(self.theme_combo.currentData(), self.settings_manager.app_instance)
        
        #Provide user feedback
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        
        

        
        
        
        
        
        
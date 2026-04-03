import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout, 
    QLabel, QToolBar, QFileDialog, QDialog, QTextBrowser, QPushButton, QSlider, QCheckBox)

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QAction

from core.settings_manager import SettingsManager
from core.utils import get_resource_path
from core.audio_player import AudioPlayer

from ui.home_view import HomeView
from ui.settings_view import SettingsView
from ui.edit_view import EditView


"""
Main Window Class:
    
    This inherits from QMainWindow which provides a neat little widget 
    that allows us to personalise the main window with ease.
    
    This will be developed in a deck of cards layout, such that the application has a modern look and feel.
"""



class SetupGuideDialog(QDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        self.setWindowTitle("How to Setup with Discord")
        self.setFixedSize(500, 500)
        
        layout = QVBoxLayout(self)
        
        guide_text = QTextBrowser()
        guide_text.setOpenExternalLinks(True)
        
        instructions = """
        
        <h2 style="text-align: center;">Discord & Voice Chat Setup</h2>
        <p>To let your friends hear the soundboard <b>AND</b> your voice at the same time, follow these quick steps:</p>
        
        <h3>Step 1: Set Up the App</h3>
        <ul>
            <li>Go to the <b>Settings</b> tab in this app.</li>
            <li>Set Primary Output to your <b>Headphones</b> (e.g., SteelSeries Sonar Gaming).</li>
            <li>Set Secondary Output to <b>CABLE Input (VB-Audio Virtual Cable)</b> (or as close to this name).</li>
        </ul>

        <h3>Step 2: Connect Your Real Microphone</h3>
        <p>We need to route your physical mic into the virtual cable.</p>
        <ol>
            <li>Press <b>Windows Key + R</b>, type <code>mmsys.cpl</code>, and hit Enter.</li>
            <li>Go to the <b>Recording</b> tab and double-click your physical Microphone.</li>
            <li>Go to the <b>Listen</b> tab.</li>
            <li>Check the box that says <b>"Listen to this device"</b>.</li>
            <li>In the dropdown below it, select <b>CABLE Input (VB-Audio Virtual Cable)</b>.</li>
            <li>Click Apply and OK!</li>
        </ol>

        <h3>Step 3: Set Up Discord</h3>
        <ul>
            <li>Open Discord Settings > Voice & Video.</li>
            <li>Set your Input Device (Mic) to <b>CABLE Output</b>.</li>
            <li><i>Optional: Turn off Discord's "Echo Cancellation" and "Noise Suppression" so the sounds play clearly!</i></li>
        </ul>
        <h4 style="text-align: center; color: #4CAF50;">🎉 You're all set!</h4>
        """
        
        guide_text.setHtml(instructions)
        layout.addWidget(guide_text)
        
        close_button = QPushButton("Got It")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        



class MainWindow(QMainWindow):
    
    def __init__(self, app):
        
        super().__init__()
        
        #Create a settings manager object - handles all settings needs
        self.settings_manager = SettingsManager(app)
        
        #Create the audio engine
        self.audio_player = AudioPlayer(self.settings_manager)
        
        self.setWindowTitle(f"Tower of Babel 2.0")
        self.setMinimumSize(QSize(1500, 500))
        
        
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
        
        
        self.settings_view = SettingsView(self.settings_manager)
        self.edit_view = EditView(self.settings_manager, self.audio_player)
        
        # Add views onto the stack
        self.stacked_widget.addWidget(self.home_view)       # Index 0
        self.stacked_widget.addWidget(self.settings_view)   # Index 1
        self.stacked_widget.addWidget(self.edit_view)       # Index 2
        
        self.stacked_widget_indexes = {self.home_view: 0, self.settings_view: 1, self.edit_view: 2}
        
        
        self.stacked_widget.setCurrentIndex(self.stacked_widget_indexes[self.home_view])
        self.stacked_widget.currentChanged.connect(self._on_tab_changed)


    def _on_tab_changed(self, index):

        """
        Automatically refreshes the view 
        """

        if index == self.stacked_widget_indexes[self.home_view]:
            self.home_view.load_sounds()

        elif index == self.stacked_widget_indexes[self.edit_view]:
            self.edit_view.load_sounds()
        
        
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
        
        spacer = QWidget()
        spacer.setFixedSize(200, 0)
        
        
        #Home Button (switches the stacked layout index to 0)
        home_action = QAction("Home", self)
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget_indexes[self.home_view]))
        toolbar.addAction(home_action)
        
        #Settings Button (Switches to Index 1)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget_indexes[self.settings_view]))
        toolbar.addAction(settings_action)

        edit_action = QAction("Edit Files", self)
        edit_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget_indexes[self.edit_view]))
        toolbar.addAction(edit_action)
        
        toolbar.addSeparator()
        
        setup_guide_action = QAction("Setup Guide", self)
        setup_guide_action.triggered.connect(self._show_setup_guide)
        
        toolbar.addAction(setup_guide_action)
        toolbar.addSeparator()
        
        #Add File(s) Button
        add_files_action = QAction("Add File(s)", self)
        add_files_action.triggered.connect(self._add_files)
        toolbar.addAction(add_files_action)
        
        #Stop Sound(s) Button
        stop_sounds_action = QAction("Stop Sound(s)", self)
        stop_sounds_action.triggered.connect(self.audio_player.stop)
        toolbar.addAction(stop_sounds_action)
        
        toolbar.addSeparator()
        toolbar.addWidget(spacer)
        
        #Continuous Play Checkbox
        spam_play_checkbox = QCheckBox("Continuous Playback", self)
        spam_play_checkbox.checkStateChanged.connect(self._on_checkbox_changed)
        toolbar.addWidget(spam_play_checkbox)
        
        
        #Current Sound Volume Slider
        volume_label = QAction("Volume", self)
        volume_label.setDisabled(True)
        toolbar.addAction(volume_label)
        
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(1, 100)
        volume_slider.setSingleStep(1)
        volume_slider.setValue(self.settings_manager.settings.get("volume")*100)
        volume_slider.setFixedWidth(250)
        volume_slider.valueChanged.connect(self._set_volume)
        
        toolbar.addWidget(volume_slider)
        
        
    def _on_checkbox_changed(self, state):
        
        print(f"Checkbox Changed to state: {state}, settings: {self.settings_manager.settings.get("spam_play")}")
        
        if state == Qt.CheckState.Checked:
            self.settings_manager.settings["spam_play"] = True
            
        elif state == Qt.CheckState.Unchecked:
            self.settings_manager.settings["spam_play"] = False
            
    
    def _set_volume(self, value):
        
        self.settings_manager.settings["volume"] = value / 100
        self.home_view.load_sounds()
         
        
    def _show_setup_guide(self):
        
        """
        Opens the Discord setup Instructions popup
        """
        
        dialog = SetupGuideDialog(self)
        dialog.show()
            
    
        
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
        
        
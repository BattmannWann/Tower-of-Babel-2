# Tower of Babel 2 - Soundboard

Welcome to the Tower of Babel 2 soundboard!

This app provides a fully functional soundboard with full microphone audio routing capabilities. Compared to other apps that are paywalled or provide limited sound playback, this application is completely free AND open-source!

---

## Features

More specifically, this app provides the following core features, where users can:

- Add sound files which appear as clickable buttons 
- Edit the added sound files:

    - Rename: Only edits the apps copy of the filename
    - Trim: Edits the apps copy of the segment of audio the user wishes to play 
    - Trim - Revert: After trimming, allows the user to revert the sound back to its original state
    - Change Icon: Set the icon for the sound's button
    - Delete: Remove the app's copy of the sound from the soundboard

- Stop sounds that are currently playing

- Get detailed setup information through a moveable popup which can be viewed during the process

- Customise the app through the `Settings` page:

    - Change the username for the user (updated on application restart)
    - Set the Default Volume of the sounds that are played (changes the VOLUME OF THE SOUND ITSELF and not the system's volume)
    - Configure the Primary Output device for the sound to be played through (e.g., headphones)
    - Configure the Secondary Output device for the sound to be played through (e.g., the Virtual Audio Cable device)
    - Change the application's theme (updated on application restart)

---

## User Guide

The following link takes you to the WIKI page which provides an in-depth, step-by-step usage of this application:

[Wiki Link](https://github.com/BattmannWann/Tower-of-Babel-2/wiki)

---

## Directory Structure

```

Tower-Of-Babel-2/
├── resources/
│   ├── icons
│   │   └── cassette.png                    # The app's icon 
│   │
│   └── themes/                             # Stores all the themes for the app (`.qss` files)
│       ├── Dark_Theme.qss                  # Dark theme for the app
│       ├── Dracula_Theme.qss               # Fun theme based on stereotypical colours associated with Dracula 
│       ├── Light Theme                     # Light theme for the app, based on blue colours on a white background 
│       └── TheNothing_Theme                # The default, bare-bones application theme
│   
│
├── legacy/                                 # The old codebase, for which features were taken reference from for this revamp
│
├── src/
│   │
│   ├── core/                                  
│   │   ├── __init__.py                     # Allows Python to find this module
│   │   ├── audio_player.py                 # Class responsible for handling the playing of audio
│   │   ├── settings_manager.py             # Class responsible for storing and passing application settings and default file paths
│   │   └── utils.py                        # Convenience methods class file, used throughout the application          
│   │ 
│   ├── ui/                                  
│   │   ├── __init__.py                     # Allows Python to find this module
│   │   ├── edit_view.py                    # The widget view for the `Edit Files` page
│   │   ├── home_view.py                    # The widget view for the `Home` page
│   │   ├── main_window.py                  # The widget that holds/manages the whole application, changing pages through a stacked layout widget
│   │   └── settings_view.py                # The widget view for the `Settings` page
│   │
│   └── main.py                             # The Python script which instantiates the main_window widget and begins execution           
│
├── .gitignore                              # Files that the VC system should ignore
├── LICENSE                                 # Details the license associated to this project (MIT License)
├── README.md                               # Project overview
├── requirements.txt                        # Dependencies list (pip)
└── setup.iss                               # The `iss` file used to create the install wizard through `Inno Setup` 
                                              Not needed unless you want to create your own install wizard,
                                              has been kept in regard to development transparency            

```
---


## Build Instructions

This section details three methods of local building:

1. Running the Python file directly
2. Creating an executable (`.exe`) through the commandline
3. Downloading the application install wizard, along with all of its dependencies

---

### 1. Running Python Files

This application has been designed to run through a single file, through a modular codebase.

To run the application:

- Ensure that you have created and activated a virtual environment
- Ensure that you have installed the application's dependencies
- Ensure that you are at the project root directory

For example:

```bash
$ python3 -m venv venv_tob3/
$ source venv_tob3/bin/active # or .\venv_tob3\Scripts\activate on powershell

$ cd Tower-Of-Babel-2/
$ pip install -r requirements.txt

```

Then, issue the following command:

`python src/main.py`


### 2. Creating an Executable

If you want to build the application into an executable locally, go to the root directory and issue the following command:

`pyinstaller --noconsole --onefile --windowed --add-data "resources;resources" src/main.py`

> *Note If you do not have `pyinstaller` already installed, run: `pip install pyinstaller` inside your virtual environment*

Then, once the script has finished:

- Navigate to the `dist/` folder created in the project directory
- Double click on the executable if using a file manager or type `main.exe` in the command line


### 3. Install Wizard

Download the installation wizard found on the [release page](https://github.com/BattmannWann/Tower-of-Babel-2/releases/tag/v1.0.0) and follow the installation instructions.


### VB-Cable 

To route audio through your microphone, you MUST install the [`VB-Cable`](https://vb-audio.com/Cable/), or similar, virtual audio cable drivers, and follow the application's setup guide page. This comes alongside the install wizard setup, as part of the dependencies.

---

## Support

I am more than happy to discuss this project and take suggestions, comments, or issues related.

Please raise an issue through the [issues page](https://github.com/BattmannWann/Tower-of-Babel-2/issues) or send me an email at `battmannwann@gmail.com. 

---

## Acknowledgements

This project has been developed using the [`PySide6`](https://pypi.org/project/PySide6/) Python library, packaged through the [`PyInstaller`](https://pypi.org/project/pyinstaller/) library, and installation wizard created using [`Inno Setup`](https://jrsoftware.org/isinfo.php), thus all rights go rightfully to them. 

I have ensured to follow the associated rights agreements and by keeping this project open source, taking no monetary gains, I aim and are upholding those agreements.

---

## Project Status

The project is currently on its first release, with the core, basic feature set outlined in the `Features section`
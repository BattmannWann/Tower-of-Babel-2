from cx_Freeze import setup, Executable

build_options = {
    "packages": ["PySide6", "superqt", "sounddevice", "soundfile", "mutagen", "numpy"],
    "include_files": [
        ("fonts", "fonts"),
        ("media", "media"),
        ("themes", "themes"),
    ],
}

setup(
    name="TowerOfBabel2",
    version="1.0",
    description="Soundboard",
    options={"build_exe": build_options},
    executables=[Executable("tower_of_babel2.py", base="Win32GUI", icon="./media/images/cassette.ico")],
)

[Setup]
AppName=Tower of Babel 2
AppVersion=1.0
DefaultDirName={pf}\Tower of Babel 2
DefaultGroupName=Tower of Babel 2
OutputBaseFilename=TowerOfBabel2Installer
Compression=lzma
SolidCompression=yes
SetupIconFile="media\images\cassette.ico"


[Files]
Source: "build\exe.win-amd64-3.13\*"; DestDir: "{app}"; Flags: recursesubdirs
Source:  "media\images\cassette.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Tower of Babel 2"; Filename: "{app}\tower_of_babel2.exe"
Name: "{commondesktop}\Tower of Babel 2"; Filename: "{app}\tower_of_babel2.exe"; IconFilename: "{app}\cassette.ico"

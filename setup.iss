[Setup]
AppName=Tower of Babel
AppVersion=2.0
DefaultDirName={autopf}\Tower of Babel
DefaultGroupName=Tower of Babel
OutputDir=userdocs:Inno Setup Output
OutputBaseFilename=TowerOfBabel_Installer
Compression=lzma
SolidCompression=yes

; Require admin rights to install the VB-Cable driver silently
PrivilegesRequired=admin

; Setup Icon (Point this to the .ico file location)
SetupIconFile=C:\Users\rhysi\Documents\Projects\Tower of Babel 2\Tower-of-Babel-2\legacy\media\images\cassette.ico

[Files]
; 1. COMPILED APP (Point this to the dist/ folder)
Source: "C:\Users\rhysi\Documents\Projects\Tower of Babel 2\Tower-of-Babel-2\dist\main.exe"; DestDir: "{app}"; DestName: "TowerOfBabel.exe"; Flags: ignoreversion

; 2. THE VB-CABLE DRIVER (Grab the ENTIRE folder using the * wildcard)
Source: "C:\Users\rhysi\Downloads\VBCABLE_Driver_Pack45\*"; DestDir: "{tmp}\VBCABLE"; Flags: ignoreversion recursesubdirs deleteafterinstall

; 3. APP ICON
Source: "C:\Users\rhysi\Documents\Projects\Tower of Babel 2\Tower-of-Babel-2\legacy\media\images\cassette.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Tower of Babel"; Filename: "{app}\TowerOfBabel.exe"
Name: "{autodesktop}\Tower of Babel"; Filename: "{app}\TowerOfBabel.exe"; Tasks: desktopicon; IconFilename: "{app}\cassette.ico"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
; Silently install the audio cable BEFORE opening the app (Update path to the new VBCABLE temp folder)
Filename: "{tmp}\VBCABLE\VBCABLE_Setup_x64.exe"; Parameters: "-i -h"; Flags: waituntilterminated runhidden

; Launch the app
Filename: "{app}\TowerOfBabel.exe"; Description: "Launch Tower of Babel"; Flags: nowait postinstall skipifsilent
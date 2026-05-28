; Inno Setup script for Poopee Desktop Pet
; Build dist\PoopeePet first (run build_windows.bat), then compile this with Inno Setup.
; Download Inno Setup: https://jrsoftware.org/isinfo.php

#define AppName "Poopee Desktop Pet"
#define AppVersion "1.0.0"
#define AppPublisher "endlesszotk"
#define AppExeName "PoopeePet.exe"
#define SourceDir "dist\PoopeePet"

[Setup]
AppId={{B3A1C2D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=installer_output
OutputBaseFilename=PoopeePet_Setup_v{#AppVersion}
SetupIconFile=
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";   Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
Name: "startupentry";  Description: "Start Poopee with Windows";  GroupDescription: "Startup:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}";    Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall";     Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
  ValueType: string; ValueName: "PoopeePet"; \
  ValueData: """{app}\{#AppExeName}"""; \
  Flags: uninsdeletevalue; Tasks: startupentry

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch Poopee Desktop Pet"; \
  Flags: nowait postinstall skipifsilent

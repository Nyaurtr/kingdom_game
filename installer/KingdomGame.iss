; Kingdom Game Installer Script for Inno Setup
; This creates a professional installer that helps avoid malware detection

#define MyAppName "Kingdom Game"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Kingdom Game Studio"
#define MyAppURL "https://github.com/yourusername/kingdom-game"
#define MyAppExeName "KingdomGame.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.txt
OutputDir=installer_output
OutputBaseFilename=KingdomGame_Setup_v{#MyAppVersion}
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "KingdomGame_Portable\KingdomGame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "KingdomGame_Portable\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "KingdomGame_Portable\WINDOWS_DEFENDER_GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "KingdomGame_Portable\CODE_SIGNING_GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create a registry entry to help with Windows Defender
    RegWriteStringValue(HKEY_CURRENT_USER, 'Software\KingdomGame', 'InstallPath', ExpandConstant('{app}'));
    RegWriteStringValue(HKEY_CURRENT_USER, 'Software\KingdomGame', 'Version', '{#MyAppVersion}');
    RegWriteStringValue(HKEY_CURRENT_USER, 'Software\KingdomGame', 'Publisher', '{#MyAppPublisher}');
  end;
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if Windows Defender is running and show warning
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows Defender') then
  begin
    if MsgBox('Windows Defender is detected on your system.' + #13#10 + 
              'Kingdom Game may be flagged as a false positive.' + #13#10 + #13#10 +
              'After installation, please add the game folder to Windows Defender exclusions.' + #13#10 +
              'A guide will be provided in the installation folder.' + #13#10 + #13#10 +
              'Do you want to continue with the installation?', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Clean up registry entries
    RegDeleteKeyIncludingSubkeys(HKEY_CURRENT_USER, 'Software\KingdomGame');
  end;
end;

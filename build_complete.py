#!/usr/bin/env python3
"""
Complete Build Script for Kingdom Game Portable Edition
This script handles the entire process from source to distribution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_step(step_num, total_steps, description):
    """Print a formatted step"""
    print(f"\n[{step_num}/{total_steps}] {description}")
    print("-" * 40)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required!")
        return False
    
    print(f"Python version: {sys.version}")
    return True

def install_build_dependencies():
    """Install required build dependencies"""
    print("Installing build dependencies...")
    
    dependencies = ["pyinstaller"]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} is already installed")
        except ImportError:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} installed successfully")

def clean_build_directories():
    """Clean previous build artifacts"""
    print("Cleaning build directories...")
    
    dirs_to_clean = [
        "kingdom_game/build",
        "kingdom_game/dist", 
        "kingdom_game/__pycache__",
        "KingdomGame_Portable",
        "installer/installer_output",
        "distribution"
    ]
    
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"✓ Cleaned {dir_path}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Change to kingdom_game directory
    os.chdir('kingdom_game')
    
    # Create spec file
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/core/evidence_pools', 'src/core/evidence_pools'),
        ('src/core/game_config.py', 'src/core'),
        ('src/core/game_state.py', 'src/core'),
        ('src/core/investigation.py', 'src/core'),
        ('src/core/preparation_system.py', 'src/core'),
        ('src/core/random_event_system.py', 'src/core'),
        ('src/core/resource_system.py', 'src/core'),
        ('src/core/role_system.py', 'src/core'),
        ('src/core/content_system.py', 'src/core'),
        ('src/ui/gui.py', 'src/ui'),
        ('src/main.py', 'src'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PIL', 'Pillow', 'matplotlib', 'numpy', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KingdomGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('kingdom_game.spec', 'w') as f:
        f.write(spec_content)
    
    # Build executable
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "kingdom_game.spec"]
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_portable_package():
    """Create portable package"""
    print("Creating portable package...")
    
    # Go back to root directory
    os.chdir('..')
    
    # Create portable directory
    portable_dir = Path("KingdomGame_Portable")
    portable_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path("kingdom_game/dist/KingdomGame.exe")
    exe_dest = portable_dir / "KingdomGame.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print("✓ Copied executable")
    else:
        print("✗ Executable not found!")
        return False
    
    # Create README for portable version
    readme_content = """# Kingdom Game - Portable Edition

## Cách chạy game:
1. Double-click vào file "KingdomGame.exe"
2. Game sẽ tự động khởi động mà không cần cài đặt Python

## Thông tin game:
- Kingdom Game Version 3.0 - Narrative Investigation Game
- Game điều tra vương quốc thời trung cổ với 3 vai trò: Vua, Đội trưởng, hoặc Gián điệp
- Giải quyết khủng hoảng vương quốc trong 7 ngày
- Không cần cài đặt Python hoặc dependencies

## Hệ thống yêu cầu:
- Windows 7/8/10/11 (64-bit)
- Không cần cài đặt thêm phần mềm nào

## Lưu ý về Windows Defender:
File này có thể bị Windows Defender cảnh báo vì không có chữ ký số. 
Đây là hiện tượng "false positive" phổ biến với các ứng dụng độc lập.

## Cách thêm vào Windows Defender Exclusion:
1. Mở Windows Security
2. Vào Virus & threat protection
3. Chọn Manage settings trong Virus & threat protection settings
4. Chọn Add or remove exclusions
5. Thêm thư mục chứa game này vào danh sách exclusion

## Xác minh game an toàn:
- Game này chỉ sử dụng các module built-in của Python
- Không có kết nối mạng hoặc truy cập file hệ thống
- Mã nguồn có thể được kiểm tra tại GitHub repository

Chúc bạn chơi game vui vẻ!
"""
    
    readme_path = portable_dir / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ Created portable package")
    return True

def create_installer_files():
    """Create installer files"""
    print("Creating installer files...")
    
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Create Inno Setup script
    iss_content = '''; Kingdom Game Installer Script for Inno Setup

#define MyAppName "Kingdom Game"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Kingdom Game Studio"
#define MyAppURL "https://github.com/yourusername/kingdom-game"
#define MyAppExeName "KingdomGame.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.txt
OutputDir=installer_output
OutputBaseFilename=KingdomGame_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "KingdomGame_Portable\\KingdomGame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "KingdomGame_Portable\\README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{group}\\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
'''
    
    with open(installer_dir / "KingdomGame.iss", 'w') as f:
        f.write(iss_content)
    
    # Create LICENSE.txt
    license_content = """Kingdom Game - Medieval Investigation Game

Copyright (C) 2024 Kingdom Game Studio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open(installer_dir / "LICENSE.txt", 'w') as f:
        f.write(license_content)
    
    # Create README.txt for installer
    readme_content = """# Kingdom Game - Medieval Investigation Game

## Giới thiệu
Kingdom Game là một game điều tra thời trung cổ nơi bạn sẽ đóng vai một trong ba vai trò: Vua, Đội trưởng, hoặc Gián điệp để giải quyết khủng hoảng vương quốc trong 7 ngày.

## Tính năng chính
- **3 vai trò độc đáo**: Mỗi vai trò có khả năng và bí mật riêng
- **8 sự kiện khủng hoảng**: Từ nạn đói đến cuộc nổi dậy siêu nhiên
- **Hệ thống điều tra**: Thu thập bằng chứng từ các nguồn khác nhau
- **Quản lý tài nguyên**: Sử dụng tài nguyên một cách chiến lược
- **Sự kiện ngẫu nhiên**: Các sự kiện bất ngờ ảnh hưởng đến trò chơi
- **Kết thúc đa dạng**: Kết quả phụ thuộc vào hành động của bạn

## Hệ thống yêu cầu
- Windows 7/8/10/11 (64-bit)
- Không cần cài đặt Python hoặc dependencies

## Cách chơi
1. Khởi động game và được gán vai trò ngẫu nhiên
2. Điều tra để thu thập bằng chứng về khủng hoảng sắp tới
3. Sử dụng tài nguyên để chuẩn bị đối phó với khủng hoảng
4. Tiến hành qua 7 ngày (21 lượt hành động)
5. Xem kết quả dựa trên mức độ chuẩn bị của bạn

## Lưu ý về Windows Defender
Game này có thể bị Windows Defender cảnh báo vì không có chữ ký số. Đây là hiện tượng "false positive" phổ biến với các ứng dụng độc lập. Vui lòng tham khảo file README.txt trong thư mục cài đặt để biết cách thêm game vào danh sách ngoại lệ.

Chúc bạn chơi game vui vẻ!
"""
    
    with open(installer_dir / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ Created installer files")
    return True

def create_distribution_package():
    """Create final distribution package"""
    print("Creating distribution package...")
    
    dist_dir = Path("distribution")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy portable version
    portable_dir = Path("KingdomGame_Portable")
    if portable_dir.exists():
        shutil.copytree(portable_dir, dist_dir / "KingdomGame_Portable", dirs_exist_ok=True)
        print("✓ Copied portable version")
    
    # Create ZIP of portable version
    try:
        import zipfile
        zip_name = dist_dir / "KingdomGame_Portable_v1.0.0.zip"
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(portable_dir.parent)
                    zipf.write(file_path, arcname)
        
        print("✓ Created portable ZIP")
    except Exception as e:
        print(f"✗ Failed to create ZIP: {e}")
    
    # Create distribution README
    dist_readme = """# Kingdom Game - Distribution Package

## Files included:
- KingdomGame_Portable/: Portable version folder
- KingdomGame_Portable_v1.0.0.zip: Portable version ZIP file

## Installation Options:

### Option 1: Portable Version (Recommended)
1. Extract KingdomGame_Portable_v1.0.0.zip to any folder
2. Run KingdomGame.exe directly
3. No installation required

### Option 2: Folder Version
1. Copy KingdomGame_Portable folder to desired location
2. Run KingdomGame.exe directly
3. No installation required

## Windows Defender Notes:
The game may trigger Windows Defender warnings. This is normal for unsigned executables.
Please refer to the README.txt file included with the game for instructions on adding it to exclusions.

## System Requirements:
- Windows 7/8/10/11 (64-bit)
- No additional software required

## Game Features:
- Medieval investigation game
- 3 unique roles: King, Captain, or Spy
- 8 different crisis events
- Resource management system
- Random events
- Multiple endings based on your choices

## Support:
- GitHub: https://github.com/yourusername/kingdom-game
- Email: support@kingdomgame.com

Enjoy playing Kingdom Game!
"""
    
    with open(dist_dir / "DISTRIBUTION_README.txt", 'w', encoding='utf-8') as f:
        f.write(dist_readme)
    
    print("✓ Created distribution package")
    return True

def main():
    """Main build process"""
    print_header("Kingdom Game - Complete Portable Build")
    
    total_steps = 7
    
    try:
        # Step 1: Check Python version
        print_step(1, total_steps, "Checking Python version")
        if not check_python_version():
            return False
        
        # Step 2: Install dependencies
        print_step(2, total_steps, "Installing build dependencies")
        install_build_dependencies()
        
        # Step 3: Clean build directories
        print_step(3, total_steps, "Cleaning build directories")
        clean_build_directories()
        
        # Step 4: Build executable
        print_step(4, total_steps, "Building executable")
        if not build_executable():
            return False
        
        # Step 5: Create portable package
        print_step(5, total_steps, "Creating portable package")
        if not create_portable_package():
            return False
        
        # Step 6: Create installer files
        print_step(6, total_steps, "Creating installer files")
        create_installer_files()
        
        # Step 7: Create distribution package
        print_step(7, total_steps, "Creating distribution package")
        create_distribution_package()
        
        print_header("BUILD COMPLETED SUCCESSFULLY!")
        print("""
✓ Executable built successfully
✓ Portable package created
✓ Installer files prepared
✓ Distribution package ready

Distribution files are available in the 'distribution/' folder:
- KingdomGame_Portable/: Portable version folder
- KingdomGame_Portable_v1.0.0.zip: Portable ZIP file
- DISTRIBUTION_README.txt: Instructions for users

You can now distribute these files to users!
The game runs without requiring Python installation.
""")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

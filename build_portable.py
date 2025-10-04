#!/usr/bin/env python3
"""
Build script for Kingdom Game Portable Edition
Creates a standalone executable that doesn't require Python installation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for better control"""
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
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
)
'''
    
    with open('kingdom_game.spec', 'w') as f:
        f.write(spec_content)
    print("Created kingdom_game.spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Kingdom Game executable...")
    
    # Change to kingdom_game directory
    os.chdir('kingdom_game')
    
    # Build using spec file
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "../kingdom_game.spec"]
    
    try:
        subprocess.check_call(cmd)
        print("Build completed successfully!")
        print("Executable created in: kingdom_game/dist/KingdomGame.exe")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    
    return True

def create_portable_package():
    """Create a portable package with the executable and necessary files"""
    print("Creating portable package...")
    
    # Create portable directory
    portable_dir = Path("../KingdomGame_Portable")
    portable_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path("dist/KingdomGame.exe")
    exe_dest = portable_dir / "KingdomGame.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"Copied executable to {exe_dest}")
    else:
        print("Executable not found!")
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

## Lưu ý:
- File này đã được đóng gói để chạy độc lập
- Windows Defender có thể cảnh báo vì đây là file executable không có chữ ký số
- Để tránh cảnh báo, bạn có thể thêm file vào danh sách ngoại lệ của Windows Defender

## Cách thêm vào Windows Defender Exclusion:
1. Mở Windows Security
2. Vào Virus & threat protection
3. Chọn Manage settings trong Virus & threat protection settings
4. Chọn Add or remove exclusions
5. Thêm thư mục chứa game này vào danh sách exclusion

Chúc bạn chơi game vui vẻ!
"""
    
    readme_path = portable_dir / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Created portable package in: {portable_dir}")
    return True

def main():
    """Main build process"""
    print("=" * 60)
    print("Kingdom Game - Portable Edition Builder")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('kingdom_game'):
        print("Error: kingdom_game directory not found!")
        print("Please run this script from the project root directory.")
        return False
    
    try:
        # Step 1: Install PyInstaller
        install_pyinstaller()
        
        # Step 2: Create spec file
        create_spec_file()
        
        # Step 3: Build executable
        if not build_executable():
            return False
        
        # Step 4: Create portable package
        if not create_portable_package():
            return False
        
        print("\n" + "=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Portable game created in: KingdomGame_Portable/")
        print("Executable: KingdomGame_Portable/KingdomGame.exe")
        print("\nYou can now distribute the entire KingdomGame_Portable folder.")
        print("Users just need to run KingdomGame.exe to play!")
        
        return True
        
    except Exception as e:
        print(f"Build failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

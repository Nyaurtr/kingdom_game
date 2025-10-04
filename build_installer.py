#!/usr/bin/env python3
"""
Installer Build Script for Kingdom Game
Creates a professional installer using Inno Setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_inno_setup():
    """Check if Inno Setup is installed"""
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe"
    ]
    
    for path in inno_paths:
        if os.path.exists(path):
            print(f"Found Inno Setup at: {path}")
            return path
    
    print("Inno Setup not found!")
    print("Please install Inno Setup from: https://jrsoftware.org/isinfo.php")
    print("Or download the portable version.")
    return None

def create_installer():
    """Create the installer using Inno Setup"""
    inno_path = check_inno_setup()
    if not inno_path:
        return False
    
    # Change to installer directory
    installer_dir = Path("installer")
    if not installer_dir.exists():
        print("Installer directory not found!")
        return False
    
    os.chdir(installer_dir)
    
    # Build installer
    script_file = "KingdomGame.iss"
    if not os.path.exists(script_file):
        print(f"Script file {script_file} not found!")
        return False
    
    cmd = [inno_path, script_file]
    
    try:
        print("Building installer...")
        subprocess.check_call(cmd)
        print("Installer built successfully!")
        
        # Check if installer was created
        output_dir = Path("installer_output")
        if output_dir.exists():
            installer_files = list(output_dir.glob("*.exe"))
            if installer_files:
                installer_file = installer_files[0]
                print(f"Installer created: {installer_file}")
                return True
        
        print("Installer file not found in output directory!")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"Installer build failed: {e}")
        return False

def create_portable_zip():
    """Create a portable ZIP version as alternative"""
    print("Creating portable ZIP version...")
    
    portable_dir = Path("../KingdomGame_Portable")
    if not portable_dir.exists():
        print("Portable directory not found!")
        return False
    
    zip_name = "KingdomGame_Portable_v1.0.0.zip"
    
    try:
        import zipfile
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(portable_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"Portable ZIP created: {zip_name}")
        return True
        
    except Exception as e:
        print(f"Failed to create ZIP: {e}")
        return False

def create_distribution_package():
    """Create complete distribution package"""
    print("Creating distribution package...")
    
    dist_dir = Path("distribution")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy installer
    installer_output = Path("installer_output")
    if installer_output.exists():
        installer_files = list(installer_output.glob("*.exe"))
        if installer_files:
            shutil.copy2(installer_files[0], dist_dir / installer_files[0].name)
            print(f"Copied installer to distribution folder")
    
    # Copy portable ZIP
    zip_files = list(Path(".").glob("*.zip"))
    for zip_file in zip_files:
        shutil.copy2(zip_file, dist_dir / zip_file.name)
        print(f"Copied {zip_file.name} to distribution folder")
    
    # Create distribution README
    dist_readme = """# Kingdom Game - Distribution Package

## Files included:
- KingdomGame_Setup_v1.0.0.exe: Professional installer (recommended)
- KingdomGame_Portable_v1.0.0.zip: Portable version (no installation required)

## Installation Options:

### Option 1: Professional Installer (Recommended)
1. Run KingdomGame_Setup_v1.0.0.exe
2. Follow the installation wizard
3. Game will be installed to Program Files
4. Desktop shortcut will be created

### Option 2: Portable Version
1. Extract KingdomGame_Portable_v1.0.0.zip to any folder
2. Run KingdomGame.exe directly
3. No installation required

## Windows Defender Notes:
Both versions may trigger Windows Defender warnings. This is normal for unsigned executables.
Please refer to the Windows Defender guide included with the game.

## System Requirements:
- Windows 7/8/10/11 (64-bit)
- No additional software required

## Support:
- GitHub: https://github.com/yourusername/kingdom-game
- Email: support@kingdomgame.com

Enjoy playing Kingdom Game!
"""
    
    with open(dist_dir / "DISTRIBUTION_README.txt", 'w', encoding='utf-8') as f:
        f.write(dist_readme)
    
    print(f"Distribution package created in: {dist_dir}")
    return True

def main():
    """Main installer build process"""
    print("=" * 60)
    print("Kingdom Game - Installer Builder")
    print("=" * 60)
    
    try:
        # Create installer
        installer_success = create_installer()
        
        # Create portable ZIP
        zip_success = create_portable_zip()
        
        # Create distribution package
        if installer_success or zip_success:
            create_distribution_package()
        
        print("\n" + "=" * 60)
        print("BUILD COMPLETED!")
        print("=" * 60)
        
        if installer_success:
            print("✓ Professional installer created")
        else:
            print("✗ Installer creation failed")
        
        if zip_success:
            print("✓ Portable ZIP created")
        else:
            print("✗ ZIP creation failed")
        
        print("\nDistribution files are ready in the distribution/ folder")
        print("You can now distribute these files to users!")
        
        return True
        
    except Exception as e:
        print(f"Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

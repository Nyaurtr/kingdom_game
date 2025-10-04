#!/usr/bin/env python3
"""
Digital Signature Script for Kingdom Game
Helps avoid false positive malware detection by Windows Defender
"""

import os
import sys
import subprocess
import hashlib
from pathlib import Path

def create_manifest_file():
    """Create application manifest to help with Windows compatibility"""
    manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="*"
    name="KingdomGame"
    type="win32"
  />
  <description>Kingdom Game - Medieval Investigation Game</description>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
        type="win32"
        name="Microsoft.Windows.Common-Controls"
        version="6.0.0.0"
        processorArchitecture="*"
        publicKeyToken="6595b64144ccf1df"
        language="*"
      />
    </dependentAssembly>
  </dependency>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="asInvoker" uiAccess="false" />
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <!-- Windows 7 -->
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
      <!-- Windows 8 -->
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
      <!-- Windows 8.1 -->
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>
      <!-- Windows 10 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
    </application>
  </compatibility>
</assembly>'''
    
    manifest_path = Path("KingdomGame_Portable/KingdomGame.exe.manifest")
    with open(manifest_path, 'w') as f:
        f.write(manifest_content)
    
    print(f"Created manifest file: {manifest_path}")
    return manifest_path

def create_version_info():
    """Create version information file"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined.
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Kingdom Game Studio'),
        StringStruct(u'FileDescription', u'Kingdom Game - Medieval Investigation Game'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'KingdomGame'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024 Kingdom Game Studio'),
        StringStruct(u'OriginalFilename', u'KingdomGame.exe'),
        StringStruct(u'ProductName', u'Kingdom Game'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    version_path = Path("version_info.txt")
    with open(version_path, 'w') as f:
        f.write(version_info)
    
    print(f"Created version info file: {version_path}")
    return version_path

def update_spec_with_signature():
    """Update the spec file to include manifest and version info"""
    spec_file = Path("kingdom_game.spec")
    if not spec_file.exists():
        print("Spec file not found. Please run build_portable.py first.")
        return False
    
    # Read current spec
    with open(spec_file, 'r') as f:
        spec_content = f.read()
    
    # Add version info and manifest
    updated_spec = spec_content.replace(
        'icon=None,  # Add icon file path here if you have one',
        '''icon=None,  # Add icon file path here if you have one
    version='version_info.txt',
    manifest='KingdomGame_Portable/KingdomGame.exe.manifest','''
    )
    
    with open(spec_file, 'w') as f:
        f.write(updated_spec)
    
    print("Updated spec file with version info and manifest")
    return True

def create_code_signing_instructions():
    """Create instructions for code signing"""
    instructions = """# Code Signing Instructions for Kingdom Game

## Why Code Signing?
Code signing helps prevent Windows Defender from flagging your executable as malware.
It provides cryptographic proof that the software hasn't been tampered with.

## Free Code Signing Options:

### 1. Self-Signed Certificate (Free but limited)
```bash
# Create self-signed certificate
makecert -r -pe -ss PrivateCertStore -n "CN=Kingdom Game Studio" KingdomGame.cer

# Sign the executable
signtool sign /f KingdomGame.pfx /p password KingdomGame.exe
```

### 2. Let's Encrypt + Certbot (Free)
- Use Let's Encrypt to get a free SSL certificate
- Convert to code signing certificate
- Sign your executable

### 3. Commercial Code Signing (Recommended)
- DigiCert: ~$200-400/year
- Sectigo: ~$200-300/year
- GlobalSign: ~$300-500/year

## Alternative: Windows Defender Exclusion
If you can't afford code signing, users can add your game to Windows Defender exclusions:

1. Open Windows Security
2. Go to Virus & threat protection
3. Click "Manage settings" under Virus & threat protection settings
4. Click "Add or remove exclusions"
5. Add the game folder to exclusions

## Best Practices:
1. Always scan your executable with multiple antivirus engines before distribution
2. Provide clear documentation about what your software does
3. Use a reputable hosting service
4. Consider getting a code signing certificate for professional distribution

## Testing Your Signed Executable:
1. Upload to VirusTotal.com to check detection rates
2. Test on clean Windows machines
3. Monitor user feedback for false positive reports
"""
    
    instructions_path = Path("KingdomGame_Portable/CODE_SIGNING_GUIDE.txt")
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"Created code signing guide: {instructions_path}")

def create_antivirus_whitelist_instructions():
    """Create instructions for users to whitelist the game"""
    whitelist_guide = """# Hướng dẫn thêm Kingdom Game vào danh sách ngoại lệ Windows Defender

## Tại sao Windows Defender cảnh báo?
Windows Defender có thể cảnh báo về Kingdom Game vì:
- Đây là file executable (.exe) không có chữ ký số từ nhà phát triển đã được xác minh
- Windows Defender sử dụng heuristic analysis và có thể nhận diện nhầm game là phần mềm độc hại
- Đây là hiện tượng "false positive" (báo động sai) rất phổ biến với các ứng dụng độc lập

## Cách thêm vào danh sách ngoại lệ:

### Phương pháp 1: Thêm file cụ thể
1. Mở Windows Security (Windows Defender)
2. Vào "Virus & threat protection"
3. Chọn "Manage settings" trong phần "Virus & threat protection settings"
4. Chọn "Add or remove exclusions"
5. Chọn "Add an exclusion" > "File"
6. Duyệt đến file KingdomGame.exe và chọn

### Phương pháp 2: Thêm thư mục (Khuyến nghị)
1. Làm theo bước 1-4 như trên
2. Chọn "Add an exclusion" > "Folder"
3. Chọn toàn bộ thư mục chứa Kingdom Game

### Phương pháp 3: Tạm thời tắt Real-time protection
1. Vào Windows Security
2. Vào "Virus & threat protection"
3. Tắt "Real-time protection" tạm thời
4. Chạy game
5. Bật lại Real-time protection

## Xác minh game an toàn:
- Game này chỉ sử dụng các module built-in của Python
- Không có kết nối mạng hoặc truy cập file hệ thống
- Mã nguồn có thể được kiểm tra tại: [GitHub repository]
- Game đã được quét bằng VirusTotal: [Link sẽ được cung cấp]

## Liên hệ hỗ trợ:
Nếu bạn gặp vấn đề với Windows Defender, vui lòng liên hệ:
- Email: [support email]
- GitHub Issues: [repository link]

Chúc bạn chơi game vui vẻ!
"""
    
    whitelist_path = Path("KingdomGame_Portable/WINDOWS_DEFENDER_GUIDE.txt")
    with open(whitelist_path, 'w', encoding='utf-8') as f:
        f.write(whitelist_guide)
    
    print(f"Created Windows Defender guide: {whitelist_path}")

def main():
    """Main signature preparation process"""
    print("=" * 60)
    print("Kingdom Game - Digital Signature Preparation")
    print("=" * 60)
    
    try:
        # Create manifest file
        create_manifest_file()
        
        # Create version info
        create_version_info()
        
        # Update spec file
        update_spec_with_signature()
        
        # Create code signing instructions
        create_code_signing_instructions()
        
        # Create antivirus whitelist instructions
        create_antivirus_whitelist_instructions()
        
        print("\n" + "=" * 60)
        print("SIGNATURE PREPARATION COMPLETED!")
        print("=" * 60)
        print("Files created:")
        print("- KingdomGame_Portable/KingdomGame.exe.manifest")
        print("- version_info.txt")
        print("- KingdomGame_Portable/CODE_SIGNING_GUIDE.txt")
        print("- KingdomGame_Portable/WINDOWS_DEFENDER_GUIDE.txt")
        print("\nNext steps:")
        print("1. Run build_portable.py again to rebuild with signature info")
        print("2. Consider getting a code signing certificate")
        print("3. Test the executable on clean Windows machines")
        
        return True
        
    except Exception as e:
        print(f"Signature preparation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

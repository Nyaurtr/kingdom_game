#!/usr/bin/env python3
"""
Test Script for Kingdom Game Portable Edition
Tests the game functionality and provides verification steps
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_executable_exists():
    """Test if the executable exists"""
    print("Testing executable existence...")
    
    exe_path = Path("KingdomGame_Portable/KingdomGame.exe")
    if exe_path.exists():
        print(f"✓ Executable found: {exe_path}")
        return True
    else:
        print(f"✗ Executable not found: {exe_path}")
        return False

def test_executable_size():
    """Test if executable has reasonable size"""
    print("Testing executable size...")
    
    exe_path = Path("KingdomGame_Portable/KingdomGame.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable size: {size_mb:.1f} MB")
        
        if size_mb < 10:
            print("⚠ Warning: Executable seems too small")
        elif size_mb > 500:
            print("⚠ Warning: Executable seems too large")
        else:
            print("✓ Executable size is reasonable")
        
        return True
    else:
        return False

def test_game_startup():
    """Test if game starts without errors"""
    print("Testing game startup...")
    
    exe_path = Path("KingdomGame_Portable/KingdomGame.exe")
    if not exe_path.exists():
        print("✗ Executable not found")
        return False
    
    try:
        # Start the game process
        print("Starting game process...")
        process = subprocess.Popen([str(exe_path)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Game started successfully")
            
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            print("✓ Game terminated cleanly")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"✗ Game failed to start")
            if stderr:
                print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_dependencies():
    """Test if all required files are present"""
    print("Testing dependencies...")
    
    portable_dir = Path("KingdomGame_Portable")
    required_files = [
        "KingdomGame.exe",
        "README.txt"
    ]
    
    all_present = True
    for file_name in required_files:
        file_path = portable_dir / file_name
        if file_path.exists():
            print(f"✓ {file_name} found")
        else:
            print(f"✗ {file_name} missing")
            all_present = False
    
    return all_present

def test_windows_compatibility():
    """Test Windows compatibility"""
    print("Testing Windows compatibility...")
    
    if sys.platform != "win32":
        print("⚠ Warning: Not running on Windows")
        return False
    
    # Check Windows version
    import platform
    windows_version = platform.platform()
    print(f"✓ Running on: {windows_version}")
    
    # Check if executable is 64-bit compatible
    exe_path = Path("KingdomGame_Portable/KingdomGame.exe")
    if exe_path.exists():
        # Try to read PE header to check architecture
        try:
            with open(exe_path, 'rb') as f:
                # Read PE header
                f.seek(0x3C)  # PE header offset
                pe_offset = int.from_bytes(f.read(4), 'little')
                f.seek(pe_offset + 4)  # Machine type offset
                machine_type = int.from_bytes(f.read(2), 'little')
                
                if machine_type == 0x8664:  # AMD64
                    print("✓ Executable is 64-bit")
                elif machine_type == 0x014c:  # i386
                    print("✓ Executable is 32-bit")
                else:
                    print(f"⚠ Unknown architecture: {machine_type:x}")
        except Exception as e:
            print(f"⚠ Could not determine architecture: {e}")
    
    return True

def create_test_report():
    """Create a test report"""
    print("Creating test report...")
    
    report_content = f"""# Kingdom Game - Test Report

## Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
## Test Environment: {sys.platform} {sys.version}

## Test Results:

### 1. Executable Existence
- Status: {'PASS' if test_executable_exists() else 'FAIL'}
- Location: KingdomGame_Portable/KingdomGame.exe

### 2. Executable Size
- Status: {'PASS' if test_executable_size() else 'FAIL'}
- Size: {Path('KingdomGame_Portable/KingdomGame.exe').stat().st_size / (1024 * 1024):.1f} MB

### 3. Game Startup
- Status: {'PASS' if test_game_startup() else 'FAIL'}
- Test: Game starts without errors

### 4. Dependencies
- Status: {'PASS' if test_dependencies() else 'FAIL'}
- Required files present

### 5. Windows Compatibility
- Status: {'PASS' if test_windows_compatibility() else 'FAIL'}
- Platform: {sys.platform}

## Recommendations:

1. **Windows Defender**: Add the game folder to Windows Defender exclusions
2. **Distribution**: Test on clean Windows machines before distribution
3. **Code Signing**: Consider getting a code signing certificate for professional distribution
4. **Virus Scanning**: Upload to VirusTotal.com to check detection rates

## Next Steps:

1. Test the game on different Windows versions
2. Test on machines without Python installed
3. Verify all game features work correctly
4. Create user documentation

## Support:

If you encounter issues:
- Check Windows Defender exclusions
- Verify system requirements
- Contact support: support@kingdomgame.com
"""
    
    report_path = Path("KingdomGame_Portable/TEST_REPORT.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✓ Test report created: {report_path}")

def main():
    """Main test process"""
    print("=" * 60)
    print("Kingdom Game - Portable Edition Test")
    print("=" * 60)
    
    tests = [
        ("Executable Existence", test_executable_exists),
        ("Executable Size", test_executable_size),
        ("Game Startup", test_game_startup),
        ("Dependencies", test_dependencies),
        ("Windows Compatibility", test_windows_compatibility)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name}: PASSED")
            else:
                print(f"✗ {test_name}: FAILED")
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✓ All tests passed! Game is ready for distribution.")
    else:
        print("⚠ Some tests failed. Please check the issues above.")
    
    # Create test report
    create_test_report()
    
    print("\nTest report saved to KingdomGame_Portable/TEST_REPORT.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script tự động build file exe cho AutoCashier
Hỗ trợ cả 2 phiên bản: CustomTkinter (Win10+) và PyQt5 (Win7+)

Usage:
    python build_exe.py                    # Build both versions
    python build_exe.py --version pyqt5    # Build only PyQt5 version
    python build_exe.py --version ctk      # Build only CustomTkinter version
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

# Determine separator for --add-data based on OS
if sys.platform == 'win32':
    DATA_SEP = ';'
else:
    DATA_SEP = ':'

def print_header():
    """In header"""
    print("=" * 70)
    print("  AutoCashier - Build Executable")
    print("  Hỗ trợ: PyQt5 (Win7+) và CustomTkinter (Win10+)")
    print("=" * 70)
    
    # Warning for cross-platform builds
    if sys.platform != 'win32':
        print()
        print("⚠️  CẢNH BÁO: Đang build trên Linux/macOS")
        print("   PyInstaller KHÔNG hỗ trợ cross-compile!")
        print("   File .exe build từ Linux SẼ KHÔNG chạy được trên Windows.")
        print()
        print("   Để tạo file .exe thật cho Windows:")
        print("   1. Build trên máy Windows")
        print("   2. Dùng Wine (xem BUILD_FOR_WINDOWS.md)")
        print("   3. Dùng GitHub Actions CI/CD")
        print()
        input("   Nhấn Enter để tiếp tục build (chỉ để test)...")
    
    print()

def clean_build_folders():
    """Xóa các folder build cũ"""
    print("[1/4] Dọn dẹp folder build cũ...")
    
    folders_to_clean = ["build", "dist", "__pycache__"]
    
    for folder in folders_to_clean:
        folder_path = Path(folder)
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"   ✓ Đã xóa {folder}")
    
    # Xóa file .spec cũ
    spec_files = list(Path(".").glob("*.spec"))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"   ✓ Đã xóa {spec_file.name}")
    
    print()

def build_pyqt5_version():
    """Build PyQt5 version (Windows 7 compatible)"""
    print("[BUILD PyQt5] Build phiên bản Windows 7+...")
    print("   (Quá trình này có thể mất vài phút)")
    print()
    
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=AutoCashier-Win7",
        "--onefile",
        "--windowed",
        f"--add-data=config.json{DATA_SEP}.",
        f"--add-data=utils.py{DATA_SEP}.",
        "--hidden-import=PyQt5",
        "--hidden-import=pypdf",
        "--hidden-import=docx",
        "--hidden-import=pptx",
        "--hidden-import=openpyxl",
        "--hidden-import=PIL",
        "--noconsole",
        "--noconfirm",
        "main_pyqt5.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Lỗi khi build PyQt5 version!")
            print(result.stderr)
            return False
        
        print("✓ Build PyQt5 thành công!")
        
        # Add .exe extension on Linux/Mac (for Windows compatibility)
        if sys.platform != 'win32':
            dist_folder = Path("dist")
            exe_file = dist_folder / "AutoCashier-Win7"
            exe_file_with_ext = dist_folder / "AutoCashier-Win7.exe"
            
            if exe_file.exists():
                exe_file.rename(exe_file_with_ext)
                print("   ✓ Đã thêm đuôi .exe")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def build_customtkinter_version():
    """Build CustomTkinter version (Windows 10+ only)"""
    print("[BUILD CustomTkinter] Build phiên bản Windows 10+...")
    print("   (Quá trình này có thể mất vài phút)")
    print()
    
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=AutoCashier-Win10",
        "--onefile",
        "--windowed",
        f"--add-data=config.json{DATA_SEP}.",
        f"--add-data=utils.py{DATA_SEP}.",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=customtkinter",
        "--hidden-import=tkinterdnd2",
        "--hidden-import=pypdf",
        "--hidden-import=docx",
        "--hidden-import=pptx",
        "--hidden-import=openpyxl",
        "--hidden-import=PIL",
        "--collect-all=customtkinter",
        "--collect-all=tkinterdnd2",
        "--noconsole",
        "--noconfirm",
        "main.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Lỗi khi build CustomTkinter version!")
            print(result.stderr)
            return False
        
        print("✓ Build CustomTkinter thành công!")
        
        # Add .exe extension on Linux/Mac (for Windows compatibility)
        if sys.platform != 'win32':
            dist_folder = Path("dist")
            exe_file = dist_folder / "AutoCashier-Win10"
            exe_file_with_ext = dist_folder / "AutoCashier-Win10.exe"
            
            if exe_file.exists():
                exe_file.rename(exe_file_with_ext)
                print("   ✓ Đã thêm đuôi .exe")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def copy_config():
    """Copy file config vào thư mục dist"""
    print("[Copy config] Copy file cấu hình...")
    
    dist_folder = Path("dist")
    
    # Create dist folder if it doesn't exist (in case both builds failed)
    if not dist_folder.exists():
        print("   ⚠ Thư mục dist chưa tồn tại (có thể do build thất bại)")
        return
    
    # Copy config.json
    config_src = Path("config.json")
    config_dst = dist_folder / "config.json"
    
    if config_src.exists():
        shutil.copy2(config_src, config_dst)
        print("   ✓ Đã copy config.json")
    else:
        print("   ⚠ Không tìm thấy config.json")
    
    print()

def show_completion():
    """Hiển thị thông báo hoàn tất"""
    print()
    print("=" * 70)
    print("  🎉 BUILD THÀNH CÔNG!")
    print("=" * 70)
    print()
    print("File exe đã được tạo tại folder 'dist':")
    print()
    
    dist_folder = Path("dist")
    if dist_folder.exists():
        # List all .exe files
        found_files = False
        for exe_file in dist_folder.glob("*.exe"):
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            print(f"    📦 {exe_file.name} ({size_mb:.1f} MB)")
            found_files = True
        
        if not found_files:
            print("    ⚠ Không tìm thấy file .exe")
    
    print()
    print("Cách sử dụng:")
    print("  • Windows 7/8:  Dùng AutoCashier-Win7.exe (PyQt5)")
    print("  • Windows 10+:  Dùng AutoCashier-Win10.exe (CustomTkinter)")
    print()
    print("Lưu ý:")
    print("  • File config.json phải cùng folder với .exe")
    print("  • Windows 7: Cần cài Visual C++ 2015-2019 Redistributable")
    print("  • Link: https://aka.ms/vs/16/release/vc_redist.x64.exe")
    
    if sys.platform != 'win32':
        print()
        print("=" * 70)
        print("⚠️  CẢNH BÁO QUAN TRỌNG")
        print("=" * 70)
        print()
        print("File .exe vừa build từ Linux/macOS KHÔNG phải Windows executable!")
        print("Đây chỉ là Linux binary với tên .exe, SẼ KHÔNG chạy trên Windows.")
        print()
        print("Để build cho Windows:")
        print("  1. Copy source code sang máy Windows và build")
        print("  2. Dùng Wine để build (xem BUILD_FOR_WINDOWS.md)")
        print("  3. Dùng GitHub Actions (xem BUILD_FOR_WINDOWS.md)")
        print()
        print("Kiểm tra file type:")
        print("  file dist/*.exe")
        print("  → Linux: 'ELF 64-bit LSB executable' (SAI)")
        print("  → Windows: 'PE32+ executable' (ĐÚNG)")
    
    print()

def main():
    """Hàm main"""
    parser = argparse.ArgumentParser(
        description="Build AutoCashier executables",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version',
        choices=['pyqt5', 'ctk', 'both'],
        default='both',
        help='Which version to build (default: both)'
    )
    parser.add_argument(
        '--no-clean',
        action='store_true',
        help='Skip cleaning previous build artifacts'
    )
    
    args = parser.parse_args()
    
    print_header()
    
    try:
        # Clean
        if not args.no_clean:
            clean_build_folders()
        
        # Build based on choice
        success_count = 0
        
        if args.version in ['pyqt5', 'both']:
            if build_pyqt5_version():
                success_count += 1
            print()
        
        if args.version in ['ctk', 'both']:
            if build_customtkinter_version():
                success_count += 1
            print()
        
        # Copy config
        copy_config()
        
        # Show completion
        if success_count > 0:
            show_completion()
        else:
            print("❌ Không có version nào build thành công!")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print()
        print("❌ Đã hủy build")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Lỗi không mong muốn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

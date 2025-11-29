#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script tự động build file exe cho AutoCashier
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """In header"""
    print("=" * 60)
    print("  AutoCashier - Build Executable")
    print("  Tạo file .exe độc lập")
    print("=" * 60)
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

def build_executable():
    """Build file exe bằng PyInstaller"""
    print("[2/4] Build file executable...")
    print("   (Quá trình này có thể mất vài phút)")
    print()
    
    # Lệnh PyInstaller với các tùy chọn
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=AutoCashier",
        "--onefile",
        "--windowed",
        "--add-data=config.json;.",
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
        "--noconfirm",
        "main.py"
    ]
    
    try:
        # Chạy với output để debug
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Lỗi khi build!")
            print()
            print("STDERR:")
            print(result.stderr)
            print()
            print("STDOUT:")
            print(result.stdout)
            sys.exit(1)
        
        print()
        print("✓ Build thành công!")
        print()
    except Exception as e:
        print()
        print(f"❌ Lỗi khi build: {e}")
        sys.exit(1)

def copy_config():
    """Copy file config vào thư mục dist"""
    print("[3/4] Copy file cấu hình...")
    
    dist_folder = Path("dist")
    if not dist_folder.exists():
        print("❌ Không tìm thấy thư mục dist")
        sys.exit(1)
    
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
    print("[4/4] Hoàn tất!")
    print()
    print("=" * 60)
    print("  🎉 BUILD THÀNH CÔNG!")
    print("=" * 60)
    print()
    print("File exe đã được tạo tại:")
    print()
    exe_path = Path("dist") / "AutoCashier.exe"
    print(f"    {exe_path.absolute()}")
    print()
    print("Bạn có thể:")
    print("  1. Double-click file .exe để chạy")
    print("  2. Copy cả folder 'dist' sang máy khác (không cần Python)")
    print("  3. Chỉnh sửa config.json trong folder 'dist' để đổi giá")
    print()
    print("Lưu ý:")
    print("  - Lần đầu chạy có thể hơi lâu (giải nén thư viện)")
    print("  - File exe khoảng 50-100MB (chứa toàn bộ Python runtime)")
    print("  - Windows Defender có thể cảnh báo, chọn 'Run anyway'")
    print()

def main():
    """Hàm main"""
    print_header()
    
    try:
        clean_build_folders()
        build_executable()
        copy_config()
        show_completion()
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

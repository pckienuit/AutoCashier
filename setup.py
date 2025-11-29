#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoCashier Setup Script
Tự động cài đặt dependencies và cấu hình ứng dụng
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    """In header của script"""
    print("=" * 60)
    print("  AutoCashier - Hệ thống tính tiền photocopy tự động")
    print("  Version 1.0.0")
    print("=" * 60)
    print()

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print("[1/5] Kiểm tra phiên bản Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Lỗi: Yêu cầu Python 3.8 trở lên")
        print(f"   Phiên bản hiện tại: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()

def install_dependencies():
    """Cài đặt các dependencies từ requirements.txt"""
    print("[2/5] Cài đặt dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Lỗi: Không tìm thấy file requirements.txt")
        sys.exit(1)
    
    try:
        # Upgrade pip trước
        print("   Đang nâng cấp pip...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cài đặt dependencies
        print("   Đang cài đặt thư viện...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        
        print("✓ Cài đặt thành công tất cả dependencies")
        print()
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt dependencies: {e}")
        sys.exit(1)

def check_config_file():
    """Kiểm tra và tạo file config nếu chưa có"""
    print("[3/5] Kiểm tra file cấu hình...")
    
    config_file = Path(__file__).parent / "config.json"
    
    if config_file.exists():
        print("✓ File config.json đã tồn tại")
        print()
        return
    
    # Tạo config mặc định
    print("   Đang tạo file config.json mặc định...")
    
    default_config = {
        "prices": {
            "A4": {
                "soft": {
                    "bw": {"1": 1000, "2": 1500},
                    "color": {"1": 2000, "2": 3000}
                },
                "hard": {
                    "bw": {"1": 2000, "2": 3000},
                    "color": {"1": 4000, "2": 6000}
                }
            },
            "A3": {
                "soft": {
                    "bw": {"1": 2000, "2": 3000},
                    "color": {"1": 4000, "2": 5000}
                },
                "hard": {
                    "bw": {"1": 4000, "2": 6000},
                    "color": {"1": 8000, "2": 10000}
                }
            }
        },
        "defaults": {
            "pdf": {
                "size": "A4",
                "type": "soft",
                "color": "bw",
                "sides": 1,
                "pages_per_sheet": 1
            },
            "docx": {
                "size": "A4",
                "type": "soft",
                "color": "bw",
                "sides": 1,
                "pages_per_sheet": 1
            },
            "pptx": {
                "size": "A4",
                "type": "soft",
                "color": "bw",
                "sides": 1,
                "pages_per_sheet": 4
            },
            "xlsx": {
                "size": "A4",
                "type": "soft",
                "color": "bw",
                "sides": 1,
                "pages_per_sheet": 1
            },
            "image": {
                "size": "A4",
                "type": "soft",
                "color": "color",
                "sides": 1,
                "pages_per_sheet": 1
            }
        },
        "watch_folders": [],
        "customer_timeout_seconds": 60,
        "note": "Giá tính theo tờ. Key '1' = in 1 mặt, key '2' = in 2 mặt. watch_folders: danh sách folder tự động theo dõi khi khởi động."
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print("✓ Đã tạo file config.json với cấu hình mặc định")
        print()
    except Exception as e:
        print(f"❌ Lỗi khi tạo file config: {e}")
        sys.exit(1)

def verify_files():
    """Kiểm tra các file cần thiết"""
    print("[4/5] Kiểm tra các file cần thiết...")
    
    required_files = ["main.py", "utils.py", "config.json"]
    missing_files = []
    
    for file in required_files:
        file_path = Path(__file__).parent / file
        if file_path.exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ❌ {file} (không tìm thấy)")
            missing_files.append(file)
    
    if missing_files:
        print()
        print(f"❌ Thiếu {len(missing_files)} file cần thiết")
        sys.exit(1)
    
    print("✓ Tất cả file cần thiết đã có đầy đủ")
    print()

def create_shortcuts():
    """Tạo shortcut (tùy chọn)"""
    print("[5/5] Tạo shortcut...")
    
    if sys.platform != "win32":
        print("⚠ Chỉ hỗ trợ tạo shortcut trên Windows")
        print()
        return
    
    response = input("Bạn có muốn tạo shortcut trên Desktop? (y/n): ").lower().strip()
    
    if response != 'y':
        print("⊘ Bỏ qua tạo shortcut")
        print()
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        main_py = str(Path(__file__).parent / "main.py")
        shortcut_path = os.path.join(desktop, "AutoCashier.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{main_py}"'
        shortcut.WorkingDirectory = str(Path(__file__).parent)
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print(f"✓ Đã tạo shortcut: {shortcut_path}")
        print()
    except ImportError:
        print("⚠ Cần cài thêm: pip install pywin32 winshell")
        print("⊘ Bỏ qua tạo shortcut")
        print()
    except Exception as e:
        print(f"⚠ Không thể tạo shortcut: {e}")
        print()

def print_completion():
    """In thông báo hoàn tất"""
    print("=" * 60)
    print("  🎉 CÀI ĐẶT HOÀN TẤT!")
    print("=" * 60)
    print()
    print("Để chạy ứng dụng, sử dụng lệnh:")
    print()
    print("    python main.py")
    print()
    print("Hoặc double-click vào shortcut trên Desktop (nếu đã tạo)")
    print()
    print("Tham khảo README.md để biết thêm chi tiết sử dụng")
    print()

def main():
    """Hàm main"""
    print_header()
    
    try:
        check_python_version()
        install_dependencies()
        check_config_file()
        verify_files()
        create_shortcuts()
        print_completion()
    except KeyboardInterrupt:
        print()
        print("❌ Đã hủy cài đặt")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Lỗi không mong muốn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# ✅ AutoCashier - Hỗ trợ Windows 7

## 📋 Tổng quan

AutoCashier giờ đã có **2 phiên bản**:

| Phiên bản | File | Hỗ trợ | Giao diện |
|-----------|------|--------|-----------|
| **CustomTkinter** | `main.py` | Windows 10+ | Hiện đại, mượt mà |
| **PyQt5** | `main_pyqt5.py` | **Windows 7/8/10/11** | Tương tự, ổn định |

## 🚀 Chạy ứng dụng

### Windows 7/8:
```cmd
python main_pyqt5.py
```

### Windows 10+:
```cmd
# Dùng phiên bản nào cũng được
python main.py          # CustomTkinter (khuyên dùng)
python main_pyqt5.py    # PyQt5 (backup)
```

## 📦 Build file .exe

### Build cả 2 phiên bản:
```cmd
python build_exe.py
```

### Build riêng từng phiên bản:
```cmd
python build_exe.py --version pyqt5    # Chỉ build Win7+
python build_exe.py --version ctk      # Chỉ build Win10+
```

### Kết quả:
```
dist/
├── AutoCashier-Win7.exe     # PyQt5 - Windows 7+ (~80MB)
├── AutoCashier-Win10.exe    # CustomTkinter - Windows 10+ (~40MB)
└── config.json
```

## 🔧 Cài đặt Windows 7

### Bước 1: Cài Python 3.8.10
- **Download:** https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
- ✅ **Tick:** "Add Python 3.8 to PATH"
- Cài đặt bình thường

### Bước 2: Cài thư viện
```cmd
pip install PyQt5==5.15.9
pip install pypdf python-docx python-pptx openpyxl Pillow packaging
```

### Bước 3: Chạy ứng dụng
```cmd
cd C:\đường\dẫn\AutoCashier
python main_pyqt5.py
```

## ⚠️ Yêu cầu Windows 7

Nếu chạy file `.exe` và gặp lỗi "DLL not found":

**Cài Visual C++ Redistributable:**
- Download: https://aka.ms/vs/16/release/vc_redist.x64.exe
- Chạy file và cài đặt
- Restart máy
- Chạy lại AutoCashier-Win7.exe

## 🆚 So sánh chi tiết

### Tính năng

| Tính năng | CustomTkinter | PyQt5 |
|-----------|---------------|-------|
| Drag & Drop | ✅ | ✅ |
| Watch Folder | ✅ | ✅ |
| Mini Widget | ✅ | ✅ |
| Dark/Light Mode | ✅ | ✅ |
| Tính giá tự động | ✅ | ✅ |
| Global controls | ✅ | ✅ |

### Hiệu năng

| Chỉ số | CustomTkinter | PyQt5 |
|--------|---------------|-------|
| File .exe | ~40 MB | ~80 MB |
| RAM sử dụng | ~100 MB | ~130 MB |
| Tốc độ khởi động | ~1-2s | ~2-3s |
| Tốc độ hoạt động | Nhanh | Trung bình |

### Khuyến nghị

- ✅ **Windows 7/8:** Dùng PyQt5 (bắt buộc)
- ✅ **Windows 10+:** Dùng CustomTkinter (mượt hơn, nhẹ hơn)

## 📂 Cấu trúc project

```
AutoCashier/
├── main.py              # CustomTkinter (Win10+)
├── main_pyqt5.py        # PyQt5 (Win7+) ✨ MỚI
├── utils.py             # Shared utilities
├── config.json          # Configuration
├── build_exe.py         # Build script ✨ CẬP NHẬT
├── requirements.txt     # Dependencies ✨ CẬP NHẬT
├── README.md            # Main documentation
├── README_PYQT5.md      # PyQt5 guide ✨ MỚI
├── HEADLESS_SETUP.md    # Linux headless setup
└── WINDOWS7_SUPPORT.md  # This file ✨ MỚI
```

## 🐛 Troubleshooting

### Lỗi: "python is not recognized"
**Fix:**
1. Gỡ cài đặt Python
2. Cài lại, nhớ tick "Add Python to PATH"

### Lỗi: "No module named 'PyQt5'"
**Fix:**
```cmd
pip install PyQt5==5.15.9
```

### Lỗi: "Visual C++ Runtime not found"
**Fix:** Cài Visual C++ Redistributable (link ở trên)

### Lỗi: "config.json not found"
**Fix:** Copy file `config.json` vào cùng folder với `.exe`

## 💡 Tips

### Chạy cả 2 phiên bản cùng lúc?
**Không nên** - Cả 2 dùng chung file `config.json`, có thể conflict.

### So sánh thêm tính năng?
Xem file `README_PYQT5.md` để biết chi tiết đầy đủ.

### Build trên Windows 7?
```cmd
pip install pyinstaller==5.13.2
python build_exe.py --version pyqt5
```
**Lưu ý:** PyInstaller 6.0+ không hỗ trợ Win7!

## 📞 Hỗ trợ

- **Hướng dẫn đầy đủ:** `README_PYQT5.md`
- **Setup headless:** `HEADLESS_SETUP.md`
- **Build script:** `build_exe.py --help`

---

**Tác giả:** AutoCashier Team  
**Ngày cập nhật:** 30/11/2025  
**Phiên bản:** 2.0 - PyQt5 Support Added

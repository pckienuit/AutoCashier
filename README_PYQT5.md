# AutoCashier - PyQt5 Version (Hỗ trợ Windows 7)

## 📋 Tổng quan

Phiên bản **PyQt5** của AutoCashier được tạo ra để hỗ trợ **Windows 7** và các hệ thống cũ hơn. CustomTkinter (phiên bản gốc) chỉ hỗ trợ từ Windows 10 trở lên.

## 🆚 So sánh 2 phiên bản

| Tính năng | CustomTkinter (`main.py`) | PyQt5 (`main_pyqt5.py`) |
|-----------|---------------------------|-------------------------|
| **Hỗ trợ Windows 7** | ❌ Không | ✅ Có |
| **Hỗ trợ Windows 10+** | ✅ Có | ✅ Có |
| **Hỗ trợ Linux** | ✅ Có | ✅ Có |
| **Hỗ trợ macOS** | ✅ Có (10.13+) | ✅ Có (10.12+) |
| **Giao diện** | Hiện đại, rounded corners | Hiện đại, tương tự |
| **Dark/Light Mode** | ✅ Có | ✅ Có |
| **Drag & Drop** | ✅ Có | ✅ Có |
| **Watch Folder** | ✅ Có | ✅ Có |
| **Mini Widget** | ✅ Có | ✅ Có |
| **Kích thước file .exe** | ~30-40 MB | ~50-70 MB |
| **Thư viện phụ thuộc** | customtkinter, tkinterdnd2 | PyQt5 |

## 🚀 Cài đặt

### Windows 7

#### Bước 1: Cài Python 3.8.10
Windows 7 chỉ hỗ trợ tối đa **Python 3.8.10** (phiên bản cuối cùng cho Win7).

1. Tải về: [Python 3.8.10 - Windows x86-64](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
2. Chạy file cài đặt:
   - ✅ Tick vào **"Add Python 3.8 to PATH"**
   - Nhấn **"Install Now"**

#### Bước 2: Kiểm tra cài đặt
Mở **Command Prompt** (cmd) và gõ:
```cmd
python --version
```
Kết quả phải là: `Python 3.8.10`

#### Bước 3: Cài đặt thư viện
```cmd
cd C:\đường\dẫn\tới\AutoCashier
pip install PyQt5==5.15.9
pip install pypdf python-docx python-pptx openpyxl Pillow packaging
```

**Lưu ý quan trọng:**
- Dùng PyQt5 **5.15.9** (phiên bản cuối cùng hỗ trợ Python 3.8)
- **KHÔNG** cài `customtkinter` và `tkinterdnd2` (không cần thiết cho bản PyQt5)

### Windows 10/11

#### Cài Python 3.11 hoặc 3.12
1. Tải về: [Python 3.12](https://www.python.org/downloads/)
2. Cài đặt (tick vào "Add Python to PATH")

#### Cài đặt thư viện
```cmd
pip install -r requirements.txt
```

Hoặc chỉ cài PyQt5:
```cmd
pip install PyQt5 pypdf python-docx python-pptx openpyxl Pillow packaging
```

### Linux / macOS

```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5

# Hoặc dùng pip
pip install PyQt5

# Cài dependencies
pip install pypdf python-docx python-pptx openpyxl Pillow packaging
```

## ▶️ Chạy ứng dụng

### Chạy phiên bản PyQt5 (Windows 7 compatible)
```cmd
python main_pyqt5.py
```

### Chạy phiên bản CustomTkinter (Windows 10+)
```cmd
python main.py
```

## 📦 Tạo file .exe (Windows)

### Cho Windows 7

#### Bước 1: Cài PyInstaller trên Windows 7
```cmd
pip install pyinstaller==5.13.2
```
**Lưu ý:** PyInstaller 6.0+ không hỗ trợ Windows 7!

#### Bước 2: Build
```cmd
pyinstaller --onefile --windowed --name="AutoCashier-Win7" --icon=icon.ico main_pyqt5.py
```

File `.exe` sẽ nằm trong thư mục `dist/`

### Cho Windows 10+

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --name="AutoCashier" --icon=icon.ico main_pyqt5.py
```

### Tùy chọn nâng cao
```cmd
pyinstaller --onefile ^
            --windowed ^
            --name="AutoCashier" ^
            --icon=icon.ico ^
            --add-data "config.json;." ^
            --noconsole ^
            main_pyqt5.py
```

## 🎨 Tính năng

### 1. Giao diện chính
- **Header:** Logo, nút minimize, theme toggle, global controls
- **Bảng file:** Hiển thị danh sách file với các tùy chọn
- **Footer:** Nút thêm/xóa file, hiển thị tổng tiền

### 2. Tính năng nâng cao
- ✅ **Drag & Drop:** Kéo thả file trực tiếp vào cửa sổ
- ✅ **Watch Folder:** Tự động theo dõi folder và thêm file mới
- ✅ **Mini Widget:** Cửa sổ mini luôn hiển thị, always-on-top
- ✅ **Dark/Light Mode:** Chuyển đổi giao diện sáng/tối
- ✅ **Global Controls:** Áp dụng thiết lập cho tất cả file cùng lúc
- ✅ **Tự động reset khách hàng:** Xóa danh sách sau timeout

### 3. Các cột trong bảng
1. **Tên file:** Tên file gốc
2. **Trang:** Số trang (có thể chỉnh sửa)
3. **Khổ:** A4 / A3
4. **Loại:** soft / hard (giấy mềm/cứng)
5. **Màu:** bw (đen trắng) / color (màu)
6. **Mặt:** 1 mặt / 2 mặt
7. **Ghép:** Số trang ghép trên 1 mặt (1/2/4/6/9)
8. **Giá:** Giá tính tự động (VND)
9. **Xóa:** Nút xóa file

### 4. Cách tính giá
```python
# Ví dụ: 32 trang, ghép 2, in 2 mặt
faces_to_print = ceil(32 / 2 / 2) = ceil(8) = 8 mặt
sheets_physical = ceil(8 / 2) = 4 tờ giấy
# In 2 mặt → dùng 4 tờ
sheets_needed = 4

# Giá = 4 tờ × giá_per_sheet
# Làm tròn lên hàng nghìn
```

## ⚙️ Cấu hình (config.json)

```json
{
  "prices": {
    "A4": {
      "soft": {
        "bw": { "1": 500, "2": 400 },
        "color": { "1": 2000, "2": 1500 }
      },
      "hard": {
        "bw": { "1": 700, "2": 600 },
        "color": { "1": 2500, "2": 2000 }
      }
    },
    "A3": { ... }
  },
  "defaults": {
    "pdf": { "size": "A4", "type": "soft", "color": "bw", "sides": "1", "pages_per_sheet": "1" },
    "docx": { ... },
    "pptx": { ... },
    "xlsx": { ... },
    "image": { ... },
    "default": { ... }
  },
  "watch_folders": [
    "C:\\Users\\Public\\Downloads"
  ],
  "customer_timeout_seconds": 60
}
```

### Giải thích:
- **prices:** Bảng giá theo khổ giấy, loại giấy, màu sắc, mặt in
- **defaults:** Thiết lập mặc định cho từng loại file
- **watch_folders:** Danh sách folder tự động theo dõi
- **customer_timeout_seconds:** Thời gian timeout để reset khách hàng mới (giây)

## 🛠️ Khắc phục sự cố

### Windows 7

#### Lỗi: "python is not recognized"
**Nguyên nhân:** Python chưa được thêm vào PATH.

**Cách fix:**
1. Gỡ cài đặt Python
2. Cài lại và **tick vào "Add Python to PATH"**

#### Lỗi: "No module named 'PyQt5'"
```cmd
pip install PyQt5==5.15.9
```

#### Lỗi: "dll load failed" khi chạy .exe
**Nguyên nhân:** Thiếu Visual C++ Runtime.

**Cách fix:**
1. Tải về: [Visual C++ 2015-2019 Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe)
2. Cài đặt

#### Lỗi: PyInstaller không hoạt động
```cmd
pip uninstall pyinstaller
pip install pyinstaller==5.13.2
```

### Windows 10/11

#### Lỗi: Cửa sổ nhấp nháy rồi tắt
- Chạy từ Command Prompt để xem lỗi chi tiết:
  ```cmd
  python main_pyqt5.py
  ```

#### Lỗi: "config.json not found"
- Đảm bảo file `config.json` nằm cùng thư mục với `main_pyqt5.py`

### Linux

#### Lỗi: "Qt platform plugin could not be initialized"
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

#### Headless environment (Server)
PyQt5 cần X server. Dùng Xvfb:
```bash
sudo apt-get install xvfb
xvfb-run python main_pyqt5.py
```

## 🔄 Chuyển đổi giữa 2 phiên bản

### Từ CustomTkinter → PyQt5
1. Cài PyQt5: `pip install PyQt5`
2. Chạy: `python main_pyqt5.py`
3. Config.json giữ nguyên, không cần thay đổi

### Từ PyQt5 → CustomTkinter
1. Cài CustomTkinter: `pip install customtkinter tkinterdnd2`
2. Chạy: `python main.py`

## 📝 File structure

```
AutoCashier/
├── main.py              # Phiên bản CustomTkinter (Windows 10+)
├── main_pyqt5.py        # Phiên bản PyQt5 (Windows 7+)
├── utils.py             # Hàm tiện ích (chung cho cả 2 phiên bản)
├── config.json          # File cấu hình
├── requirements.txt     # Danh sách thư viện
├── README.md            # Hướng dẫn chính
├── README_PYQT5.md      # Hướng dẫn PyQt5 (file này)
├── HEADLESS_SETUP.md    # Hướng dẫn chạy headless (Linux)
└── build_exe.py         # Script build .exe tự động
```

## 📊 Performance

### Kích thước file .exe

| Phiên bản | Kích thước |
|-----------|-----------|
| CustomTkinter | ~30-40 MB |
| PyQt5 | ~50-70 MB |

### Tốc độ khởi động

| Phiên bản | Thời gian khởi động |
|-----------|---------------------|
| CustomTkinter | ~1-2 giây |
| PyQt5 | ~2-3 giây |

### Bộ nhớ RAM

| Phiên bản | RAM sử dụng |
|-----------|-------------|
| CustomTkinter | ~80-120 MB |
| PyQt5 | ~100-150 MB |

## 🎯 Khi nào dùng phiên bản nào?

### Dùng PyQt5 (`main_pyqt5.py`) khi:
- ✅ Cần chạy trên **Windows 7**
- ✅ Cần compatibility tối đa với nhiều hệ điều hành
- ✅ Muốn giao diện ổn định, ít bug
- ✅ Không quan tâm file .exe hơi lớn

### Dùng CustomTkinter (`main.py`) khi:
- ✅ Chạy trên **Windows 10+**
- ✅ Muốn giao diện hiện đại hơn
- ✅ Muốn file .exe nhỏ gọn hơn
- ✅ Headless environment (Linux server với Xvfb)

## 🔗 Liên kết hữu ích

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Python 3.8.10 Download](https://www.python.org/downloads/release/python-3810/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Visual C++ Runtime](https://aka.ms/vs/16/release/vc_redist.x64.exe)

## 💡 Tips & Tricks

### Tăng tốc độ khởi động
Compile bytecode:
```cmd
python -m compileall main_pyqt5.py utils.py
```

### Giảm kích thước .exe
Dùng UPX compression:
```cmd
pyinstaller --onefile --windowed --upx-dir=C:\path\to\upx main_pyqt5.py
```

### Debug mode
Chạy với console window để xem logs:
```cmd
pyinstaller --onefile --console main_pyqt5.py
```

## ❓ FAQ

**Q: Tại sao không dùng PyQt6?**  
A: PyQt6 không hỗ trợ Windows 7. PyQt5 là phiên bản cuối cùng có Win7 support.

**Q: Có thể chạy cả 2 phiên bản cùng lúc không?**  
A: Có, nhưng không nên vì dùng chung file `config.json`.

**Q: File .exe có chạy được trên máy khác không?**  
A: Có, nhưng cần cài Visual C++ Runtime (link ở trên).

**Q: Làm sao biết đang chạy phiên bản nào?**  
A: Xem tiêu đề cửa sổ: "AutoCashier" (CustomTkinter) vs "AutoCashier - PyQt5"

**Q: Có thể dùng Python 3.9+ trên Windows 7 không?**  
A: Không, Win7 chỉ hỗ trợ tối đa Python 3.8.10.

---

**Tác giả:** AutoCashier Team  
**Phiên bản:** 2.0 (PyQt5)  
**Ngày cập nhật:** 30/11/2025

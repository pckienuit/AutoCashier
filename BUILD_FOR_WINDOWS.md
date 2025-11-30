# Build .exe cho Windows

## ⚠️ LƯU Ý QUAN TRỌNG

**PyInstaller KHÔNG thể cross-compile!**

- Build trên **Linux** → Linux executable
- Build trên **Windows** → Windows .exe
- Build trên **macOS** → macOS app

File `AutoCashier-Win7.exe` build từ Linux chỉ là Linux binary với tên `.exe`, **KHÔNG chạy được trên Windows**.

---

## ✅ Cách 1: Build trên máy Windows (Khuyên dùng)

### Windows 7:

```cmd
REM Bước 1: Cài Python 3.8.10
REM Download: https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
REM Tick "Add Python 3.8 to PATH" khi cài

REM Bước 2: Mở Command Prompt
cd C:\đường\dẫn\AutoCashier

REM Bước 3: Cài dependencies
pip install pyinstaller==5.13.2
pip install PyQt5==5.15.9
pip install pypdf python-docx python-pptx openpyxl Pillow packaging

REM Bước 4: Build
python build_exe.py --version pyqt5

REM Bước 5: File .exe ở trong folder dist/
dir dist\
```

### Windows 10/11:

```cmd
REM Bước 1: Cài Python 3.11 hoặc 3.12
REM Download: https://www.python.org/downloads/

cd C:\đường\dẫn\AutoCashier

REM Bước 2: Cài dependencies
pip install pyinstaller
pip install PyQt5
pip install customtkinter tkinterdnd2
pip install pypdf python-docx python-pptx openpyxl Pillow packaging

REM Bước 3: Build cả 2 phiên bản
python build_exe.py

REM Hoặc chỉ build 1 phiên bản:
python build_exe.py --version pyqt5    REM PyQt5 (Win7+)
python build_exe.py --version ctk      REM CustomTkinter (Win10+)
```

---

## 🐳 Cách 2: Dùng Wine (Build Windows .exe từ Linux)

Wine cho phép chạy Python Windows trên Linux.

### Cài đặt Wine và Python Windows:

```bash
# Cài Wine
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install wine wine32 wine64

# Download Python Windows installer
wget https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe

# Cài Python qua Wine
wine python-3.8.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Kiểm tra
wine python --version
```

### Build với Wine:

```bash
cd /workspaces/AutoCashier

# Cài dependencies
wine python -m pip install pyinstaller==5.13.2
wine python -m pip install PyQt5==5.15.9
wine python -m pip install pypdf python-docx python-pptx openpyxl Pillow packaging

# Build
wine python build_exe.py --version pyqt5

# File .exe sẽ ở dist/ và chạy được trên Windows
```

**Lưu ý:** Wine có thể không ổn định, khuyên dùng Cách 1.

---

## ☁️ Cách 3: Dùng GitHub Actions (CI/CD)

Tạo workflow tự động build trên Windows.

### File `.github/workflows/build.yml`:

```yaml
name: Build Windows Executables

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pyinstaller
        pip install PyQt5 customtkinter tkinterdnd2
        pip install pypdf python-docx python-pptx openpyxl Pillow packaging
    
    - name: Build executables
      run: python build_exe.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: AutoCashier-Windows
        path: dist/*.exe
```

Sau khi push code, GitHub tự động build và upload file .exe trong tab **Actions**.

---

## 🖥️ Cách 4: Dùng Windows Virtual Machine

### Trên Linux host:

```bash
# Cài VirtualBox
sudo apt install virtualbox

# Download Windows 10 ISO
# https://www.microsoft.com/en-us/software-download/windows10

# Tạo VM và cài Windows
# Sau đó copy source code vào VM và build theo Cách 1
```

---

## 📋 So sánh các cách:

| Cách | Độ khó | Tốc độ | Độ tin cậy |
|------|--------|--------|------------|
| **1. Build trên Windows** | ⭐ Dễ | ⭐⭐⭐ Nhanh | ⭐⭐⭐ Cao |
| **2. Wine** | ⭐⭐⭐ Khó | ⭐⭐ Trung bình | ⭐⭐ Trung bình |
| **3. GitHub Actions** | ⭐⭐ Vừa | ⭐ Chậm | ⭐⭐⭐ Cao |
| **4. Virtual Machine** | ⭐⭐⭐ Khó | ⭐ Chậm | ⭐⭐⭐ Cao |

---

## ✅ Khuyến nghị:

1. **Có máy Windows?** → Dùng **Cách 1** (đơn giản nhất)
2. **Chỉ có Linux/macOS?** → Dùng **Cách 3** (GitHub Actions)
3. **Cần test nhiều?** → Setup **Cách 4** (VM)

---

## 🐛 Khắc phục lỗi "file is not compatible"

Lỗi này xảy ra vì:
- ❌ File build trên Linux không phải Windows .exe thực sự
- ❌ Format: ELF (Linux) thay vì PE (Windows)

**Kiểm tra file type:**

```bash
# Trên Linux:
file dist/AutoCashier-Win7.exe
# Output sai: "ELF 64-bit LSB executable"
# Output đúng: "PE32+ executable (GUI) x86-64, for MS Windows"
```

**Fix:** Build lại trên Windows hoặc dùng Wine/GitHub Actions.

---

## 📝 Checklist build đúng:

- [ ] Build trên Windows (hoặc Wine/GitHub Actions)
- [ ] Cài đúng Python version (3.8.10 cho Win7, 3.11+ cho Win10+)
- [ ] Cài đúng PyInstaller version (5.13.2 cho Win7, latest cho Win10+)
- [ ] File .exe xuất hiện trong `dist/`
- [ ] Kiểm tra file type: PE32+ executable
- [ ] Test trên máy Windows target

---

**Tác giả:** AutoCashier Team  
**Ngày cập nhật:** 30/11/2025

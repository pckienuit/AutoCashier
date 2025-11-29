# 💰 AutoCashier - Hệ thống tính tiền photocopy tự động

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Ứng dụng desktop hiện đại dành cho tiệm photocopy, giúp tính tiền nhanh chóng và chính xác cho nhiều loại file.

![AutoCashier Demo](https://via.placeholder.com/800x450/1f538b/ffffff?text=AutoCashier+Screenshot)

## ✨ Tính năng nổi bật

### 📄 Hỗ trợ đa định dạng file
- **PDF** - Đếm chính xác số trang
- **Word (.docx)** - Ước tính thông minh
- **PowerPoint (.pptx)** - Đếm theo slide
- **Excel (.xlsx)** - Đếm theo sheet
- **Ảnh (.jpg, .png, .bmp)** - Mỗi ảnh = 1 trang

### 💵 Tính giá thông minh
- Tính theo **số tờ giấy** (không phải số trang)
- Làm tròn tự động lên nghìn
- Cấu hình giá linh hoạt qua JSON
- Hỗ trợ ghép trang (1, 2, 4, 6, 9 trang/mặt)

### 🎯 Tùy chọn in đa dạng
- **Khổ giấy**: A4, A3
- **Chất liệu**: Giấy mềm, giấy cứng
- **Màu sắc**: Đen trắng, màu
- **Số mặt**: 1 mặt, 2 mặt (duplex)

### 🚀 Tính năng tự động hóa
- **Theo dõi folder** - Tự động thêm file mới
- **Timeout khách hàng** - Tự xóa sau 60s
- **Mini widget** - Luôn hiển thị ở góc màn hình
- **Drag & Drop** - Kéo thả file dễ dàng

### 🎨 Giao diện hiện đại
- Theme sáng/tối
- Responsive layout
- Always-on-top widget
- Font và màu sắc tối ưu

---

## 📦 Cài đặt

### Yêu cầu hệ thống
- Windows 10/11 (64-bit)
- Python 3.8+ (nếu chạy từ source)
- 100MB dung lượng trống

### Phương pháp 1: Chạy file .exe (Khuyến nghị)

**Không cần cài Python!**

1. Tải file `AutoCashier.exe` từ [Releases](https://github.com/pckienuit/AutoCashier/releases)
2. Double-click để chạy
3. Chỉnh sửa `config.json` để thay đổi giá

> **Lưu ý:** Windows Defender có thể cảnh báo. Chọn "More info" → "Run anyway"

### Phương pháp 2: Cài đặt tự động (Python)

```bash
# Clone repository
git clone https://github.com/pckienuit/AutoCashier.git
cd AutoCashier

# Chạy script cài đặt
python setup.py
```

Script sẽ tự động:
- ✓ Kiểm tra Python version
- ✓ Cài đặt dependencies
- ✓ Tạo config.json mặc định
- ✓ Kiểm tra file cần thiết
- ✓ Tạo shortcut (tùy chọn)

### Phương pháp 3: Cài đặt thủ công

```bash
# Clone repository
git clone https://github.com/pckienuit/AutoCashier.git
cd AutoCashier

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py
```

### Phương pháp 4: Build file .exe từ source

```bash
# Cài đặt dependencies (bao gồm PyInstaller)
pip install -r requirements.txt

# Build exe
python build_exe.py
```

File `AutoCashier.exe` sẽ được tạo trong folder `dist/`

---

## 🚀 Hướng dẫn sử dụng

### Khởi động ứng dụng

```bash
python main.py
```

Hoặc double-click file `AutoCashier.exe`

### Thêm file cần in

Có 3 cách:

1. **Kéo thả** - Kéo file trực tiếp vào cửa sổ
2. **Nút "Thêm File"** - Click và chọn từ hộp thoại
3. **Tự động** - File trong folder được theo dõi

### Chỉnh sửa thông tin file

Mỗi file có 7 cột có thể chỉnh sửa:

| Cột | Tùy chọn | Mô tả |
|-----|----------|-------|
| **Số trang** | Số | Thay đổi nếu ước tính sai |
| **Khổ** | A4, A3 | Kích thước giấy in |
| **Loại** | Mềm, Cứng | Chất liệu giấy |
| **Màu** | BW, Color | Đen trắng hoặc màu |
| **Mặt** | 1, 2 | Một mặt hoặc hai mặt |
| **Trang/mặt** | 1, 2, 4, 6, 9 | Ghép trang để tiết kiệm |

### Theo dõi folder tự động

1. **Click chuột phải** vào nút "Thêm File"
2. Chọn **"Quản lý Folder"**
3. Click **"Thêm Folder"** và chọn folder cần theo dõi
4. File mới sẽ tự động thêm vào ứng dụng

**Tính năng đặc biệt:**
- File tự động xóa sau 60 giây (dành cho khách mới)
- Hỗ trợ theo dõi nhiều folder cùng lúc
- Lưu vào config để tự động chạy lần sau

### Sử dụng Mini Widget

1. Click nút **▼** (minimize) ở góc trên
2. Widget nhỏ sẽ luôn hiển thị ở góc phải màn hình
3. Hiển thị: **Tổng tiền** (to) + Số file | Trang | Tờ
4. Click **▲** để mở lại cửa sổ chính

### Chuyển đổi theme

Click nút **🌙/☀️** để đổi giữa theme tối và sáng

---

## ⚙️ Cấu hình

### Cấu trúc file config.json

```json
{
  "prices": {
    "A4": {
      "soft": {
        "bw": { "1": 1000, "2": 1500 },
        "color": { "1": 2000, "2": 3000 }
      },
      "hard": {
        "bw": { "1": 2000, "2": 3000 },
        "color": { "1": 4000, "2": 6000 }
      }
    },
    "A3": {
      "soft": {
        "bw": { "1": 2000, "2": 3000 },
        "color": { "1": 4000, "2": 5000 }
      },
      "hard": {
        "bw": { "1": 4000, "2": 6000 },
        "color": { "1": 8000, "2": 10000 }
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
    "pptx": {
      "pages_per_sheet": 4
    }
  },
  "watch_folders": [],
  "customer_timeout_seconds": 60
}
```

### Giải thích chi tiết

#### 1. Bảng giá (`prices`)

Cấu trúc: `prices[khổ][loại][màu][mặt] = giá`

- **Khổ giấy**: `A4`, `A3`
- **Loại giấy**: `soft` (mềm), `hard` (cứng)  
- **Màu**: `bw` (đen trắng), `color` (màu)
- **Số mặt**: `"1"` (1 mặt), `"2"` (2 mặt) - **phải là string!**

**Ví dụ:** `prices.A4.soft.color.2 = 3000` nghĩa là:
- Giấy A4 mềm, in màu, 2 mặt = **3.000đ/tờ**

#### 2. Mặc định theo loại file (`defaults`)

```json
"pdf": {
  "size": "A4",
  "type": "soft", 
  "color": "bw",
  "sides": 1,
  "pages_per_sheet": 1
}
```

Các loại file: `pdf`, `docx`, `pptx`, `xlsx`, `image`

**Mẹo:** Đặt PowerPoint `pages_per_sheet: 4` để tiết kiệm giấy

#### 3. Folder theo dõi (`watch_folders`)

```json
"watch_folders": [
  "D:/PhotocopyShop/In",
  "C:/Users/Public/Desktop/In"
]
```

Danh sách folder tự động theo dõi khi khởi động

#### 4. Timeout khách hàng (`customer_timeout_seconds`)

```json
"customer_timeout_seconds": 60
```

Thời gian tự động xóa file (mặc định 60 giây)

---

## 💰 Công thức tính tiền

### Các bước tính

```
1. Số mặt in = ⌈Số trang / Trang_per_mặt⌉

2. Số tờ giấy = {
     Số mặt                  (nếu in 1 mặt)
     ⌈Số mặt / 2⌉            (nếu in 2 mặt)
   }

3. Giá tạm = Số tờ × Đơn giá

4. Giá cuối = ⌈Giá tạm / 1000⌉ × 1000  (làm tròn lên nghìn)
```

### Ví dụ cụ thể

**Case 1: File PDF đơn giản**
- 10 trang, A4 đen trắng, 1 mặt, 1 trang/mặt
- Đơn giá: 1.000đ/tờ

```
Số mặt = ⌈10 / 1⌉ = 10 mặt
Số tờ = 10 tờ (in 1 mặt)
Giá tạm = 10 × 1.000 = 10.000đ
Giá cuối = ⌈10.000 / 1.000⌉ × 1.000 = 10.000đ
```

**Case 2: File PowerPoint ghép trang**
- 12 slide, A4 màu, 2 mặt, 4 slide/mặt
- Đơn giá: 3.000đ/tờ

```
Số mặt = ⌈12 / 4⌉ = 3 mặt
Số tờ = ⌈3 / 2⌉ = 2 tờ (in 2 mặt)
Giá tạm = 2 × 3.000 = 6.000đ
Giá cuối = ⌈6.000 / 1.000⌉ × 1.000 = 6.000đ
```

**Case 3: File lớn với làm tròn**
- 25 trang, A4 màu, 2 mặt, 2 trang/mặt
- Đơn giá: 3.000đ/tờ

```
Số mặt = ⌈25 / 2⌉ = 13 mặt
Số tờ = ⌈13 / 2⌉ = 7 tờ
Giá tạm = 7 × 3.000 = 21.000đ
Giá cuối = ⌈21.000 / 1.000⌉ × 1.000 = 21.000đ
```

**Case 4: Số lẻ cần làm tròn**
- 3 trang, A4 đen trắng, 1 mặt, 1 trang/mặt
- Đơn giá: 1.200đ/tờ (giá lẻ)

```
Số mặt = ⌈3 / 1⌉ = 3 mặt
Số tờ = 3 tờ
Giá tạm = 3 × 1.200 = 3.600đ
Giá cuối = ⌈3.600 / 1.000⌉ × 1.000 = 4.000đ ← Làm tròn lên
```

---

## 🐛 Khắc phục sự cố

### 1. Lỗi khi chạy ứng dụng

**Lỗi:** `ModuleNotFoundError: No module named 'customtkinter'`

**Nguyên nhân:** Chưa cài đặt dependencies

**Giải pháp:**
```bash
pip install -r requirements.txt
```

---

**Lỗi:** `UnicodeDecodeError` khi load config

**Nguyên nhân:** File config không phải UTF-8

**Giải pháp:**
- Mở `config.json` bằng Notepad++
- Chuyển encoding sang UTF-8
- Hoặc xóa file và chạy lại `setup.py`

---

### 2. File đếm sai số trang

**Word (.docx):**
- Ứng dụng ước tính ~3000 ký tự/trang
- Có thể chênh lệch nếu nhiều hình ảnh/bảng
- **Giải pháp:** Chỉnh sửa số trang thủ công trong cột "Trang"

**PowerPoint (.pptx):**
- Đếm chính xác theo số slide
- Không có vấn đề

**Excel (.xlsx):**
- Đếm theo số sheet, không phải số trang in thực tế
- **Giải pháp:** Kiểm tra file và chỉnh thủ công

---

### 3. Folder watch không hoạt động

**Kiểm tra:**
1. Đường dẫn trong `config.json` có đúng không?
2. Folder có tồn tại và có quyền truy cập?
3. Click chuột phải "Thêm File" → "Quản lý Folder" để kiểm tra

**Lưu ý:**
- Dùng dấu `/` thay vì `\` trong đường dẫn
- Ví dụ: `D:/Photo` thay vì `D:\Photo`

---

### 4. Giá tính sai

**Kiểm tra:**
1. Cấu trúc JSON đúng chưa? (dùng JSONLint.com)
2. Key `"1"` và `"2"` phải là **string**, không phải number
3. Giá tính theo **số tờ**, không phải số trang

**Ví dụ sai:**
```json
"bw": { 1: 1000, 2: 1500 }  ❌ Thiếu dấu ngoặc kép
```

**Ví dụ đúng:**
```json
"bw": { "1": 1000, "2": 1500 }  ✓
```

---

### 5. Windows Defender chặn file .exe

**Nguyên nhân:** File exe do PyInstaller tạo thường bị cảnh báo

**Giải pháp:**
1. Click "More info"
2. Click "Run anyway"
3. Hoặc thêm exception trong Windows Security

---

### 6. Mini widget không hiển thị

**Kiểm tra:**
1. Có đang ở chế độ fullscreen không?
2. Thử Alt+Tab để tìm cửa sổ
3. Click nút ▲ trên widget để restore

---

## 📁 Cấu trúc project

```
AutoCashier/
├── .git/                   # Git repository
├── .venv/                  # Virtual environment (nếu có)
├── .gitignore             # Git ignore file
│
├── main.py                # ⭐ File chính - UI và logic
├── utils.py               # Hàm tiện ích (đếm trang, format)
├── config.json            # ⚙️ Cấu hình giá và mặc định
│
├── requirements.txt       # Dependencies Python
├── setup.py              # Script cài đặt tự động
├── build_exe.py          # Script build file .exe
│
└── README.md             # 📖 Tài liệu này
```

### Mô tả các file chính

**main.py** (1131 dòng)
- Class `FileRow`: Component hiển thị 1 file
- Class `MiniWidget`: Widget thu nhỏ always-on-top
- Class `App`: Cửa sổ chính với tất cả logic
- Hàm `calculate_price()`: Tính giá theo công thức

**utils.py**
- `get_page_count()`: Đếm trang cho từng loại file
- `format_currency()`: Format số tiền có dấu chấm

**config.json**
- Bảng giá theo khổ, loại, màu, mặt
- Mặc định cho từng loại file
- Danh sách folder theo dõi
- Timeout khách hàng

---

## 🔧 Phát triển

### Chạy trong môi trường dev

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py
```

### Build file executable

```bash
# Build với PyInstaller
python build_exe.py

# Output: dist/AutoCashier.exe
```

### Thêm tính năng mới

1. Fork repository
2. Tạo branch mới: `git checkout -b feature/ten-tinh-nang`
3. Commit changes: `git commit -m "Thêm tính năng X"`
4. Push: `git push origin feature/ten-tinh-nang`
5. Tạo Pull Request

---

## 🗺️ Roadmap

### Version 1.1 (Tương lai)
- [ ] Export hóa đơn PDF
- [ ] Lịch sử giao dịch
- [ ] Thống kê doanh thu
- [ ] Database SQLite
- [ ] Hỗ trợ nhiều máy in

### Version 1.2
- [ ] Chức năng tính công nợ
- [ ] Quản lý khách hàng
- [ ] In trực tiếp từ app
- [ ] Cloud backup

### Version 2.0
- [ ] Web version
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Plugin system

---

## 📜 Changelog

### Version 1.0.0 (29/11/2024)

**Tính năng chính:**
- ✨ Hỗ trợ 5 định dạng file: PDF, Word, PowerPoint, Excel, ảnh
- 💰 Tính giá theo số tờ giấy, làm tròn lên nghìn
- 📁 Theo dõi nhiều folder cùng lúc với auto-reload
- 👥 Tự động xóa file sau timeout (60s) cho khách mới
- 🪟 Mini widget always-on-top với hiển thị tổng tiền lớn
- 🌓 Theme sáng/tối với toggle dễ dàng
- 🎨 Giao diện CustomTkinter hiện đại
- ⚙️ Cấu hình linh hoạt hoàn toàn qua JSON
- 🖱️ Drag & Drop file vào cửa sổ
- 📝 7 cột tùy chỉnh cho mỗi file

**Công nghệ:**
- Python 3.8+
- CustomTkinter (UI framework)
- tkinterdnd2 (Drag & Drop)
- pypdf, python-docx, python-pptx, openpyxl, Pillow (File handling)
- PyInstaller (Build exe)

---

## 📄 License

MIT License

Copyright (c) 2024 PCKIEN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👨‍💻 Tác giả

**PCKIEN**  
GitHub: [@pckienuit](https://github.com/pckienuit)  
Email: pckien@example.com

---

## 🙏 Đóng góp

Contributions, issues và feature requests luôn được chào đón!

Hãy thoải mái:
- 🐛 Report bugs
- 💡 Suggest features  
- 🔧 Submit PRs

Xem [issues page](https://github.com/pckienuit/AutoCashier/issues)

---

## ⭐ Support

Nếu project này hữu ích, hãy cho một ⭐️ trên GitHub!

**Ủng hộ phát triển:**
- ⭐ Star repository
- 🍴 Fork và contribute
- 📢 Share với bạn bè
- ☕ [Buy me a coffee](https://www.buymeacoffee.com/pckien)

---

**Made with ❤️ in Vietnam**

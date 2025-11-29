# AutoCashier

Ứng dụng quản lý và tính tiền photocopy tự động cho tiệm photo.

![AutoCashier](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🎯 Tính năng

### Tính năng chính
- ✅ **Tính tiền tự động**: Hỗ trợ nhiều loại giấy (A4, A3), chất liệu (mềm/cứng), màu sắc (đen trắng/màu)
- 📁 **Theo dõi folder**: Tự động phát hiện file mới trong folder (Downloads, Desktop...)
- 👥 **Phân biệt khách hàng**: Tự động phân nhóm file theo thời gian (mặc định 60s)
- 📊 **Mini Widget**: Hiển thị tổng tiền và thống kê luôn ở trên cùng
- 🎨 **Giao diện hiện đại**: Light/Dark mode, drag & drop file
- 🔧 **Cấu hình linh hoạt**: Dễ dàng thay đổi giá và cài đặt qua file config

### Định dạng file hỗ trợ
- 📄 PDF (.pdf)
- 📝 Word (.docx, .doc)
- 📊 PowerPoint (.pptx, .ppt)
- 📈 Excel (.xlsx, .xls)
- 🖼️ Ảnh (.jpg, .jpeg, .png, .bmp, .gif, .tiff)

### Tùy chọn in
- **Khổ giấy**: A4, A3
- **Chất liệu**: Mềm (soft), Cứng (hard)
- **Màu sắc**: Đen trắng (bw), Màu (color)
- **Số mặt**: 1 mặt, 2 mặt
- **Ghép trang**: 1, 2, 4, 6, 9 trang/mặt

## 📦 Cài đặt

### Yêu cầu hệ thống
- Windows 10/11
- Python 3.8 trở lên
- 100MB dung lượng trống

### Cài đặt nhanh

#### Cách 1: Sử dụng file setup (Khuyến nghị)
```bash
python setup.py
```

#### Cách 2: Cài đặt thủ công
```bash
pip install -r requirements.txt
python main.py
```

#### Cách 3: Build file .exe (Không cần Python)
```bash
pip install pyinstaller
python build_exe.py
```
File exe sẽ được tạo trong folder `dist/`. Copy cả folder để chạy trên máy khác.

## 🚀 Sử dụng

### Khởi động ứng dụng
```bash
python main.py
```

### Thêm file cần in
1. **Kéo thả**: Kéo file trực tiếp vào cửa sổ ứng dụng
2. **Nút "Thêm File"**: Click chọn file từ hộp thoại
3. **Tự động**: File trong folder được theo dõi sẽ tự động thêm vào

### Tính năng nâng cao

#### Theo dõi folder
- Click chuột phải vào **"Thêm File"** → chọn **"Quản lý Folder"**
- Thêm folder cần theo dõi → file mới sẽ tự động thêm vào
- File sẽ tự động xóa sau 60 giây (dành cho khách hàng mới)

#### Mini Widget
- Click nút **▼** để thu nhỏ về widget luôn hiển thị
- Widget hiển thị: Tổng tiền (to), Số file | Số trang | Số tờ
- Click **▲** để mở lại cửa sổ chính

#### Chuyển theme
- Click nút **🌙/☀️** để đổi giữa theme tối và sáng

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
      "hard": { ... }
    },
    "A3": { ... }
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
  "watch_folders": ["D:/In"],
  "customer_timeout_seconds": 60
}
```

### Giải thích

#### Bảng giá (`prices`)
- **Khổ giấy**: `A4`, `A3`
- **Loại giấy**: `soft` (mềm), `hard` (cứng)
- **Màu**: `bw` (đen trắng), `color` (màu)
- **Số mặt**: `"1"` (1 mặt), `"2"` (2 mặt)
- **Giá**: Tính theo **số tờ giấy**, không phải số trang

#### Mặc định theo loại file (`defaults`)
- `pdf`: In 1 trang/mặt, đen trắng, 1 mặt
- `pptx`: Ghép 4 slide/mặt (tiết kiệm giấy)
- `docx`, `xlsx`, `image`: Tùy chỉnh theo nhu cầu

#### Folder theo dõi (`watch_folders`)
- Danh sách folder tự động theo dõi khi khởi động
- File mới sẽ tự động thêm vào ứng dụng

#### Timeout khách hàng (`customer_timeout_seconds`)
- Thời gian tự động xóa file (mặc định 60 giây)
- Phù hợp cho tiệm photo có nhiều khách

## 💰 Cách tính tiền

### Công thức
```
1. Số mặt = ⌈Số trang / Trang/mặt⌉
2. Số tờ = Số mặt (nếu in 1 mặt)
         = ⌈Số mặt / 2⌉ (nếu in 2 mặt)
3. Giá tạm = Số tờ × Đơn giá
4. Giá cuối = ⌈Giá tạm / 1000⌉ × 1000 (làm tròn lên nghìn)
```

### Ví dụ
- File PDF 10 trang, A4 màu, in 2 mặt, ghép 2 trang/mặt
- Đơn giá: 3.000đ/tờ (A4, mềm, màu, 2 mặt)

```
Số mặt = ⌈10 / 2⌉ = 5 mặt
Số tờ = ⌈5 / 2⌉ = 3 tờ
Giá tạm = 3 × 3.000 = 9.000đ
Giá cuối = ⌈9.000 / 1.000⌉ × 1.000 = 9.000đ
```

## 🐛 Khắc phục sự cố

### Lỗi khi chạy ứng dụng
**Lỗi**: `ModuleNotFoundError: No module named 'customtkinter'`  
**Giải pháp**: Cài đặt lại dependencies
```bash
pip install -r requirements.txt
```

### File Word/PowerPoint đếm sai số trang
- **Word**: Ứng dụng ước tính ~3000 ký tự/trang, có thể chênh lệch
- **PowerPoint**: Đếm theo số slide, chính xác
- **Giải pháp**: Chỉnh sửa số trang thủ công trong ứng dụng

### Folder watch không hoạt động
- Kiểm tra đường dẫn trong `config.json` có đúng không
- Đảm bảo folder tồn tại và có quyền truy cập
- Click chuột phải "Thêm File" → "Quản lý Folder" để kiểm tra

### Giá tính sai
- Kiểm tra lại cấu hình giá trong `config.json`
- Đảm bảo cấu trúc JSON đúng (key `"1"` và `"2"` phải là string)
- Giá tính theo **số tờ giấy**, không phải số trang

## 📝 Cấu trúc project

```
AutoCashier/
├── main.py              # File chính, chứa UI và logic
├── utils.py             # Hàm tiện ích (đếm trang, format tiền)
├── config.json          # Cấu hình giá và mặc định
├── requirements.txt     # Dependencies
├── setup.py             # Script cài đặt tự động
├── build_exe.py         # Script build file .exe
└── README.md            # Tài liệu này
```

## 📜 Changelog

### Version 1.0.0 (2024)
- ✨ Hỗ trợ đa định dạng: PDF, Word, PowerPoint, Excel, ảnh
- 🎯 Tính giá theo số tờ, làm tròn lên nghìn
- 📁 Theo dõi nhiều folder cùng lúc
- 👥 Tự động xóa file sau timeout (60s)
- 🪟 Mini widget always-on-top
- 🌓 Theme sáng/tối
- 🎨 Giao diện hiện đại với CustomTkinter
- ⚙️ Cấu hình linh hoạt qua JSON

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết

## 👨‍💻 Tác giả

**PCKIEN** - [@pckienuit](https://github.com/pckienuit)

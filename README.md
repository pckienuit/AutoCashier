# AutoCashier - Ứng dụng tính tiền Photocopy

Ứng dụng giúp tính tiền nhanh cho các file cần in ấn, hỗ trợ đếm trang PDF tự động.

## Cài đặt

1.  Cài đặt Python (nếu chưa có).
2.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

## Sử dụng

1.  Chạy file `main.py`:
    ```bash
    python main.py
    ```
2.  Bấm "Thêm File" để chọn các file cần tính tiền.
3.  Ứng dụng sẽ tự động đếm số trang (đối với PDF) và tính tiền mặc định.
4.  Bạn có thể chỉnh sửa số trang, khổ giấy (A4/A3), loại giấy (mềm/cứng), và màu sắc (trắng đen/màu) cho từng file.
5.  Sử dụng thanh công cụ phía trên để áp dụng chế độ in cho tất cả các file cùng lúc.
6.  Tổng tiền sẽ được hiển thị ở góc dưới bên phải.

## Cấu hình giá

Bạn có thể thay đổi bảng giá trong file `config.json`.
Cấu trúc file config:
- `prices`: Chứa giá tiền.
  - `A4` / `A3`: Khổ giấy.
    - `soft` / `hard`: Loại giấy (mềm/cứng).
      - `bw`: Trắng đen.
      - `color`: In màu.

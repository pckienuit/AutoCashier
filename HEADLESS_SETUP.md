# 🖥️ Hướng dẫn chạy AutoCashier trên môi trường Headless

Hướng dẫn này dành cho việc chạy AutoCashier trên server Linux không có GUI (headless environment) như container Docker, GitHub Codespaces, hoặc server từ xa.

## 📋 Mục lục

- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt dependencies](#cài-đặt-dependencies)
- [Phương pháp 1: noVNC (Xem qua trình duyệt)](#phương-pháp-1-novnc-xem-qua-trình-duyệt)
- [Phương pháp 2: X11 Forwarding qua SSH](#phương-pháp-2-x11-forwarding-qua-ssh)
- [Phương pháp 3: VNC Client](#phương-pháp-3-vnc-client)
- [Khắc phục sự cố](#khắc-phục-sự-cố)

---

## Yêu cầu hệ thống

- Ubuntu/Debian 20.04+
- Python 3.8+
- Quyền sudo (để cài đặt packages)

---

## Cài đặt dependencies

### 1. Cài đặt X11 libraries và Xvfb

```bash
sudo apt-get update
sudo apt-get install -y xvfb \
    libxcursor1 libxi6 libxfixes3 \
    libx11-xcb1 libxcb1 libxrandr2 \
    libxrender1 libxext6 libxft2
```

### 2. Cài đặt Python dependencies

```bash
cd /workspaces/AutoCashier
pip install -r requirements.txt
```

Các package quan trọng:
- `pyvirtualdisplay` - Tự động khởi động virtual display
- `customtkinter` - UI framework
- `tkinterdnd2` - Drag & drop support

---

## Phương pháp 1: noVNC (Xem qua trình duyệt)

**Khuyến nghị:** Cách này tốt nhất cho môi trường cloud/container.

### Bước 1: Cài đặt VNC server và noVNC

```bash
# Cài đặt x11vnc và websockify
sudo apt-get install -y x11vnc websockify python3-numpy

# Tải noVNC
cd /tmp
git clone --depth 1 https://github.com/novnc/noVNC.git
```

### Bước 2: Khởi động Xvfb (Virtual Display)

```bash
# Khởi động virtual display :99 với resolution 1280x800
pkill Xvfb  # Dừng instances cũ
rm -f /tmp/.X99-lock
Xvfb :99 -screen 0 1280x800x24 -ac &
```

**Giải thích:**
- `:99` - Display number
- `-screen 0 1280x800x24` - Screen 0, resolution 1280x800, 24-bit color
- `-ac` - Disable access control

### Bước 3: Chạy AutoCashier

```bash
cd /workspaces/AutoCashier
DISPLAY=:99 python main.py &
```

App sẽ chạy trên virtual display :99.

### Bước 4: Khởi động x11vnc

```bash
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 &
```

**Tùy chọn:**
- `-forever` - Không tự động thoát
- `-shared` - Cho phép nhiều kết nối
- `-rfbport 5900` - Port VNC (mặc định)

**Thêm mật khẩu (khuyến nghị):**
```bash
x11vnc -storepasswd
# Nhập mật khẩu khi được yêu cầu
```

Sau đó chạy với password:
```bash
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 -rfbauth ~/.vnc/passwd &
```

### Bước 5: Khởi động noVNC proxy

```bash
cd /tmp/noVNC
./utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
```

### Bước 6: Truy cập qua trình duyệt

Mở trình duyệt và truy cập:

```
http://localhost:6080/vnc.html
```

Hoặc từ máy khác (thay `<IP>` bằng IP server):
```
http://<IP-server>:6080/vnc.html
```

**Lưu ý:** Nếu đang dùng GitHub Codespaces, click vào tab "PORTS" và forward port 6080.

### Script tự động hóa

Tạo file `start_vnc.sh`:

```bash
#!/bin/bash

# Dừng các process cũ
pkill Xvfb
pkill x11vnc
pkill python

# Dọn dẹp
rm -f /tmp/.X99-lock

# Khởi động Xvfb
Xvfb :99 -screen 0 1280x800x24 -ac &
sleep 2

# Chạy AutoCashier
cd /workspaces/AutoCashier
DISPLAY=:99 python main.py &
sleep 2

# Khởi động x11vnc
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 &
sleep 2

# Khởi động noVNC
cd /tmp/noVNC
./utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

echo "✅ Hoàn tất! Truy cập: http://localhost:6080/vnc.html"
```

Chạy:
```bash
chmod +x start_vnc.sh
./start_vnc.sh
```

---

## Phương pháp 2: X11 Forwarding qua SSH

**Yêu cầu:** 
- Máy client phải có X server (Linux/Mac có sẵn, Windows cần XLaunch/VcXsrv)

### Windows

1. Tải và cài đặt [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Chạy XLaunch với tùy chọn "Disable access control"
3. SSH với X11 forwarding:

```bash
ssh -X user@server-ip
```

### Mac

1. Cài đặt XQuartz:
```bash
brew install --cask xquartz
```

2. Logout và login lại
3. SSH với X11 forwarding:

```bash
ssh -X user@server-ip
```

### Linux

```bash
ssh -X user@server-ip
```

### Chạy app

```bash
cd /workspaces/AutoCashier
python main.py
```

App sẽ hiển thị trên máy local của bạn!

---

## Phương pháp 3: VNC Client

Nếu bạn không muốn dùng noVNC, có thể dùng VNC client truyền thống:

### 1. Khởi động VNC server

```bash
# Xvfb
Xvfb :99 -screen 0 1280x800x24 -ac &

# AutoCashier
DISPLAY=:99 python main.py &

# x11vnc
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 &
```

### 2. SSH Port Forwarding

Từ máy local:

```bash
ssh -L 5900:localhost:5900 user@server-ip
```

### 3. Kết nối VNC Client

Sử dụng VNC client như:
- [RealVNC Viewer](https://www.realvnc.com/en/connect/download/viewer/)
- [TigerVNC](https://tigervnc.org/)
- [TightVNC](https://www.tightvnc.com/)

Kết nối đến: `localhost:5900` (hoặc `localhost::5900`)

---

## Khắc phục sự cố

### Lỗi: `TclError: no display name and no $DISPLAY environment variable`

**Nguyên nhân:** Chưa khởi động Xvfb hoặc chưa set DISPLAY

**Giải pháp:**
```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1280x800x24 -ac &
python main.py
```

### Lỗi: `couldn't connect to display ":99"`

**Nguyên nhân:** Xvfb chưa chạy hoặc đang chạy trên display khác

**Giải pháp:**
```bash
# Kiểm tra Xvfb đang chạy
ps aux | grep Xvfb

# Nếu không có, khởi động lại
pkill Xvfb
rm -f /tmp/.X99-lock
Xvfb :99 -screen 0 1280x800x24 -ac &
```

### Lỗi: `Server is already active for display 99`

**Giải pháp:**
```bash
# Xóa lock file
rm -f /tmp/.X99-lock

# Hoặc dùng display khác
Xvfb :100 -screen 0 1280x800x24 -ac &
export DISPLAY=:100
```

### Lỗi: `libXcursor.so.1: cannot open shared object file`

**Nguyên nhân:** Thiếu X11 libraries

**Giải pháp:**
```bash
sudo apt-get install -y libxcursor1 libxi6 libxfixes3 \
    libx11-xcb1 libxcb1 libxrandr2 libxrender1 libxext6 libxft2
```

### Lỗi: `RuntimeError: Unable to load tkdnd library`

**Nguyên nhân:** Thiếu X11 libraries cho tkinterdnd2

**Giải pháp:** Giống như trên, cài đặt đầy đủ X11 libraries

### Port 6080 bị chiếm

**Kiểm tra:**
```bash
ss -tuln | grep 6080
lsof -i :6080
```

**Giải pháp:**
```bash
# Dừng process đang dùng port
pkill -f novnc_proxy

# Hoặc dùng port khác
./utils/novnc_proxy --vnc localhost:5900 --listen 6081 &
```

### Không thấy chuột/bàn phím hoạt động

**Nguyên nhân:** noVNC chưa connect hoặc thiếu focus

**Giải pháp:**
- Click vào vùng hiển thị trước khi dùng bàn phím
- Thử refresh trang
- Kiểm tra console log trong browser (F12)

### Màn hình đen hoặc không hiển thị gì

**Kiểm tra:**
```bash
# App có đang chạy?
ps aux | grep "python main.py"

# x11vnc có hoạt động?
ps aux | grep x11vnc

# noVNC có chạy?
ps aux | grep novnc
```

**Giải pháp:**
```bash
# Restart tất cả
pkill Xvfb
pkill x11vnc
pkill python
rm -f /tmp/.X99-lock

# Chạy lại từ đầu
./start_vnc.sh
```

---

## Tối ưu hiệu suất

### Giảm độ phân giải để tăng tốc

```bash
# Thay vì 1280x800, dùng 1024x600
Xvfb :99 -screen 0 1024x600x24 -ac &
```

### Giảm color depth

```bash
# Dùng 16-bit thay vì 24-bit
Xvfb :99 -screen 0 1280x800x16 -ac &
```

### Tắt compression trong x11vnc

```bash
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 -noxdamage -noxfixes &
```

---

## Bảo mật

### 1. Thêm mật khẩu cho VNC

```bash
x11vnc -storepasswd
```

Chạy với password:
```bash
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 -rfbauth ~/.vnc/passwd &
```

### 2. Chỉ lắng nghe localhost

```bash
DISPLAY=:99 x11vnc -forever -shared -rfbport 5900 -localhost &
```

Sau đó dùng SSH port forwarding:
```bash
ssh -L 5900:localhost:5900 user@server
```

### 3. Sử dụng SSL/TLS cho noVNC

```bash
# Tạo self-signed cert
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Chạy noVNC với SSL
cd /tmp/noVNC
./utils/novnc_proxy --vnc localhost:5900 --listen 6080 --cert cert.pem --key key.pem &
```

Truy cập qua HTTPS:
```
https://localhost:6080/vnc.html
```

### 4. Firewall

Chỉ mở port cho IP cụ thể:

```bash
# Ubuntu/Debian
sudo ufw allow from <YOUR_IP> to any port 6080
sudo ufw allow from <YOUR_IP> to any port 5900

# Hoặc chặn tất cả
sudo ufw deny 6080
sudo ufw deny 5900
```

---

## Script quản lý tự động

Tạo file `autocashier-vnc.sh`:

```bash
#!/bin/bash

ACTION="${1:-start}"
DISPLAY_NUM=99
VNC_PORT=5900
NOVNC_PORT=6080
APP_DIR="/workspaces/AutoCashier"

case $ACTION in
    start)
        echo "🚀 Khởi động AutoCashier VNC..."
        
        # Dọn dẹp
        pkill Xvfb 2>/dev/null
        pkill x11vnc 2>/dev/null
        rm -f /tmp/.X${DISPLAY_NUM}-lock
        
        # Xvfb
        echo "  ✓ Khởi động Xvfb :${DISPLAY_NUM}..."
        Xvfb :${DISPLAY_NUM} -screen 0 1280x800x24 -ac &
        sleep 2
        
        # AutoCashier
        echo "  ✓ Khởi động AutoCashier..."
        cd "$APP_DIR"
        DISPLAY=:${DISPLAY_NUM} python main.py &
        sleep 2
        
        # x11vnc
        echo "  ✓ Khởi động x11vnc (port ${VNC_PORT})..."
        DISPLAY=:${DISPLAY_NUM} x11vnc -forever -shared -rfbport ${VNC_PORT} &
        sleep 2
        
        # noVNC
        if [ -d "/tmp/noVNC" ]; then
            echo "  ✓ Khởi động noVNC (port ${NOVNC_PORT})..."
            cd /tmp/noVNC
            ./utils/novnc_proxy --vnc localhost:${VNC_PORT} --listen ${NOVNC_PORT} &
        else
            echo "  ⚠ noVNC không tìm thấy. Bỏ qua."
        fi
        
        echo ""
        echo "✅ Hoàn tất!"
        echo "   📺 Truy cập: http://localhost:${NOVNC_PORT}/vnc.html"
        echo "   🔌 VNC: localhost:${VNC_PORT}"
        ;;
        
    stop)
        echo "🛑 Dừng AutoCashier VNC..."
        pkill Xvfb
        pkill x11vnc
        pkill -f "python main.py"
        pkill -f novnc_proxy
        rm -f /tmp/.X${DISPLAY_NUM}-lock
        echo "✅ Đã dừng tất cả services"
        ;;
        
    restart)
        echo "🔄 Khởi động lại..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        echo "📊 Trạng thái services:"
        echo ""
        
        echo -n "  Xvfb: "
        pgrep -f "Xvfb :${DISPLAY_NUM}" > /dev/null && echo "✓ Đang chạy" || echo "✗ Không chạy"
        
        echo -n "  AutoCashier: "
        pgrep -f "python main.py" > /dev/null && echo "✓ Đang chạy" || echo "✗ Không chạy"
        
        echo -n "  x11vnc: "
        pgrep -f "x11vnc" > /dev/null && echo "✓ Đang chạy" || echo "✗ Không chạy"
        
        echo -n "  noVNC: "
        pgrep -f "novnc_proxy" > /dev/null && echo "✓ Đang chạy" || echo "✗ Không chạy"
        
        echo ""
        echo "  Ports:"
        ss -tuln | grep -E "(${VNC_PORT}|${NOVNC_PORT})" | sed 's/^/    /'
        ;;
        
    logs)
        echo "📝 Logs (Ctrl+C để thoát):"
        echo ""
        tail -f /tmp/.X${DISPLAY_NUM}-lock 2>/dev/null || echo "Không có logs"
        ;;
        
    *)
        echo "Cách dùng: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Ví dụ:"
        echo "  $0 start    - Khởi động tất cả services"
        echo "  $0 stop     - Dừng tất cả services"
        echo "  $0 restart  - Khởi động lại"
        echo "  $0 status   - Kiểm tra trạng thái"
        exit 1
        ;;
esac
```

Sử dụng:

```bash
chmod +x autocashier-vnc.sh

# Khởi động
./autocashier-vnc.sh start

# Kiểm tra trạng thái
./autocashier-vnc.sh status

# Dừng
./autocashier-vnc.sh stop

# Khởi động lại
./autocashier-vnc.sh restart
```

---

## Systemd Service (Tự động khởi động)

Tạo file `/etc/systemd/system/autocashier-vnc.service`:

```ini
[Unit]
Description=AutoCashier VNC Service
After=network.target

[Service]
Type=forking
User=codespace
WorkingDirectory=/workspaces/AutoCashier
ExecStart=/workspaces/AutoCashier/autocashier-vnc.sh start
ExecStop=/workspaces/AutoCashier/autocashier-vnc.sh stop
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Kích hoạt:

```bash
sudo systemctl daemon-reload
sudo systemctl enable autocashier-vnc
sudo systemctl start autocashier-vnc

# Kiểm tra
sudo systemctl status autocashier-vnc
```

---

## Docker Support

Tạo `Dockerfile`:

```dockerfile
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    xvfb x11vnc websockify \
    libxcursor1 libxi6 libxfixes3 \
    libx11-xcb1 libxcb1 libxrandr2 \
    libxrender1 libxext6 libxft2 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone noVNC
RUN cd /tmp && git clone --depth 1 https://github.com/novnc/noVNC.git

# Set working directory
WORKDIR /app

# Copy application
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5900 6080

# Start script
COPY docker-start.sh /app/
RUN chmod +x /app/docker-start.sh

CMD ["/app/docker-start.sh"]
```

Tạo `docker-start.sh`:

```bash
#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1280x800x24 -ac &
export DISPLAY=:99
sleep 2

# Start AutoCashier
python3 main.py &
sleep 2

# Start x11vnc
x11vnc -forever -shared -rfbport 5900 -display :99 &
sleep 2

# Start noVNC
cd /tmp/noVNC
./utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

# Keep container running
tail -f /dev/null
```

Build và chạy:

```bash
docker build -t autocashier-vnc .
docker run -d -p 6080:6080 -p 5900:5900 --name autocashier autocashier-vnc
```

---

## FAQ

### Q: Tại sao cần Xvfb?

**A:** Xvfb (X Virtual FrameBuffer) tạo một màn hình ảo trong bộ nhớ, cho phép chạy ứng dụng GUI trên server không có màn hình thật.

### Q: noVNC vs VNC client, dùng cái nào?

**A:** 
- **noVNC**: Xem qua browser, không cần cài đặt, tiện cho cloud/container
- **VNC client**: Hiệu suất tốt hơn, ít lag hơn, cần cài phần mềm

### Q: Có cách nào chạy AutoCashier không cần GUI không?

**A:** Không, vì AutoCashier sử dụng CustomTkinter (GUI framework). Cần môi trường có X server để chạy.

### Q: Làm sao để nhiều người cùng xem?

**A:** Dùng option `-shared` trong x11vnc và cho nhiều người truy cập cùng URL noVNC.

### Q: Có thể chạy nhiều instance AutoCashier không?

**A:** Có, dùng display numbers khác nhau:

```bash
# Instance 1
Xvfb :99 -screen 0 1280x800x24 -ac &
DISPLAY=:99 python main.py &
DISPLAY=:99 x11vnc -rfbport 5900 &

# Instance 2
Xvfb :100 -screen 0 1280x800x24 -ac &
DISPLAY=:100 python main.py &
DISPLAY=:100 x11vnc -rfbport 5901 &
```

---

## Tài liệu tham khảo

- [Xvfb Manual](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml)
- [x11vnc Documentation](http://www.karlrunge.com/x11vnc/)
- [noVNC GitHub](https://github.com/novnc/noVNC)
- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)

---

## Hỗ trợ

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra [Khắc phục sự cố](#khắc-phục-sự-cố)
2. Chạy `./autocashier-vnc.sh status` để xem trạng thái
3. Kiểm tra logs: `journalctl -u autocashier-vnc -f`
4. Tạo issue trên GitHub: [AutoCashier Issues](https://github.com/pckienuit/AutoCashier/issues)

---

**Made with ❤️ for headless environments**

# Kingdom Game - Portable Edition Builder

## Tổng quan
Bộ công cụ này giúp bạn tạo ra một phiên bản portable của Kingdom Game có thể chạy được mà không cần cài đặt Python và tránh bị Microsoft nhận diện là phần mềm độc hại.

## Các file đã tạo

### 1. Scripts chính:
- `build_complete.py` - Script tổng hợp để build toàn bộ game portable
- `build_portable.py` - Script để build executable bằng PyInstaller
- `prepare_signature.py` - Script để chuẩn bị digital signature
- `build_installer.py` - Script để tạo installer bằng Inno Setup
- `test_portable.py` - Script để test game portable

### 2. Files cấu hình:
- `kingdom_game.spec` - File cấu hình PyInstaller
- `installer/KingdomGame.iss` - Script Inno Setup
- `installer/LICENSE.txt` - License file
- `installer/README.txt` - README cho installer

## Cách sử dụng

### Bước 1: Chuẩn bị môi trường
```bash
# Đảm bảo bạn có Python 3.7+
python --version

# Cài đặt PyInstaller
pip install pyinstaller
```

### Bước 2: Build game portable
```bash
# Chạy script tổng hợp (khuyến nghị)
python build_complete.py

# Hoặc chạy từng bước:
python build_portable.py
python prepare_signature.py
python test_portable.py
```

### Bước 3: Kiểm tra kết quả
Sau khi build thành công, bạn sẽ có:
- `KingdomGame_Portable/` - Thư mục chứa game portable
- `distribution/` - Thư mục chứa package phân phối
- `KingdomGame_Portable/KingdomGame.exe` - File executable chính

## Các tính năng đã implement

### ✅ Loại bỏ dependencies bên ngoài
- Đã loại bỏ PIL/Pillow dependency
- Chỉ sử dụng các module built-in của Python
- Game hoàn toàn độc lập

### ✅ Tạo executable portable
- Sử dụng PyInstaller để tạo .exe file
- Không cần cài đặt Python trên máy người dùng
- Tự động đóng gói tất cả dependencies

### ✅ Tránh bị nhận diện là malware
- Tạo application manifest
- Thêm version information
- Hướng dẫn người dùng thêm vào Windows Defender exclusions
- Cung cấp hướng dẫn code signing

### ✅ Tạo installer chuyên nghiệp
- Script Inno Setup để tạo installer
- Hỗ trợ desktop shortcut
- Uninstaller tự động
- License và README tích hợp

### ✅ Testing và verification
- Script test tự động
- Kiểm tra executable size và compatibility
- Tạo test report chi tiết

## Cấu trúc thư mục sau khi build

```
KingdomGame_Portable/
├── KingdomGame.exe          # File executable chính
├── README.txt               # Hướng dẫn sử dụng
├── TEST_REPORT.txt          # Báo cáo test
└── WINDOWS_DEFENDER_GUIDE.txt # Hướng dẫn Windows Defender

distribution/
├── KingdomGame_Portable/    # Thư mục portable
├── KingdomGame_Portable_v1.0.0.zip # File ZIP portable
└── DISTRIBUTION_README.txt  # Hướng dẫn phân phối
```

## Hướng dẫn phân phối

### Cho người dùng cuối:
1. **Tải về**: `KingdomGame_Portable_v1.0.0.zip`
2. **Giải nén**: Extract vào thư mục bất kỳ
3. **Chạy game**: Double-click `KingdomGame.exe`
4. **Windows Defender**: Thêm thư mục vào exclusions nếu cần

### Lưu ý quan trọng:
- Game có thể bị Windows Defender cảnh báo (false positive)
- Cung cấp hướng dẫn chi tiết cho người dùng
- Khuyến khích test trên nhiều máy khác nhau

## Troubleshooting

### Lỗi thường gặp:

1. **PyInstaller không tìm thấy**
   ```bash
   pip install pyinstaller
   ```

2. **Executable quá lớn**
   - Kiểm tra excludes trong spec file
   - Loại bỏ các module không cần thiết

3. **Windows Defender cảnh báo**
   - Thêm vào exclusions
   - Cân nhắc code signing certificate

4. **Game không chạy**
   - Kiểm tra Windows version compatibility
   - Test trên máy clean (không có Python)

## Code Signing (Tùy chọn)

Để tránh hoàn toàn cảnh báo Windows Defender:

1. **Self-signed certificate** (miễn phí nhưng hạn chế)
2. **Commercial certificate** ($200-500/năm)
3. **Let's Encrypt** (miễn phí, phức tạp)

Xem `prepare_signature.py` để biết chi tiết.

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra `TEST_REPORT.txt`
2. Chạy `test_portable.py`
3. Xem logs trong quá trình build
4. Liên hệ qua GitHub Issues

## Kết luận

Bộ công cụ này đã tạo ra một phiên bản portable hoàn chỉnh của Kingdom Game:
- ✅ Không cần cài đặt Python
- ✅ Tránh được phần lớn cảnh báo malware
- ✅ Dễ dàng phân phối và sử dụng
- ✅ Professional installer
- ✅ Testing và verification đầy đủ

Game sẵn sàng để phân phối cho người dùng!

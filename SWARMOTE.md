# Nghiên cứu và tích hợp Swarmote

## Hành vi có bằng chứng

- [Hướng dẫn chính thức của Swarmote](https://www.swarmote.cn/web/help) mô tả mỗi Profile là một điện thoại Android đám mây độc lập. Proxy là cấu hình mạng gán cho Profile. App Store của Swarmote hỗ trợ cài Amazon Shopping trực tiếp vào Profile.
- Ảnh do người dùng cung cấp cho thấy Profile 3 đang có Amazon Shopping 32.2.0.100 với trạng thái `Installed`. Ảnh không chứng minh nguồn APK hoặc khả năng điều khiển bằng ADB.
- Phân tích tĩnh bản Swarmote đang cài tại `C:\Users\David\AppData\Local\Programs\Swarmote\resources\app.asar` (SHA-256 `a6c5bd14a98c3a67da85061c53ff8b7bda799a74f86bf1915e018a17e64aebf2`, REA Evidence `ev_22ceffcfb898a5a1587170d3b4b7a53e677266d2bf749b4ccc3e847c7adb838b`) cho thấy Terminal tạo đường hầm SSH tới ADB và đặt serial tại `127.0.0.1:<localPort>`. Mã này nằm ở `dist-electron/main/index-DwxZtFR-.js`, quanh dòng 4833–4968 của bản đã giải gói. Terminal nhận thông tin kết nối do Swarmote cấp; công cụ của dự án không truy cập thông tin đó.
- Swarmote đóng gói ADB riêng tại `resources/adb/bin/win/adb.exe`. Cấu trúc chương trình còn có WebSocket nội bộ cho Terminal, quanh dòng 5171–5239. Đây là quan sát tĩnh; không chứng minh kết nối tới Profile hiện tại đã được mở.
- ADB của Swarmote là bản 36.0.0, còn Android SDK vừa cài là bản 37.0.1. Hai phiên bản cùng dùng ADB server mặc định có thể thay thế tiến trình server của nhau. Vì vậy các lệnh emulator cục bộ của dự án dùng cổng ADB server 5038; chế độ Swarmote dùng ADB đi kèm ứng dụng ở cổng mặc định 5037.

## Phần đã áp dụng

- `python -m amazon_android.cli cloud-scan`: dùng ADB đóng gói cùng Swarmote, chỉ nhận thiết bị loopback xuất hiện trong `adb devices` **và** có cổng lắng nghe thuộc tiến trình Swarmote, rồi hỏi Android Package Manager và `getprop` để lấy trạng thái. Khi không có tunnel, trả danh sách trống.
- `python -m amazon_android.cli cloud-open-amazon 127.0.0.1:PORT`: kiểm tra thiết bị, package Amazon, boot status; mở ứng dụng rồi kiểm tra tiến trình và cửa sổ trước.
- Không đọc khóa SSH, không gọi API riêng chưa công bố, không lưu mật khẩu/OTP. Trường `source_verified` luôn `false` cho tới khi có bằng chứng nguồn cài độc lập; metadata `installer` của Android không đủ chứng minh Google Play.

## Kiểm thử còn lại

Đã mở `Terminal > ADB Shell` trên Profile 6 và kiểm chứng `cloud-scan` cùng `cloud-open-amazon` trên điện thoại thật ngày 2026-11-12. Cổng tunnel là tạm thời. App Center Swarmote cài trực tiếp từ kho của họ, nên không thể báo đạt yêu cầu gốc “cài từ Google Play” chỉ dựa trên nút `Installed`.

Sau đó, đã dùng UI Automation nền tạo Profile `Amazon 01` với proxy do người dùng cung cấp, mở ADB Shell, cài Amazon từ App Store Swarmote, xác minh package và mở màn bắt đầu đăng ký. Luồng này không dùng chuột Windows. Việc khởi chạy Profile từ Offline chưa được kiểm chứng qua mã; Profile đã chạy khi kiểm tra. Chưa hoàn tất đăng ký vì chưa có dữ liệu tài khoản và OTP/CAPTCHA sẽ cần người dùng xử lý.

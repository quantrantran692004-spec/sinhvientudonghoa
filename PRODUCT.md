# Amazon trên Swarmote

## Người dùng và công việc

- Người dùng tự chuẩn bị proxy và thông tin đăng ký, muốn nhập vào phần mềm của mình thay vì gửi từng bộ trong chat.
- Một thao tác có thể chuẩn bị 1–12 điện thoại Swarmote; người dùng muốn lặp lại các mẻ có kích thước khác nhau.
- Công cụ tạo Profile, gán proxy, mở điện thoại và cài Amazon Shopping. q1 và q2 đã có b1–b3 riêng rồi dùng chung b4–b11 tới OTP SMS theo ảnh người dùng nhưng chưa thử thật; q3–q12 vẫn dừng ở menu ba gạch. SĐT, mật khẩu, tên, thẻ và URL OTP của mỗi hàng được gắn với đúng máy và giữ trong bộ nhớ phiên; thẻ chưa được dùng trong luồng hiện tại.

## Nền tảng

- Windows desktop, chạy cùng ứng dụng Swarmote đã đăng nhập.
- Điều khiển Swarmote bằng UI Automation nền; điều khiển điện thoại bằng ADB qua tunnel của Swarmote.
- Mật khẩu chỉ giữ trong bộ nhớ phiên, không ghi SQLite hay log.

## Điều chưa xác minh

- Biểu mẫu tên/mật khẩu của Amazon sau bước Continue chưa có thử nghiệm thật.
- Khởi chạy Profile từ Offline và một mẻ 5 máy chưa được thử end-to-end.
- Giới hạn slot Profile và tính năng tạo hàng loạt riêng của Swarmote chưa được kiểm chứng cho bản đang cài.

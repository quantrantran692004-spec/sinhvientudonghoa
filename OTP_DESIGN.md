# Thiết kế OTP cho từng Profile

## Đã chuẩn bị

- Bảng Amazon nhận `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`. Hàng n gắn với Máy n / Profile qN. Bản sao Markdown có thể có cột trống xen giữa, dấu `\|` trong thẻ và URL dạng link; parser vẫn lấy thẻ và URL cùng hàng, không đưa thẻ vào luồng OTP. URL phải thuộc endpoint HTTPS `apifc.net/smsrecord` và token không được trùng giữa các máy.
- Giao diện cho xem SĐT, dấu hiệu URL được gán và đuôi token theo từng hàng; chọn máy để kiểm tra URL đầy đủ. Trạng thái khởi đầu là **Chưa yêu cầu mã**. Khi có mã, khu vực OTP của máy đó có thể hiện mã và nút **Sao chép**.
- `amazon_android/otp.py` cung cấp `read_otp(url)` và `wait_for_new_otp(url, previous_code)`. Nó chỉ nhận sáu chữ số trong mẫu `yes|Amazon: 123456 is your sign-in code.`; không đưa URL, token hay nội dung SMS vào lỗi. Hai lời gọi chờ trên hai URL chạy độc lập.
- Khi bắt đầu mẻ, từng `RunJob` giữ bản dữ liệu Amazon và URL OTP bất biến của chính hàng đó trong bộ nhớ. Worker sau này sẽ dùng bản này, không đọc ô nhập liệu đang được chọn trên giao diện.
- **Làm lại / mẻ mới** xóa URL, mã và trạng thái OTP của toàn bộ hàng trong bộ nhớ phiên cùng với dữ liệu Amazon và proxy. Profile Swarmote đã tạo không bị xóa bởi thao tác này.

## Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon

1. Runner lấy bản dữ liệu bất biến của hàng: `batch_id`, `slot`, Profile, SĐT, mật khẩu, tên, thẻ và URL OTP. Nó chỉ thao tác trên điện thoại có Device ID/ADB serial của hàng đó. Thẻ hiện chỉ được gắn dữ liệu, chưa dùng trong các bước b1–b11.
2. Sau khi nhận diện đúng form, runner điền thông tin. Ngay trước nút gửi OTP, gọi `read_otp(url)` để ghi nhận mã cũ. Nếu không đọc được URL, dừng hàng này trước khi gửi.
3. Runner bấm gửi OTP, xác nhận màn hình nhập mã rồi gọi `wait_for_new_otp(url, previous_code)`. Chờ tối đa 30 giây, kiểm tra khoảng mỗi giây. Mã bằng mã cũ tiếp tục được xem là đang chờ.
4. Mã mới được chuyển về đúng hàng bằng `batch_id` và `slot`, hiện cho người dùng quan sát, rồi nhập vào ô OTP của cùng điện thoại. Chỉ bấm xác nhận nếu nhận diện được duy nhất ô và nút đúng. Trạng thái hiện chỉ ghi đã xong các bước được hướng dẫn; chưa xác nhận tài khoản thành công.
5. Màn hình khác dự kiến, CAPTCHA, URL lỗi hoặc hết thời gian chờ làm hàng đó dừng và báo lý do. Các máy khác vẫn chạy độc lập.

q1 và q2 đã nối bước chọn **Send code by SMS**, đọc URL của chính hàng và gõ mã SMS vào ô `Enter security code`. Các luồng mới qua kiểm thử mô phỏng; chưa xác minh cây giao diện thực tế trên q1/q2. q3–q12 chưa có bước sau menu. Màn sau nút Create chưa được hướng dẫn, nên không báo tài khoản tạo thành công khi mới bấm nút.

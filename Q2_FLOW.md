# Luồng q2 từ menu ba gạch

Nguồn: hai ảnh người dùng gửi ngày 13/11/2026. q2 bắt đầu ở menu ba gạch do phần chuẩn bị điện thoại đưa tới. Chỉ b1–b3 riêng q2; b4–b11 dùng `build_common_steps` như q1, với SĐT, URL OTP, trạng thái và đồng hồ riêng.

| Bước | Hành động | Kiểm tra |
| --- | --- | --- |
| b1 | Bấm tab biểu tượng nhà ở thanh dưới. Xem trang chủ trong một khoảng chọn từ 2, 3, 4, 5 giây. | Xác nhận trang chủ bằng chữ `Sign in for the best experience` hoặc tab Home được chọn. Nếu chưa chuyển màn, dừng tại b1. |
| b2 | Bấm tab menu ba gạch ở thanh dưới. | Xác nhận `Shop by category` hoặc hàng Sign In/Customer Service của menu. |
| b3 | Bấm thẻ `Pets`. | Tìm thẻ theo chữ trong cây UI hiện tại; nếu phải cuộn thì dùng kích thước màn hiện tại. |
| b4–b11 | Luồng chung: Sign In, nhập số, US +1, tạo tài khoản, chọn SMS, lấy OTP từ URL cùng hàng, nhập OTP, bấm Create. | Xem [Q1_FLOW.md](Q1_FLOW.md) và [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md). |

Nếu màn hình khác ảnh hoặc phần tử không xác định duy nhất, q2 dừng tại bước hiện tại để người dùng sửa rồi bấm **Tiếp tục**. Đồng hồ riêng của q2 bắt đầu từ menu ba gạch, chu kỳ 3–4–5–4 phút. Chưa thử b1–b11 trên q2 thật; ảnh không xác nhận màn sau Create.

Người dùng báo q2 đã tới menu ba gạch rồi đứng; trạng thái trong tool chỉ ghi đã tới menu, không có lỗi. Khi một mẻ cũ đã lưu `MENU_OPEN`, runner trước đây phát sự kiện `done` nhưng không nối lại ADB serial, làm `_start_post_menu` bỏ qua b1. Nhánh này đã được sửa: q2 Running có dữ liệu Amazon sẽ nối ADB trước khi chạy b1; nếu thiếu dữ liệu hoặc serial, tool hiện lý do ở hàng Máy 2. Nếu q2 Offline, tool nhắc Start rồi bấm Tiếp tục. Đây là kết luận từ mã và test mô phỏng, **chưa xác minh là nguyên nhân duy nhất của lần dừng thật**.

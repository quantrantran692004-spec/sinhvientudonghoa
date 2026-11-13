# Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

**Chưa có toàn bộ quy trình.** Những ảnh đã gửi chỉ mô tả các mốc dưới đây. Mỗi ảnh tiếp theo của người dùng có thể bổ sung hoặc sửa một mốc; phải cập nhật file này, tài liệu máy tương ứng và mã trước khi nói máy đó đã hoàn tất. Không suy diễn màn sau ảnh cuối.

## Phần dùng chung đã được hướng dẫn

Menu ba gạch có hai bố cục đã biết. Với menu dạng thẻ, q1/q2 chạy b1–b3 riêng. Với menu dạng danh sách, sau khi nhận diện qua cây UI Android, tool bấm Home, chỉ xem 2–5 giây, trở lại menu và tiếp tục b4 Sign In; quy tắc này dùng cho mọi máy đã được nối sau menu. Xem [MENU_ROUTING.md](MENU_ROUTING.md). Chưa thử nhánh mới trên máy thật.

Từ **b4 Sign In** ở menu ba gạch: nhập số của đúng hàng, chọn `United States +1`, Continue, xác nhận tài khoản mới, nhập tên, chọn **Send code by SMS** thay WhatsApp, lấy OTP mới từ URL riêng của hàng, gõ từng số vào form SMS rồi bấm **Create your Amazon account**. Ảnh cuối dừng ở màn nhập OTP SMS và nút Create; **chưa có ảnh màn sau khi bấm Create**, chưa biết điều kiện xác nhận tài khoản đã tạo thành công. Mật khẩu và thẻ có trong hàng dữ liệu nhưng ảnh hiện tại chưa có màn cần nhập chúng. Luồng chung được mã hóa tại `build_common_steps` trong `amazon_android/account_flow.py` và được gọi riêng cho từng máy.

## Phần riêng từng máy

| Máy | Ảnh/mốc đã hướng dẫn | Đã nối trong mã | Đã thử trên máy thật | Phần còn thiếu |
| --- | --- | --- | --- | --- |
| q1 | Chín ảnh ban đầu đánh dấu b1–b11; thêm năm ảnh ngày 13/11: form SĐT, lỗi b6/b9/b10. Ảnh chọn quốc gia ban đầu có tiêu đề q6 nên chỉ là ví dụ UI. | Có: `build_q1_steps` + luồng chung đã sửa b4/b6/b9/b10 và Tiếp tục. | Người dùng đã thử q1 và gửi lỗi ở b6, b9, b10; sửa mới chưa được thử lại thật. | Xác minh sửa trên q1, URL OTP sau gửi và màn sau Create. |
| q2 | Hai ảnh: b1 bấm tab nhà và xem 2–5 giây; b2 bấm menu ba gạch; b3 bấm Pets. | Có: `build_q2_steps` + luồng chung; đã sửa nhánh nối lại ADB từ menu lưu trước. | Người dùng thấy q2 tới menu rồi đứng, tool chỉ ghi đã tới menu. Sửa mới chưa thử lại thật. | Xác minh q2 tự bấm Home sau menu, locator/UI thực tế và màn sau Create. |
| q3–q12 | Chưa nhận ảnh b1–b3 riêng của từng máy. | Chưa bật sau menu; vẫn dừng tại menu ba gạch. | Chưa. | Người dùng hướng dẫn b1–b3 từng máy. |

## Cách xử lý ảnh tiếp theo

1. Ghi máy nào, mốc nào, chữ/điều khiển thấy trên ảnh, kết quả mong đợi và các biến thể UI có thể xảy ra. Không sao chép tọa độ ảnh vào mã.
2. Xác định ảnh đó **thêm bước mới**, **thay bước cũ** hay chỉ là **màn kiểm tra**. Nếu ảnh không đủ để phân biệt, dừng ở bước đó để người dùng chỉ tiếp.
3. Cập nhật `Q1_FLOW.md` hoặc `Q2_FLOW.md` (hay tạo file Qn mới), `PROJECT_HANDOFF.md`, test cần thiết, rồi chạy `python -m graphify update .` và `python -m graphify tree`.
4. Báo riêng kết quả test mô phỏng và kết quả máy thật. Không dùng “đã tạo tài khoản thành công” khi chỉ thấy bấm Create hoặc rời màn OTP.

Mười sáu ảnh q1/q2 và một ảnh menu chung đã được lưu và ánh xạ tới bước trong [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Graphify hiện chỉ lập chỉ mục tiêu đề/link, không trích xuất pixel; phải mở ảnh khi phân tích chi tiết. File này vẫn chỉ ghi **nội dung đã được người dùng hướng dẫn**, không khẳng định ảnh đã đủ toàn bộ quy trình.

Người dùng gửi thêm sáu ảnh q1: dropdown quốc gia ở đầu chữ A lúc báo lỗi b6, form tên đang mở bàn phím lúc báo nhiều Continue ở b9, và màn WhatsApp chưa bấm SMS lúc tool báo HTTP 403 ở b10. Bản mã hiện tại đã có lọc bounds cho b6, lọc nút Continue nhìn thấy ở b9 và chỉ đọc URL ở b11. Có test hồi quy mới, nhưng **chưa xác minh tiến trình tool trên màn đang nạp bản mã này**; không tự khởi động lại vì dữ liệu mẻ chỉ ở RAM.

Ảnh q1 mới cho thấy b4 trên menu danh sách dừng vì nhiều nhãn Sign In trong cây UI. Đã sửa bộ chọn chung để ưu tiên node có thể bấm, rồi dùng Customer Service làm mốc khi cần; giữ dừng an toàn nếu vẫn không phân biệt được. Chưa có lượt chạy thật sau sửa.

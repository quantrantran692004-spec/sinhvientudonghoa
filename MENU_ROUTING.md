# Điều hướng hai dạng menu ba gạch

## Bằng chứng và phạm vi

Ảnh mới [menu dạng danh sách](flow_images/shared/01_list_menu.png) hiển thị `Shop by Category`, Books, Electronics, Home services, See all, Today's Deals, Try Prime, Settings, Customer Service và Sign In. Người dùng xác nhận: gặp dạng này thì bấm Home, **chỉ xem 2–5 giây**, trở lại menu rồi bấm Sign In ở b4. Không cuộn Home. Ảnh này là bằng chứng thiết kế; chưa có lượt chạy thật trên Swarmote sau khi sửa. Các ảnh menu dạng thẻ của q1/q2 vẫn ở [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

## Quy tắc chạy

1. Sau khi xác nhận menu ba gạch trên ADB serial của máy, khởi động đồng hồ riêng của lượt (3→4→5→4 phút). Đọc cây `uiautomator dump` hiện tại. `screen` và `menu_layout` trong `amazon_android/account_flow.py` phân loại màn và bố cục theo chữ/content description; không so khớp pixel ảnh hay tọa độ cố định.
2. Dạng thẻ: q1 chạy Gifting → Pets → Fashion and Beauty; q2 chạy Home 2–5 giây → menu → Pets. Chỉ các máy đã có b1–b3 riêng được chạy sau menu.
3. Dạng danh sách: `route_list_menu` ghi nhánh cho phiên máy, bấm tab Home từ cây UI có bounds hợp lệ, xác nhận Home, chờ 2–5 giây trong thời hạn lượt, rồi chuyển `next_step` sang b4. b4 dùng `_ensure_menu` để bấm tab menu ba gạch trở lại, tìm Sign In trong cây UI (cuộn menu nếu cần), bấm và xác nhận form số điện thoại. Không chạy lại b1–b3 dạng thẻ trên nhánh này.
4. Nếu người dùng sửa màn rồi bấm Tiếp tục, tool đọc lại UI. Nhánh danh sách được giữ trong phiên để tiếp tục được cả khi máy đang ở Home sau lần dừng; nếu thấy menu dạng thẻ thì bỏ nhánh danh sách. Lỗi đọc cây, màn lạ, nhiều điều khiển cùng khớp, hoặc hết hạn đều dừng máy đó tại bước hiện tại để sửa trực tiếp. Không gửi OTP hoặc bấm Create trong bước điều hướng này.
5. b4–b11 là một bộ bước chung với SĐT, URL OTP, trạng thái SMS, mã, đồng hồ và điểm dừng riêng cho từng máy. q3–q12 chưa có hướng dẫn b1–b3 và vẫn dừng ở menu, dù bộ phân loại có thể dùng lại khi các máy này được nối về sau.

Ở b4, menu có thể trả nhiều node cùng nhãn `Sign In` dù chỉ một hàng nhìn thấy. Bộ chọn chung ưu tiên node `clickable`; nếu nhãn vẫn lặp, dùng hàng `Customer Service` đang hiện ngay phía trên làm mốc và chỉ nhận một Sign In nằm dưới. Khi vẫn mơ hồ, tool dừng để sửa trên máy. Ảnh lỗi q1 ở [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

## Kiểm chứng

Test mô phỏng kiểm tra phân loại hai bố cục, q1/q2 bỏ qua b1–b3 khi gặp danh sách, giữ các bước riêng khi gặp thẻ, hồi phục từ Home và b4 quay lại menu trước Sign In. Chưa có ADB của q1/q2 trong môi trường kiểm tra hiện tại, nên kết quả trên máy thật và các biến thể UI khác chưa được xác nhận. Khi có dump thực tế, đối chiếu chữ, `content-desc`, trạng thái chọn và vùng bấm rồi sửa bộ phân loại chung nếu cần.

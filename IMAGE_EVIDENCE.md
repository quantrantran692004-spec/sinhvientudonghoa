# Ảnh hướng dẫn q1/q2 và menu chung lưu cục bộ

Các ảnh người dùng gửi đã được sao chép vào `flow_images/` để phiên sau xem lại pixel. Ảnh được lưu cùng mã nguồn theo yêu cầu bàn giao đầy đủ; repository GitHub hiện là **công khai** và ảnh có thể hiển thị SĐT hoặc OTP đã xuất hiện trong ảnh gốc. Không chép lại các giá trị này sang log hoặc tài liệu. Graphify chỉ lập chỉ mục các tiêu đề và liên kết dưới đây, **không đọc nội dung pixel**.

## q1 ảnh 01 — Menu và ba thẻ

[01_menu_cards.png](flow_images/q1/01_menu_cards.png): Gifting, Pets, Fashion and Beauty được đánh dấu b1–b3.

## q1 ảnh 02 — Sign In cuối menu

[02_sign_in_menu.png](flow_images/q1/02_sign_in_menu.png): hàng Sign In b4.

## q1 ảnh 03 — Nhập số điện thoại

[03_phone_input.png](flow_images/q1/03_phone_input.png): form nhập số b5.

## q1 ảnh 04 — Chọn mã quốc gia

[04_country_reference_q6.png](flow_images/q1/04_country_reference_q6.png): United States +1 b6. Tiêu đề cửa sổ trong ảnh là **q6**, nên đây là tham chiếu giao diện cho q1, chưa phải bằng chứng q1 thật.

## q1 ảnh 05 — Continue số điện thoại

[05_continue_number.png](flow_images/q1/05_continue_number.png): nút Continue b7.

## q1 ảnh 06 — Tạo tài khoản mới

[06_new_account.png](flow_images/q1/06_new_account.png): Proceed to create an account b8.

## q1 ảnh 07 — Form tên

[07_name_form.png](flow_images/q1/07_name_form.png): First and last name b9.

## q1 ảnh 08 — Chọn SMS thay WhatsApp

[08_whatsapp_sms_choice.png](flow_images/q1/08_whatsapp_sms_choice.png): Send code by SMS b10.

## q1 ảnh 09 — Nhập OTP SMS

[09_sms_otp.png](flow_images/q1/09_sms_otp.png): Verify mobile number, ô OTP SMS và nút Create b11. **Chưa có ảnh sau khi bấm Create.**

## q1 ảnh 10 — Form SĐT hiện tại

[10_identifier_current.png](flow_images/q1/10_identifier_current.png): q1 ở màn `Sign in or create account` với ô SĐT trống. Người dùng xác nhận đây là màn hiện tại sau các lần dừng. Khi bấm Tiếp tục, luồng chung cần đọc lại màn, quay về b4 và chạm ô trước khi gõ.

## q1 ảnh 11 — Lỗi b6 vùng bấm

[11_b6_invalid_region.png](flow_images/q1/11_b6_invalid_region.png): thông báo `Vùng bấm Amazon không hợp lệ` khi chọn US +1. Cây UI có thể có mục US ẩn hoặc bounds bằng 0; cần cuộn đến mục đang hiển thị thay vì bấm mục ẩn.

## q1 ảnh 12 — Lỗi b9 Continue

[12_b9_continue_ambiguous.png](flow_images/q1/12_b9_continue_ambiguous.png): thông báo có nhiều phần tử `Continue`. Chọn nút đang hiển thị, có thể bấm và thuộc form tên.

## q1 ảnh 13 — Lỗi URL OTP ở b10

[13_b10_otp_http403.png](flow_images/q1/13_b10_otp_http403.png): URL OTP trả HTTP 403 trước khi tool gửi SMS. Người dùng yêu cầu bấm gửi SMS trước, rồi mới đọc URL.

## q1 ảnh 14 — Lỗi b10 màn không khớp

[14_b10_not_whatsapp.png](flow_images/q1/14_b10_not_whatsapp.png): b10 báo q1 chưa ở màn chọn SMS; cần đọc lại màn hiện tại khi Tiếp tục và quay về đúng bước chung của máy này.

## q2 ảnh 01 — Trang chủ

[01_home.png](flow_images/q2/01_home.png): b1 bấm tab nhà, xem 2–5 giây.

## q2 ảnh 02 — Menu và Pets

[02_menu_pets.png](flow_images/q2/02_menu_pets.png): b2 menu ba gạch, b3 Pets.

## Menu chung ảnh 01 — Danh sách chữ

[01_list_menu.png](flow_images/shared/01_list_menu.png): biến thể menu ba gạch gồm `Shop by Category`, các hàng danh mục và `Sign In`. Người dùng yêu cầu bấm Home, chỉ xem 2–5 giây, quay về menu rồi làm b4 Sign In. Bộ phân loại xử lý theo cây UI đang hiển thị, không phụ thuộc ảnh này; xem [MENU_ROUTING.md](MENU_ROUTING.md).

## q1 ảnh lỗi mới 01–06 — b6, b9, b10

- [01_b6_error.png](flow_images/q1/latest_errors/01_b6_error.png): lỗi vùng bấm ở b6.
- [02_country_open.png](flow_images/q1/latest_errors/02_country_open.png): danh sách quốc gia còn ở đầu chữ A; phải cuộn tới United States +1 đang hiện và có bounds hợp lệ.
- [03_b9_error.png](flow_images/q1/latest_errors/03_b9_error.png): thông báo nhiều `Continue` ở b9.
- [04_name_form.png](flow_images/q1/latest_errors/04_name_form.png): form tên có bàn phím mở và một nút Continue nhìn thấy dưới ô tên.
- [05_b10_error.png](flow_images/q1/latest_errors/05_b10_error.png): thông báo URL OTP HTTP 403 khi tool ghi b10.
- [06_whatsapp.png](flow_images/q1/latest_errors/06_whatsapp.png): màn vẫn là Verify with WhatsApp, nút Send code by SMS chưa được bấm. Ảnh này cho thấy bản đang chạy đã đọc URL trước khi gửi SMS; mã nguồn hiện tại đọc URL ở b11 sau khi xác nhận màn SMS. Chưa kiểm chứng phiên tool đang chạy nạp phiên bản mã nào.

## q1 ảnh 15 — b4 Sign In trên menu danh sách

[15_b4_list_sign_in_ambiguous.png](flow_images/q1/15_b4_list_sign_in_ambiguous.png): q1 hiện menu dạng danh sách, Sign In nằm dưới Customer Service nhưng tool báo không xác định được duy nhất `Sign In`. Bộ chọn b4 cần ưu tiên phần tử có thể bấm, hoặc phần tử ở dưới Customer Service khi cây UI trả nhãn lặp. Chưa có ADB dump của chính máy này để xác minh thuộc tính các node.

Ảnh tiếp theo của người dùng chưa có trong danh mục này. Khi nhận ảnh mới, lưu tên theo máy và thứ tự, cập nhật `STEP_INVENTORY.md`, file Qn tương ứng, `PROJECT_HANDOFF.md` rồi cập nhật Graphify.

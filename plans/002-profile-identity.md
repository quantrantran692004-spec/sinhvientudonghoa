# 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ

## Mục tiêu và bằng chứng

`desktop.py:55-60` gán q1..q12 khi mở app; `desktop.py:617-630` gán lại sau xóa mẻ. `desktop.py:685-694` gọi `profile_status(name)`; mọi `ToolError` đều dẫn tới `create_profile`. Nếu tên đã có, nhánh thành công bỏ qua proxy mới và mở Profile cũ. `swarmote_desktop.py:164-174` báo lỗi chung cho không tìm thấy, nhiều kết quả hoặc lỗi UI. `create_profile` chỉ xác nhận tên xuất hiện sau khi gửi Create (`swarmote_desktop.py:155-161`), chưa đối chiếu lại proxy đã áp dụng.

## Phạm vi

Sửa `amazon_android/desktop.py`, `amazon_android/swarmote_desktop.py`; thêm `amazon_android/profile_registry.py`, `tests/test_profile_registry.py`; cập nhật README. Không tự xóa Profile Swarmote, không đổi proxy của Profile đã tồn tại và không thực hiện đăng ký Amazon.

## Thiết kế yêu cầu

- Tên Profile Swarmote tăng liên tục q1, q2… xuyên các mẻ. Giao diện vẫn hiện "Máy 1..N" cho slot trong mẻ, kèm tên qN thực tế. Không tái sử dụng qN tự động khi người dùng mở lại tool.
- Lưu **chỉ metadata** vào một file JSON cục bộ: tên qN đã cấp, ID mẻ, trạng thái tạo/không chắc chắn, Device ID nếu có. Không lưu proxy, mật khẩu, số điện thoại hay tên Amazon. Ghi file theo kiểu atomic replace.
- Trước khi cấp qN, đối chiếu với Swarmote. Một tên có sẵn mà không thuộc mẻ hiện tại là xung đột, không phải bằng chứng proxy đúng. Bỏ qua tới qN tiếp theo hoặc báo hết dung lượng; không dùng lại âm thầm.
- Tách lỗi `ProfileNotFound` khỏi `ProfileLookupError`/`AmbiguousProfile`. Chỉ `ProfileNotFound` mới cho phép tạo; lỗi UI, nhiều dòng trùng hoặc trạng thái chưa rõ phải dừng máy đó.
- Sau Create, xác nhận duy nhất tên, trạng thái và Device ID khi có. Nếu Create timeout hoặc kết quả chưa rõ, lưu trạng thái `UNCERTAIN`; lần Tiếp tục phải tra cứu lại trước khi quyết định, tuyệt đối không gửi Create lần hai một cách mù quáng.
- Không hứa sẽ tạo vô hạn Profile. Nếu Swarmote báo hết slot/tài nguyên, trả trạng thái cần xử lý và giữ các máy khác. Không tự xóa các Profile cũ.

## Các bước

1. Viết registry và bộ cấp tên độc lập Tk; thêm kiểm tra tính duy nhất qua nhiều mẻ và sau khởi động lại.
2. Tách loại lỗi của `profile_status` và sửa `desktop._run` để chỉ tạo khi chắc chắn chưa có Profile. Trường hợp đã tồn tại phải có liên kết registry đúng mẻ; nếu không, báo xung đột.
3. Reconcile kết quả Create trước khi mở máy; hiển thị qN thực tế trên bảng và trong trạng thái. Không hiển thị proxy/mật khẩu trong registry hoặc log.

## Kiểm tra bắt buộc

- `python -m unittest tests.test_profile_registry -v`: mẻ 3, rồi 5, rồi 4 nhận q1..q12 không lặp; mở lại tool vẫn cấp tiếp; qN tồn tại ngoài registry không bị dùng lại; lỗi UI không gọi Create; timeout sau Create không tự thử lại.
- `python -m unittest discover -s tests -q`: toàn bộ vẫn qua.
- Kiểm thử Swarmote có kiểm soát với một Profile mới: sau tạo, tên và Device ID được đọc lại. Không dùng proxy thật của mẻ khác để thử tái sử dụng.

## Điều kiện dừng

Nếu UI Swarmote không phân biệt chắc chắn "không thấy" với lỗi danh sách/phân trang, không tự tạo và báo cần xác minh khả năng tìm Profile. Nếu không thể xác minh giới hạn slot hoặc proxy của Profile cũ, không triển khai nhánh tái sử dụng. Dự án chưa có Git; đối chiếu đoạn mã nêu trên trước khi sửa.

## Rủi ro và bảo trì

Rủi ro trung bình: cấp tên sau sự cố có thể bỏ số nhưng không được lặp số. File metadata phải chịu được đóng app đột ngột. Cần xác nhận cách Swarmote hiển thị hơn 20 Profile trước khi đặt mục tiêu số lượng lớn.

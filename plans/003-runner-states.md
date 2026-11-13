# 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật

## Mục tiêu và bằng chứng

Nút chạy `desktop.py:637-638` truyền mọi hàng 0..N-1. `desktop.py:673-708` xử lý trọn q1 rồi q2…, còn `batch.py:35-77` tạo hết năm Profile trước rồi mới mở từng máy; hai luồng không cùng quy trình. `desktop.py:680-697` chỉ kiểm tra Stop trước mỗi máy và sau tạo Profile. `home_menu.py:70-80` start, install, open Amazon rồi dừng ở menu. Lỗi của một máy được báo nhưng bước đã thành công không được lưu để tiếp tục chính xác.

## Phạm vi

Thêm `amazon_android/runner.py`, `tests/test_runner.py`; sửa `desktop.py`, `batch.py` và tài liệu quy trình. Có thể cần bổ sung hàm quan sát trạng thái read-only trong `swarmote_desktop.py` và `home_menu.py`. Không song song hóa thao tác UIA; không tự nhập dữ liệu đăng ký Amazon.

## Quy trình đích

1. Snapshot mẻ hợp lệ và khóa chỉnh sửa.
2. **Pha tạo:** với từng hàng, xác minh tên chưa có, Test proxy, Create, xác nhận Profile. Hàng lỗi được đánh dấu riêng; các hàng khác vẫn chạy. Không tự retry Create sau timeout chưa rõ.
3. **Pha chuẩn bị:** với từng Profile đã xác nhận, Start, kiểm tra ADB, cài hoặc xác nhận Amazon, mở trang chủ và menu ba gạch. Chỉ đánh dấu `MENU_OPEN` khi UI Android xác nhận.
4. Stop có hiệu lực sau bước nguyên tử hiện tại, trước bước tiếp theo. Hàng đang chờ hiển thị `Chưa chạy` hoặc `Đã dừng`, không báo toàn mẻ hoàn tất khi còn lỗi.
5. "Tiếp tục" trên từng hàng đọc trạng thái thật của Swarmote/Android rồi chạy từ bước thiếu, không lặp Create hoặc Install đã xác nhận. Một hàng `MENU_OPEN` không chạy lại trừ khi có thao tác đặt lại rõ ràng.

## Các bước

1. Tạo enum trạng thái `VALIDATED`, `CREATING`, `PROFILE_CONFIRMED`, `STARTING`, `APP_INSTALLED`, `MENU_OPEN`, `ERROR`, `UNCERTAIN`, `STOPPED` và kết quả mỗi hàng. Worker chỉ gửi sự kiện; Tk chỉ nhận ở main thread như `_poll` hiện tại.
2. Chuyển cả nút chạy và nút Tiếp tục sang một runner hai pha. `batch.prepare_five` phải dùng cùng runner hoặc được đánh dấu legacy và loại khỏi CLI/tài liệu; không để hai ngữ nghĩa mẻ khác nhau.
3. Đặt điểm kiểm tra Stop sau các bước Test/Create, Start, Install, mở Amazon. Đổi nhãn nút theo đúng hiệu lực: "Dừng sau bước hiện tại"; không hứa dừng tức thì một lệnh UIA đang chờ.
4. Thêm snapshot trạng thái sau từng bước (metadata, không chứa tài khoản/proxy), reconciliation khi tiếp tục, và tổng kết `thành công / lỗi / chưa chạy`.

## Kiểm tra bắt buộc

- `python -m unittest tests.test_runner -v`: với 3 máy, xác nhận thứ tự Create A/B/C rồi Start/Install/Menu A/B/C; Create B lỗi thì A/C tiếp tục; Stop giữa hai bước không gọi bước sau; Continue từ `APP_INSTALLED` không Create/Install lại; timeout Create đưa tới `UNCERTAIN`.
- `python -m unittest discover -s tests -q`: toàn bộ vẫn qua.
- Kiểm thử thật một Profile đã xác nhận với Swarmote: status hiện đúng `MENU_OPEN`; chụp thời gian từng bước, không chiếm chuột/focus.

## Điều kiện dừng

Nếu Swarmote không cung cấp cách đọc lại một bước đủ tin cậy, không tự resume bước đó; để `UNCERTAIN` và yêu cầu người dùng kiểm tra. Nếu thay đổi luồng cần chạy đồng thời UIA trên cùng cửa sổ quản lý, tách thành nghiên cứu riêng. Dự án chưa có Git; đối chiếu đoạn mã nêu trên trước khi sửa.

## Rủi ro và bảo trì

Rủi ro cao vì thay điều phối luồng chạy thật. Hai pha giúp biết rõ khi nào đã tạo xong toàn bộ Profile, nhưng chưa chắc nhanh hơn xử lý từng máy; chỉ số đo trong kế hoạch 004 mới quyết định tối ưu tiếp.

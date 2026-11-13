# Kế hoạch sửa luồng mẻ Swarmote

Rà soát ngày 2026-11-13. Đây là kế hoạch, chưa thay đổi mã ứng dụng. Dự án hiện không có thư mục `.git`; trước khi thực hiện một hạng mục, đối chiếu các đoạn mã và dòng trong kế hoạch với bản hiện tại thay cho `git diff`. Lệnh kiểm tra hiện chạy được: `python -m unittest discover -s tests -q` (23/23 qua).

## Kết luận đã xác minh

| Ưu tiên | Vấn đề | Bằng chứng | Tác động |
| --- | --- | --- | --- |
| P0 | Dán danh sách ngắn hơn ghi đè từ q1 nhưng giữ đuôi cũ; hai danh sách có thể lệch số hàng | `amazon_android/desktop.py:397-445` | Mẻ 3 → 5 → 4 có thể chạy sai proxy hoặc thông tin cũ |
| P0 | q1… được đặt lại sau nút xóa; Profile tồn tại được dùng lại mà không xác minh proxy | `desktop.py:617-630`, `desktop.py:685-698` | Mẻ mới có thể chạy trên máy và proxy của mẻ trước |
| P0 | Mọi lỗi `profile_status` bị hiểu như "chưa có Profile" | `desktop.py:686-693`, `swarmote_desktop.py:164-174` | Lỗi giao diện hoặc tên trùng bị chuyển thành yêu cầu tạo mới |
| P1 | Dữ liệu vẫn có thể sửa/dán khi worker đang chạy | `desktop.py:365-452`, `desktop.py:640-672` | Bảng hiển thị khác với job snapshot đang thực thi |
| P1 | Nút "Chạy các Profile đã chọn" chạy tất cả 1..N; runner chạy trọn từng máy; `batch.py` lại tạo hết năm Profile trước | `desktop.py:272-278`, `desktop.py:637-708`, `batch.py:35-77` | Hành vi khó đoán; hai đường chạy có quy trình khác nhau |
| P1 | Nút dừng chỉ được kiểm tra giữa các máy và sau tạo Profile | `desktop.py:680-697` | Không dừng được Test proxy, Start, cài app đang chờ |
| P1 | SĐT, mật khẩu, tên được nhận nhưng không truyền vào Amazon; chỉ dừng ở menu ba gạch | `desktop.py:397-419`, `desktop.py:698-703`, `home_menu.py:70-80` | Giao diện dễ làm người dùng hiểu nhầm mức hoàn thành |
| P2 | Chưa xác minh một mẻ 3/5/4 thật, giới hạn Profile Swarmote, và khả năng tạo hàng loạt của bản app đang dùng | `PRODUCT.md`, `VERIFICATION.md`, `swarmote_desktop.py:115-161` | Chưa có cơ sở hứa hẹn tốc độ hoặc chạy hàng nghìn Profile |

## Thứ tự thực hiện

| Kế hoạch | Kết quả | Ưu tiên | Công sức | Phụ thuộc | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| [001](001-batch-draft.md) | Mỗi mẻ có dữ liệu độc lập, dán 3/5/4 không lẫn | P0 | M | — | DONE (UI smoke) |
| [002](002-profile-identity.md) | qN không trùng, proxy gắn đúng Profile, lỗi được phân biệt | P0 | M | 001 | CODE DONE; LIVE CREATE PENDING |
| [003](003-runner-states.md) | Một quy trình chạy hai pha, có dừng và tiếp tục rõ ràng | P1 | L | 001, 002 | CODE DONE; LIVE RUN PENDING |
| [004](004-ui-and-verification.md) | Giao diện nói đúng trạng thái; đo tốc độ và kiểm tra thực tế | P1 | M | 001–003 | PARTIAL (live timing pending) |

## Quy trình đích

1. Tạo **mẻ mới**; dán N proxy và N hàng `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`, N từ 1 đến 12. Nút chạy chỉ bật khi phân bổ hợp lệ. Hàng cuối của mẻ cũ không xuất hiện trong mẻ mới.
2. Cấp tên Profile duy nhất theo dãy q1, q2, q3… toàn bộ các mẻ. Số thứ tự máy trong giao diện vẫn là 1..N của mẻ hiện tại.
3. Pha 1: kiểm tra và tạo tất cả Profile của mẻ, từng cái một qua UI Automation; xác nhận kết quả của từng cái. Pha 2: mở từng Profile đã tạo, cài/xác minh Amazon, mở menu ba gạch rồi dừng. Không chạy đồng thời các thao tác trên cửa sổ quản lý Swarmote khi chưa chứng minh an toàn.
4. Thất bại của một máy không tự tạo lại; máy khác tiếp tục. Nút dừng có hiệu lực tại ranh giới bước. "Tiếp tục" chỉ chạy phần còn thiếu sau khi xác minh trạng thái thật.
5. Hiển thị rõ dữ liệu Amazon mới được phân bổ trong tool và **chưa nhập vào app**. Phần đăng ký tài khoản không thuộc bốn kế hoạch này.

## Giới hạn và lựa chọn cần xác minh

- Tên qN duy nhất sẽ tiêu thụ số Profile Swarmote khả dụng. Không tự xóa hoặc tái dùng Profile đã có proxy khác. Cần đo giới hạn tài khoản/gói Swarmote và thiết kế vòng đời Profile trước khi đặt mục tiêu hàng nghìn máy.
- `create_profile` hiện dùng "Single Create". Chưa có bằng chứng rằng giao diện Swarmote hỗ trợ nhập hàng loạt proxy có xác minh từng dòng; nghiên cứu tính năng đó sau khi luồng đúng và có số đo thời gian.
- Audit tập trung vào luồng mẻ và Swarmote desktop. Chưa rà sâu Android Emulator cục bộ, phụ thuộc bên ngoài hoặc giao diện đăng ký Amazon.

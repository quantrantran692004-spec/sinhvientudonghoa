# 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng

## Mục tiêu và bằng chứng

Người dùng sẽ chạy các mẻ có kích thước thay đổi, ví dụ 3 → 5 → 4. Hiện `desktop.py:425-445` dán proxy bằng cách cập nhật `self.values[0..N-1]`, giữ các dòng cũ ở phía sau và đặt `count=max(count,N)`. `desktop.py:397-419` dán bảng thông tin cũng chỉ cập nhật các dòng đầu nhưng đặt `count=N`. `desktop.py:617-630` xóa ô nhập thủ công; không tạo một thực thể mẻ có định danh. `bulk_input.py:24-67` đã kiểm tra cú pháp từng hàng nhưng không đối chiếu hai danh sách.

## Phạm vi

Sửa `amazon_android/desktop.py`, `amazon_android/bulk_input.py`; thêm `amazon_android/batch_state.py` và `tests/test_batch_state.py`. Cập nhật README mô tả hành vi dán và mẻ mới. Không chạm điều khiển Swarmote, ADB hay tài khoản Amazon.

## Thiết kế yêu cầu

- Tạo model thuần Python `BatchDraft` có tối đa 12 slot, `proxy_rows`, `account_rows`, `batch_id`, trạng thái `editing/running/finished`. Model là nguồn dữ liệu duy nhất cho số hàng và phân bổ; Tk `StringVar` chỉ là bản hiển thị.
- Lệnh dán proxy **thay thế toàn bộ danh sách proxy của mẻ hiện tại**; lệnh dán bảng Amazon thay thế toàn bộ danh sách Amazon. Dòng ngoài danh sách mới phải rỗng trong model và UI. Dán 4 hàng sau 5 hàng phải không còn hàng thứ 5.
- Trong mẻ mới, N được xác định bằng số hàng proxy. Dữ liệu Amazon có thể chưa dán, nhưng nếu đã dán thì phải đúng N hàng. Hiển thị thiếu/thừa bao nhiêu và khóa Chạy đến khi khớp. Dữ liệu Amazon chỉ được phân bổ, chưa gửi vào app.
- Một lần dán lỗi giữ nguyên bản dữ liệu trước đó và chỉ hiện lỗi; không để nửa bảng cập nhật.
- "Mẻ mới" tạo draft mới, không xóa Profile Swarmote. Không tự đổi tên qN trong kế hoạch này; kế hoạch 002 xử lý tên thật.
- Khi `running`, không cho dán, sửa chi tiết, đổi số máy hoặc xóa mẻ. Worker nhận snapshot bất biến lúc bấm Chạy; trạng thái UI cho biết snapshot đó.

## Các bước

1. Viết `BatchDraft` và các hàm thay thế danh sách, kiểm tra số hàng và tạo snapshot. Không phụ thuộc Tk hoặc Swarmote.
2. Dùng model trong `Window._apply_account_text`, `_apply_bulk_text`, `_accept_proxy_text`, `_paste_detail_column`, `_reset`, `_launch`. Chỉ dùng một đường cập nhật phân bổ để tránh ba kiểu dán cho ba kết quả khác nhau.
3. Hiện trạng thái phân bổ N/N ở cạnh hai ô dán và từng hàng. Đổi nút "Xóa dữ liệu" thành "Mẻ mới" với mô tả không xóa Profile Swarmote.

## Kiểm tra bắt buộc

- `python -m unittest tests.test_batch_state tests.test_bulk_input -v`: dán proxy 5 rồi 4 để thấy hàng 5 rỗng; dán bảng 3 rồi 5; bảng có hàng phân cách Markdown; lỗi ở hàng thứ 4 không làm thay đổi 3 hàng hợp lệ cũ; 3 proxy + 2 hàng Amazon không tạo snapshot chạy.
- `python -m unittest discover -s tests -q`: toàn bộ vẫn qua.
- Smoke test `Window` không mở Swarmote: mẻ 3 → Mẻ mới → mẻ 5 → Mẻ mới → mẻ 4; trong mỗi mẻ bảng chỉ hiện dữ liệu hiện tại, nút chạy phản ánh hợp lệ.

## Điều kiện dừng

Nếu phần dữ liệu hiện có của người dùng trong cửa sổ đang mở không thể bảo toàn khi thay đổi UI, không tự đóng cửa sổ; hướng dẫn mở bản mới. Nếu thay đổi cần lưu mật khẩu lên đĩa để chạy, dừng và thiết kế lại.

## Rủi ro và bảo trì

Rủi ro trung bình: nhiều đường dán vào cùng 12 `StringVar` dễ lệch model. Mọi chỉnh sửa sau này phải đi qua model và thử lại ca 3/5/4. Dự án chưa có Git; trước khi sửa, đối chiếu các đoạn mã nêu trên với mã hiện tại. Baseline 2026-11-13: 23 unit tests qua.

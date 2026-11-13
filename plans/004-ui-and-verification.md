# 004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ

## Mục tiêu và bằng chứng

`desktop.py:272-278` ghi "Chạy các Profile đã chọn" dù không có checkbox chọn hàng; `_start` chạy toàn bộ N. `desktop.py:397-419` nhận SĐT/mật khẩu/tên nhưng `_run` chỉ truyền `(index, name, proxy)` và `home_menu.ready_for_home_menu` không nhập dữ liệu Amazon. `desktop.py:551-579` dùng trạng thái chung "Proxy sẵn sàng"/"Đã nhập thông tin" nhưng không hiện bước đã xác minh. `PRODUCT.md` nêu mẻ 1–5, còn UI hỗ trợ 12; `VERIFICATION.md` chưa có kiểm thử mẻ thật 3/5/4.

## Phạm vi

Sửa `desktop.py`, `README.md`, `PRODUCT.md`, `PLAN.md`, `VERIFICATION.md`; thêm bài kiểm tra UI/model phù hợp trong `tests/`. Chỉ khảo sát Swarmote UI/REA read-only để xác định có chức năng bulk create đáng tin cậy. Không tự động đăng ký Amazon, không tự xóa Profile và không dùng chuột của người dùng.

## Các bước

1. Đổi nút thành "Chạy N máy trong mẻ". Hiện số hàng proxy/account, số máy hợp lệ, tên Profile qN thật, trạng thái từng bước và lý do lỗi. Dòng thông tin Amazon phải ghi "Đã phân bổ trong tool — chưa nhập vào Amazon".
2. Sau khi chạy, hiển thị tổng số tạo, mở, cài, tới menu, lỗi, chờ. Khi mẻ đang chạy, chỉ cho xem; không cho dán hoặc sửa dữ liệu. Khi kết thúc, nút "Mẻ mới" tạo draft độc lập.
3. Dùng clock monotonic để đo thời gian Test/Create, Start, Install, Menu trên từng máy; báo tổng và trung vị theo mẻ mà không log proxy, số điện thoại hay mật khẩu. Đo 1 Profile và, chỉ nếu tài nguyên cho phép, mẻ nhiều Profile thật.
4. Khảo sát UI Swarmote xem "Batch Create" có nhập được nhiều proxy riêng và trả kết quả riêng từng dòng hay không. Chỉ lập kế hoạch tích hợp nếu kiểm chứng được; nếu không, giữ thao tác UIA tuần tự.
5. Cập nhật tài liệu theo chức năng đã chạy thật. Bài test model phải mô phỏng mẻ 3 → 5 → 4, lỗi giữa mẻ, khởi động lại tool, và tiếp tục một Profile.

## Kiểm tra bắt buộc

- `python -m unittest discover -s tests -q`: toàn bộ qua.
- Smoke test cửa sổ không kết nối Swarmote: không còn nút "đã chọn" khi không có chọn; nhập 3/5/4 cho thấy đúng tên, số hàng, trạng thái; nhập thiếu hàng khóa Chạy.
- Thử thật không vượt tài nguyên Swarmote hiện có, ghi kết quả PASS/FAIL/NOT TESTED cùng thời gian và phiên bản app vào `VERIFICATION.md`. Không ghi credential.

## Điều kiện dừng

Nếu cần xóa/tái dùng Profile để thử 3/5/4 ngoài số slot hiện có, không làm tự động; đánh dấu NOT TESTED và mô tả giới hạn. Nếu bulk create không trả kết quả từng Profile hoặc không kiểm tra từng proxy, không tích hợp. Dự án chưa có Git; đối chiếu đoạn mã nêu trên trước khi sửa.

## Rủi ro và bảo trì

Rủi ro trung bình: màn hình có thể trở nên dày đặc. Ưu tiên bảng 12 hàng và chi tiết từng máy, không thêm log chứa thông tin nhạy cảm. Tốc độ thực tế phụ thuộc Swarmote và App Store, không suy ra từ unit test.

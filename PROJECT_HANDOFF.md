# Bàn giao trạng thái dự án — 13/11/2026

## Mục tiêu và quy tắc đã chốt

Tool desktop CustomTkinter điều khiển Swarmote/Amazon Shopping cho tối đa 12 máy. Mỗi hàng Amazon chứa SĐT, mật khẩu, tên, thẻ và URL OTP riêng; hàng n gắn Máy n. Bảng Markdown có cột trống, hàng gạch phân cách, thẻ `số|tháng|năm` viết `\|`, và link URL dạng `[nhãn](URL)` phải được đọc đúng. Bảng chỉ hiện đuôi thẻ; dữ liệu giữ trong bộ nhớ phiên. Thẻ chưa được dùng trong b1–b11.

Từ menu ba gạch, chỉ b1–b3 khác nhau theo máy. b4 Sign In đến b11 nhập OTP SMS rồi bấm Create dùng chung. Người dùng sẽ hướng dẫn b1–b3 của từng máy; hiện đã có q1 và q2. Mỗi máy có ADB serial, SĐT, URL OTP, mã, trạng thái gửi, đồng hồ và điểm dừng/tiếp tục riêng. Gõ từng ký tự, không dán vào Android. Nếu lỗi, dừng ngay tại bước đó; người dùng sửa trên máy rồi bấm Tiếp tục. Chu kỳ thời hạn mỗi máy: 3, 4, 5, 4 phút rồi lặp lại; tính lại khi Tiếp tục. Đồng hồ kết thúc khi OTP SMS đã nhập đúng, sau đó bấm Create.

## Mã hiện có

- `amazon_android/bulk_input.py`, `batch_state.py`, `desktop.py`, `runner.py`: ánh xạ hàng, dữ liệu thẻ/OTP, UI 12 máy; khi gắn q1, 12 hàng vẫn hiện.
- `amazon_android/otp.py`: xác thực URL APIFC, tách đúng 6 số từ phản hồi Amazon và đọc sau khi gửi SMS; HTTP 403 tạm thời được thử lại trong thời hạn chờ. APIFC không cung cấp dấu thời gian để chứng minh mã là mới khi URL đã có mã cũ.
- `amazon_android/post_menu.py`: phiên riêng từng máy, thời hạn, dừng/tiếp tục cùng bước, gõ từng ký tự.
- `amazon_android/account_flow.py`: nhận diện UI Android và `build_common_steps` cho b4–b11. `amazon_android/q1_flow.py`: b1 Gifting, b2 Pets, b3 Fashion and Beauty. `amazon_android/q2_flow.py`: b1 tab Home và xem 2–5 giây, b2 tab Browse menu, b3 Pets. `amazon_android/desktop.py` gắn profile từ menu theo máy được chọn. Không dùng tọa độ ảnh. q1 và q2 được nối; q3–q12 dừng ở menu.
- `amazon_android/swarmote_desktop.py`: khi tạo profile, kiểm tra tên trùng; nếu tên vắng trên danh sách một trang thì không gõ vào ô lọc. Đưa cửa sổ quản lý lên trước để bấm New Profile, xác nhận form trước khi điền, sau đó Test Proxy và Create.
- `Launch Swarmote Tool.pyw` gọi `amazon_android/launcher.py` để mở desktop. Graphify không phân tích trực tiếp `.pyw`; xem [SOURCE_INDEX.md](SOURCE_INDEX.md) cho các file bị bỏ qua.

## Trạng thái kiểm chứng và giới hạn

- 122 bài unittest đã qua sau sửa luồng chung b4–b11 và nối lại q2 từ mốc menu đã lưu: chạm ô SĐT ở b4, bỏ mục US ẩn ở b6, chọn Continue có thể bấm ở b9, gửi SMS rồi mới đọc OTP, tiếp tục từ màn SĐT hiện tại. Nhánh `MENU_OPEN` nay nối lại ADB serial trước khi báo q2 đã tới menu; tool báo rõ nếu thiếu hàng Amazon hoặc serial. Test cửa sổ nhận 12 hàng, giữ đúng thẻ/URL theo máy và hiện nút thử q2. Đã thử trực tiếp mở form New Profile và đóng bằng Cancel, không gửi Create.
- Lúc kiểm tra ngày 13/11/2026, Swarmote có q1, q2, q3. Người dùng đã thử q1 và gửi năm ảnh mới: form SĐT cùng lỗi b6/b9/b10; sau đó xác nhận q1 hiện ở form SĐT. Người dùng báo q2 tới menu ba gạch rồi dừng, tool chỉ ghi đã tới menu mà không báo lỗi. Mã có nhánh mốc `MENU_OPEN` cũ không nối lại ADB và các điều kiện âm thầm dừng; đã sửa và test mô phỏng, chưa thử lại q2 thật. Chưa xác minh URL OTP sau gửi hoặc màn sau Create. Lệnh `cloud-scan` trong môi trường phiên này không tìm thấy ADB Swarmote/Android SDK nên không thể tự đọc máy trực tiếp.
- Tên q1–q12 được cố định cho các slot; tool dừng nếu tên đã có để tránh trùng. Người dùng chưa quyết định sẽ dùng lại q1–q3 hay tạo profile mới tên khác. Đây là câu hỏi cần giải trước khi đổi chính sách tên.
- `graphify.exe` trên máy hiện báo lỗi `uv trampoline failed to canonicalize script path`; `python -m graphify` hoạt động.
- Graphify đã tạo `graphify-out/graph.json`, `graph.html`, `GRAPH_TREE.html` và `GRAPH_REPORT.md`. Xem [GRAPH_AUDIT.md](GRAPH_AUDIT.md) để biết chính xác phần đã lập chỉ mục và phần còn thiếu. Graph chứa AST mã nguồn cùng file/tiêu đề/liên kết tài liệu sau `python -m graphify update .`. Xem [ASSET_INDEX.md](ASSET_INDEX.md) cho sáu PNG giao diện (năm ảnh lịch sử đã gom vào `assets/ui_history/`) và [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md) cho mười sáu ảnh q1/q2 trong `flow_images/`. Các ảnh này được đưa lên repository công khai theo yêu cầu bàn giao; có thể hiển thị SĐT/OTP trên ảnh gốc. Nội dung pixel chưa được trích xuất ngữ nghĩa vì không có LLM API key hoặc Ollama; phải mở ảnh gốc khi cần. Các cạnh INFERRED của Graphify có thể sai, cần đối chiếu mã. Xem số node/cạnh hiện tại trong `GRAPH_REPORT.md` để tránh dùng số cũ.

## Tài liệu chi tiết

**Đây là quy trình đang được hướng dẫn từng ảnh, chưa phải quy trình đầy đủ.** Đọc [STEP_INVENTORY.md](STEP_INVENTORY.md) để thấy từng mốc P01–P08, q1/q2 b1–b3, b4–b11 và các mốc chưa có ảnh. Đọc [FLOW_PROGRESS.md](FLOW_PROGRESS.md) để biết mức kiểm chứng. Sau đó đọc [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md), [Q1_FLOW.md](Q1_FLOW.md), [Q2_FLOW.md](Q2_FLOW.md), [OTP_DESIGN.md](OTP_DESIGN.md), [VERIFICATION.md](VERIFICATION.md), [README.md](README.md). Không suy ra q3–q12 đã được tự động hóa chỉ vì b4–b11 dùng chung.

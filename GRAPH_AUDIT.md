# Kiểm tra độ phủ Graphify — 13/11/2026

## Đã có trong graph

- Các module Python của tool, test và entry point `amazon_android/launcher.py` được lập chỉ mục bằng AST. Các hàm mới gồm `build_q1_steps`, `build_q2_steps`, `build_common_steps`, `_activate_manager`, `_profile_form_open`, `_unfiltered_single_page`, `validate_card` đã xuất hiện khi truy vấn graph.
- Các file Markdown có node file và tiêu đề. `STEP_INVENTORY.md` có các mốc P01–P08a, Q1/Q2 b1–b3, b4–b11, E01 và U01–U03 dưới dạng node tiêu đề; `MENU_ROUTING.md` ghi nhánh menu dạng danh sách. Nội dung trong đoạn văn vẫn phải đọc từ file gốc.
- `PROJECT_HANDOFF.md`, `FLOW_PROGRESS.md`, `AGENTS.md`, `ASSET_INDEX.md` và `SOURCE_INDEX.md` dẫn tới quy trình, mức kiểm chứng và các file Graphify bỏ qua.

## Giới hạn đã xác nhận

- Graphify không phân tích trực tiếp `Launch Swarmote Tool.pyw` và `.gitignore`; `pyproject.toml` được thấy nhưng không tạo symbol. `SOURCE_INDEX.md` ghi vai trò từng file; `.pyw` gọi `amazon_android/launcher.py` để logic khởi chạy có node mã.
- Sáu PNG giao diện cũ chưa được trích xuất pixel; `ASSET_INDEX.md` liệt kê tên/kích thước. Hai mươi ba ảnh Amazon q1/q2 và một ảnh menu chung từ chat đã được sao chép vào `flow_images/` và ánh xạ ở `IMAGE_EVIDENCE.md`. Graphify chỉ có node tiêu đề/link của danh mục; phải mở ảnh gốc để xem pixel.
- Máy không có API key LLM hoặc Ollama cho Graphify trích xuất ngữ nghĩa tài liệu/ảnh. Graph chứa cấu trúc file, tiêu đề, liên kết và AST; không chứa từng câu chữ hay từng pixel. Cạnh INFERRED phải đối chiếu mã nguồn.
- Các ảnh hướng dẫn chưa đủ toàn bộ quy trình. Màn sau Create và b1–b3 của q3–q12 là mốc thiếu có chủ đích trong `STEP_INVENTORY.md`; không coi chúng là đã triển khai.

## Cách kiểm tra sau mỗi sửa đổi

1. Cập nhật `STEP_INVENTORY.md`, `FLOW_PROGRESS.md` và tài liệu máy liên quan nếu yêu cầu đổi.
2. Chạy `python -m graphify update .` rồi `python -m graphify tree` tại `D:\sinhvien`.
3. Đối chiếu file/symbol/tiêu đề mới với `graphify-out/graph.json`, rồi đọc file gốc khi cần chi tiết. `graphify.exe` hiện lỗi uv trampoline; dùng `python -m graphify`.
4. Chạy test bằng thư mục tạm trong workspace nếu sandbox chặn Temp mặc định. Ngày 13/11/2026, `131/131` unittest đã qua với `TMP`, `TEMP`, `TMPDIR` trỏ vào `D:\sinhvien\.test_tmp` sau sửa b4 Sign In có nhãn lặp.

# File dự án mà Graphify không phân tích trực tiếp

Graphify ưu tiên mã `.py` và cấu trúc Markdown. Những file dưới đây được ghi thành node tài liệu để phiên sau biết chúng tồn tại, nhưng phải mở file gốc khi cần chi tiết.

## Launch Swarmote Tool.pyw

Launcher Windows ngắn gọi `amazon_android.launcher.main`; Graphify không nhận diện đuôi `.pyw`. Logic khởi chạy thực tế nằm trong `amazon_android/launcher.py`, có node mã trong graph.

## .gitignore

Quy tắc loại file khi dùng Git; Graphify bỏ qua file này. Kiểm tra trực tiếp trước khi thêm ảnh hoặc dữ liệu nhạy cảm vào dự án.

## pyproject.toml

Metadata/cấu hình đóng gói Python. Graphify phát hiện file nhưng bộ AST không tạo symbol từ nội dung TOML; đọc file gốc khi thay dependencies hoặc entry point.

## Ảnh PNG trong dự án

Sáu ảnh PNG giao diện cũ được liệt kê trong [ASSET_INDEX.md](ASSET_INDEX.md). Hai mươi ba ảnh q1/q2 cùng một ảnh menu chung nằm trong `flow_images/` và được ánh xạ tại [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Cây chỉ có node tên ảnh từ mục lục, không có nội dung pixel.

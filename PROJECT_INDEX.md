# Bản đồ repository

Đây là điểm bắt đầu để tiếp tục dự án mà không bỏ sót mốc đã biết. Ảnh người dùng cung cấp mới hướng dẫn q1 và q2; chưa có toàn bộ quy trình.

| Phần | Vị trí | Mục đích |
| --- | --- | --- |
| Chạy tool | [README.md](README.md), [Launch Swarmote Tool.pyw](Launch%20Swarmote%20Tool.pyw), `amazon_android/` | Cài đặt, mở giao diện và mã nguồn. |
| Bàn giao | [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md), [FLOW_PROGRESS.md](FLOW_PROGRESS.md), [STEP_INVENTORY.md](STEP_INVENTORY.md) | Trạng thái thật, từng bước đã biết và phần còn thiếu. |
| Luồng Amazon | [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md), [MENU_ROUTING.md](MENU_ROUTING.md), [Q1_FLOW.md](Q1_FLOW.md), [Q2_FLOW.md](Q2_FLOW.md), [OTP_DESIGN.md](OTP_DESIGN.md) | Hai bố cục menu, quy tắc tự động hóa và OTP theo máy. |
| Minh chứng ảnh | [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md), `flow_images/q1/`, `flow_images/q2/`, `flow_images/shared/` | Ảnh gốc từng bước; phải mở ảnh để xem pixel. |
| Giao diện cũ | [ASSET_INDEX.md](ASSET_INDEX.md), `assets/ui_history/` | Các ảnh chụp giao diện qua những lần thiết kế. |
| Kiểm chứng | [VERIFICATION.md](VERIFICATION.md), `tests/` | Kết quả kiểm tra thật và test mô phỏng. |
| Kế hoạch | `plans/`, [PLAN.md](PLAN.md), [PRODUCT.md](PRODUCT.md), [DESIGN.md](DESIGN.md) | Quyết định, yêu cầu, giao diện. |
| Cây dự án | [GRAPH_AUDIT.md](GRAPH_AUDIT.md), [SOURCE_INDEX.md](SOURCE_INDEX.md), `graphify-out/` | Graphify, giới hạn lập chỉ mục và file không được phân tích. |
| Quy tắc phiên sau | [AGENTS.md](AGENTS.md) | Cách tiếp tục, cập nhật graph và bảo toàn dữ liệu từng máy. |

`graphify-out/` chỉ đưa lên các đầu ra đọc được (`graph.json`, `graph.html`, `GRAPH_TREE.html`, `GRAPH_REPORT.md`, `manifest.json`); cache và trạng thái dựng tạm được Git bỏ qua. `__pycache__/`, `.test_tmp/` và file chạy tạm cũng không phải mã nguồn. Dữ liệu nhập thật của phiên đang chạy chỉ ở bộ nhớ và không có trong repository.

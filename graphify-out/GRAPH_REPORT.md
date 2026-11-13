# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~47,577 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 850 nodes · 2641 edges · 36 communities (32 shown, 4 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 338 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `27b2e506`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- ToolError
- desktop.py
- Window
- ToolError
- bulk_input.py
- RunnerTests
- read_otp
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_HANDOFF.md
- plans/README.md
- Danh mục từng bước đã biết — 13/11/2026
- File dự án mà Graphify không phân tích trực tiếp
- batch.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- FakeControl
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Luồng q1 từ menu ba gạch tới nhập OTP
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- Điều hướng hai dạng menu ba gạch
- Danh mục ảnh nằm trong dự án
- Giao diện vận hành
- Amazon trên Swarmote
- Nghiên cứu và tích hợp Swarmote
- PLAN.md
- Quy tắc tự động hóa sau menu ba gạch
- Bàn giao trạng thái dự án — 13/11/2026
- Amazon Android Tool — Giai đoạn A/B
- ToolError
- Thiết kế OTP cho từng Profile
- Kiểm tra độ phủ Graphify — 13/11/2026
- 004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026
- ProxyConfig

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 177 edges
2. `CloudPhone` - 79 edges
3. `Window` - 64 edges
4. `RunJob` - 45 edges
5. `build_common_steps()` - 38 edges
6. `main()` - 37 edges
7. `AttemptDeadline` - 35 edges
8. `_read_nodes()` - 34 edges
9. `RunnerTests` - 34 edges
10. `build_q2_steps()` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Phần dùng chung đã được hướng dẫn` --references--> `build_common_steps()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `Trạng thái hiện tại của dự án` --references--> `build_common_steps()`  [INFERRED]
  POST_MENU_REQUIREMENTS.md → amazon_android/account_flow.py
- `Thử trên q1 đã có` --references--> `build_common_steps()`  [INFERRED]
  Q1_FLOW.md → amazon_android/account_flow.py
- `Luồng q2 từ menu ba gạch` --references--> `build_common_steps()`  [INFERRED]
  Q2_FLOW.md → amazon_android/account_flow.py
- `Các bước` --references--> `prepare_five()`  [INFERRED]
  plans/003-runner-states.md → amazon_android/batch.py

## Import Cycles
- None detected.

## Communities (36 total, 4 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.07
Nodes (39): _table_cells(), main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names() (+31 more)

### Community 1 - "ToolError"
Cohesion: 0.06
Nodes (57): _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp(), name() (+49 more)

### Community 2 - "desktop.py"
Cohesion: 0.12
Nodes (9): _crystal_art(), main(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path() (+1 more)

### Community 3 - "Window"
Cohesion: 0.06
Nodes (14): _automatic_resume_slots(), _edge_light(), Window, otp_token(), AccountData, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc (+6 more)

### Community 4 - "ToolError"
Cohesion: 0.09
Nodes (28): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+20 more)

### Community 5 - "bulk_input.py"
Cohesion: 0.10
Nodes (8): BatchDraft, BulkRecord, lines(), parse_column(), parse_records(), _url_from_cell(), BatchDraftTests, BulkInputTests

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (15): ProfileRegistry, ProfileNotFound, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create() (+7 more)

### Community 7 - "read_otp"
Cohesion: 0.11
Nodes (6): extract_otp(), _NoRedirect, read_otp(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_HANDOFF.md"
Cohesion: 0.38
Nodes (3): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch

### Community 10 - "plans/README.md"
Cohesion: 0.20
Nodes (5): Giới hạn và lựa chọn cần xác minh, Kế hoạch sửa luồng mẻ Swarmote, Kết luận đã xác minh, Quy trình đích, Thứ tự thực hiện

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (29): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại, Chung b8 — Proceed to create an account (+21 more)

### Community 12 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 13 - "batch.py"
Cohesion: 0.40
Nodes (4): BatchItem, parse_proxy_line(), prepare_five(), BatchSafetyTests

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.12
Nodes (17): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+9 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.11
Nodes (19): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+11 more)

### Community 18 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.29
Nodes (7): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 20 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.25
Nodes (8): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng

### Community 21 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.67
Nodes (3): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch

### Community 22 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 23 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 24 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 27 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 28 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.50
Nodes (4): Bàn giao trạng thái dự án — 13/11/2026, Mục tiêu và quy tắc đã chốt, Trạng thái kiểm chứng và giới hạn, Tài liệu chi tiết

### Community 29 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.40
Nodes (5): Amazon Android Tool — Giai đoạn A/B, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 30 - "ToolError"
Cohesion: 0.05
Nodes (51): validate_card(), ToolError, emit(), _nodes(), open_home_menu(), ready_for_home_menu(), _tap(), _prepare_phone() (+43 more)

### Community 31 - "Thiết kế OTP cho từng Profile"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 32 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.50
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 33 - "004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ"
Cohesion: 0.29
Nodes (7): 004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 34 - "Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 35 - "ProxyConfig"
Cohesion: 0.22
Nodes (4): create_profile(), ProxyConfig, CreationWindowVisibilityTests, Ẩn cửa sổ quản lý khi tạo Profile — 2026-11-13

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 260 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `ToolError`, `desktop.py`, `Window`, `ToolError`, `bulk_input.py`, `RunnerTests`, `read_otp`, `ProxyConfig`, `batch.py`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`?**
  _High betweenness centrality (0.435) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `ToolError` (e.g. with `_visible()` and `BatchDraft`) actually correct?**
  _`ToolError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07201225740551584 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `ToolError` to `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`, `ToolError`, `read_otp`, `PROJECT_HANDOFF.md`, `Luồng q1 từ menu ba gạch tới nhập OTP`, `Quy tắc tự động hóa sau menu ba gạch`, `ToolError`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.059033989266547404 - nodes in this community are weakly interconnected._
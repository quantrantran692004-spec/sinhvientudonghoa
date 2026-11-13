# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 65 files · ~43,877 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 821 nodes · 2528 edges · 29 communities (25 shown, 4 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 314 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5124aa2c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- ToolError
- desktop.py
- Window
- ToolError
- runner.py
- RunnerTests
- read_otp
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_HANDOFF.md
- BatchDraft
- Danh mục từng bước đã biết — 13/11/2026
- File dự án mà Graphify không phân tích trực tiếp
- BatchDraft
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- Luồng q1 từ menu ba gạch tới nhập OTP
- swarmote_desktop.py
- Danh mục ảnh nằm trong dự án
- Giao diện vận hành
- Amazon trên Swarmote
- Nghiên cứu và tích hợp Swarmote
- PLAN.md
- Quy tắc tự động hóa sau menu ba gạch
- Bàn giao trạng thái dự án — 13/11/2026
- Amazon Android Tool — Giai đoạn A/B
- Thiết kế OTP cho từng Profile
- Kiểm tra độ phủ Graphify — 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 177 edges
2. `CloudPhone` - 76 edges
3. `Window` - 64 edges
4. `RunJob` - 39 edges
5. `main()` - 37 edges
6. `build_common_steps()` - 35 edges
7. `AttemptDeadline` - 33 edges
8. `_read_nodes()` - 32 edges
9. `ProfileRegistry` - 31 edges
10. `profile_status()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Trạng thái hiện tại của dự án` --references--> `build_common_steps()`  [INFERRED]
  POST_MENU_REQUIREMENTS.md → amazon_android/account_flow.py
- `Mã hiện có` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Thử trên q1 đã có` --references--> `build_common_steps()`  [INFERRED]
  Q1_FLOW.md → amazon_android/account_flow.py
- `Luồng q2 từ menu ba gạch` --references--> `build_common_steps()`  [INFERRED]
  Q2_FLOW.md → amazon_android/account_flow.py
- `Các bước` --references--> `prepare_five()`  [INFERRED]
  plans/003-runner-states.md → amazon_android/batch.py

## Import Cycles
- None detected.

## Communities (29 total, 4 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.08
Nodes (39): _table_cells(), main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names() (+31 more)

### Community 1 - "ToolError"
Cohesion: 0.06
Nodes (55): _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp(), name() (+47 more)

### Community 2 - "desktop.py"
Cohesion: 0.09
Nodes (12): _automatic_resume_slots(), _crystal_art(), main(), save(), default_path(), AccountData, AppSettings, load_settings() (+4 more)

### Community 3 - "Window"
Cohesion: 0.06
Nodes (12): BulkRecord, lines(), parse_column(), parse_records(), _url_from_cell(), validate_card(), _edge_light(), Window (+4 more)

### Community 4 - "ToolError"
Cohesion: 0.09
Nodes (33): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+25 more)

### Community 5 - "runner.py"
Cohesion: 0.09
Nodes (18): BatchItem, parse_proxy_line(), prepare_five(), emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots() (+10 more)

### Community 6 - "RunnerTests"
Cohesion: 0.06
Nodes (17): ProfileRegistry, ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, absent(), ProfileRegistryTests, lookup(), broken() (+9 more)

### Community 7 - "read_otp"
Cohesion: 0.09
Nodes (4): extract_otp(), _NoRedirect, read_otp(), OtpTests

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_HANDOFF.md"
Cohesion: 0.34
Nodes (3): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch

### Community 10 - "BatchDraft"
Cohesion: 0.05
Nodes (34): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ (+26 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (28): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại, Chung b8 — Proceed to create an account (+20 more)

### Community 12 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.15
Nodes (13): Biên bản kiểm tra thực tế — 2026-11-12, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13, Nút New Profile trên Swarmote — 13/11/2026, Năm ảnh lỗi q1 và sửa luồng chung — 13/11/2026 (+5 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.12
Nodes (17): q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên, q1 ảnh 08 — Chọn SMS thay WhatsApp (+9 more)

### Community 20 - "swarmote_desktop.py"
Cohesion: 0.06
Nodes (36): ready_for_home_menu(), _activate_manager(), _create_profile_form(), _descendants(), inspect(), install_amazon(), _invoke(), _main_window() (+28 more)

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
Cohesion: 0.40
Nodes (5): Bàn giao trạng thái dự án — 13/11/2026, Mã hiện có, Mục tiêu và quy tắc đã chốt, Trạng thái kiểm chứng và giới hạn, Tài liệu chi tiết

### Community 29 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.40
Nodes (5): Amazon Android Tool — Giai đoạn A/B, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 31 - "Thiết kế OTP cho từng Profile"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 32 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 250 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `ToolError`, `desktop.py`, `Window`, `runner.py`, `RunnerTests`, `read_otp`, `BatchDraft`, `BatchDraft`, `swarmote_desktop.py`?**
  _High betweenness centrality (0.450) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `ToolError` (e.g. with `_visible()` and `BatchDraft`) actually correct?**
  _`ToolError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.083089905874716 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `ToolError` to `ToolError`, `runner.py`, `PROJECT_HANDOFF.md`, `Luồng q1 từ menu ba gạch tới nhập OTP`, `swarmote_desktop.py`, `Quy tắc tự động hóa sau menu ba gạch`, `Bàn giao trạng thái dự án — 13/11/2026`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.05812324929971989 - nodes in this community are weakly interconnected._
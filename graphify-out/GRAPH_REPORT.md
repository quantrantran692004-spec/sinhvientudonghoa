# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 65 files · ~42,205 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 800 nodes · 2467 edges · 34 communities (30 shown, 4 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 305 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- core.py
- ToolError
- desktop.py
- Window
- ToolError
- ProxyConfig
- RunnerTests
- read_otp
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_HANDOFF.md
- BatchDraft
- Danh mục từng bước đã biết — 13/11/2026
- File dự án mà Graphify không phân tích trực tiếp
- BatchDraft
- test_swarmote_navigation.py
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- time
- time
- PROJECT_HANDOFF.md
- swarmote_desktop.py
- ProxyConfig
- Danh mục ảnh nằm trong dự án
- Giao diện vận hành
- Amazon trên Swarmote
- Nghiên cứu và tích hợp Swarmote
- PLAN.md
- Quy tắc tự động hóa sau menu ba gạch
- Bàn giao trạng thái dự án — 13/11/2026
- Amazon Android Tool — Giai đoạn A/B
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026
- Thiết kế OTP cho từng Profile
- Kiểm tra độ phủ Graphify — 13/11/2026
- runner.py

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 174 edges
2. `CloudPhone` - 74 edges
3. `Window` - 64 edges
4. `RunJob` - 38 edges
5. `main()` - 37 edges
6. `build_common_steps()` - 34 edges
7. `AttemptDeadline` - 32 edges
8. `_read_nodes()` - 31 edges
9. `ProfileRegistry` - 31 edges
10. `profile_status()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Phần dùng chung đã được hướng dẫn` --references--> `build_common_steps()`  [INFERRED]
  FLOW_PROGRESS.md → amazon_android/account_flow.py
- `Trạng thái hiện tại của dự án` --references--> `build_common_steps()`  [INFERRED]
  POST_MENU_REQUIREMENTS.md → amazon_android/account_flow.py
- `Mã hiện có` --references--> `build_common_steps()`  [INFERRED]
  PROJECT_HANDOFF.md → amazon_android/account_flow.py
- `Thử trên q1 đã có` --references--> `build_common_steps()`  [INFERRED]
  Q1_FLOW.md → amazon_android/account_flow.py
- `Luồng q2 từ menu ba gạch` --references--> `build_common_steps()`  [INFERRED]
  Q2_FLOW.md → amazon_android/account_flow.py

## Import Cycles
- None detected.

## Communities (34 total, 4 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.09
Nodes (38): main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play() (+30 more)

### Community 1 - "ToolError"
Cohesion: 0.08
Nodes (49): _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp(), name() (+41 more)

### Community 2 - "desktop.py"
Cohesion: 0.12
Nodes (9): _crystal_art(), main(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path() (+1 more)

### Community 3 - "Window"
Cohesion: 0.06
Nodes (15): validate_card(), _automatic_resume_slots(), _edge_light(), Window, otp_token(), AccountData, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước (+7 more)

### Community 4 - "ToolError"
Cohesion: 0.07
Nodes (32): cloud_adb(), cloud_serials(), open_amazon(), foreground(), package_path(), probe(), prop(), reported_installer() (+24 more)

### Community 5 - "ProxyConfig"
Cohesion: 0.07
Nodes (25): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), parse_column(), parse_records(), _table_cells() (+17 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (25): emit(), ProfileRegistry, _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), _profile_row_status() (+17 more)

### Community 7 - "read_otp"
Cohesion: 0.12
Nodes (6): extract_otp(), _NoRedirect, read_otp(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 10 - "BatchDraft"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (28): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại, Chung b8 — Proceed to create an account (+20 more)

### Community 12 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 14 - "test_swarmote_navigation.py"
Cohesion: 0.14
Nodes (9): _activate_manager(), _create_profile_form(), _open_profiles(), visible_profile_names(), _wait_for(), control(), ProfilesNavigationTests, descendants() (+1 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.17
Nodes (12): q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên, q1 ảnh 08 — Chọn SMS thay WhatsApp (+4 more)

### Community 17 - "time"
Cohesion: 0.18
Nodes (5): ready_for_home_menu(), install_amazon(), show_apps(), FakeControl, InstallTests

### Community 18 - "time"
Cohesion: 0.27
Nodes (4): open_adb_shell(), _phone_window(), profile_status(), _unfiltered_single_page()

### Community 19 - "PROJECT_HANDOFF.md"
Cohesion: 0.38
Nodes (3): Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 20 - "swarmote_desktop.py"
Cohesion: 0.16
Nodes (15): _descendants(), inspect(), _invoke(), _main_window(), _one(), _profile_checkbox(), _profile_form_open(), _select_profile_rows() (+7 more)

### Community 21 - "ProxyConfig"
Cohesion: 0.27
Nodes (3): create_profile(), ProxyConfig, CreationWindowVisibilityTests

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

### Community 30 - "Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 31 - "Thiết kế OTP cho từng Profile"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 32 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 33 - "runner.py"
Cohesion: 0.15
Nodes (4): ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyTestFailed, unavailable()

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 240 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ProxyConfig` to `core.py`, `ToolError`, `desktop.py`, `Window`, `ToolError`, `runner.py`, `RunnerTests`, `read_otp`, `BatchDraft`, `BatchDraft`, `test_swarmote_navigation.py`, `time`, `time`, `swarmote_desktop.py`, `ProxyConfig`?**
  _High betweenness centrality (0.448) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `ToolError` (e.g. with `BatchDraft` and `CloudPhone`) actually correct?**
  _`ToolError` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08842105263157894 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `ToolError` to `ProxyConfig`, `read_otp`, `PROJECT_HANDOFF.md`, `Quy tắc tự động hóa sau menu ba gạch`, `Bàn giao trạng thái dự án — 13/11/2026`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.0784313725490196 - nodes in this community are weakly interconnected._
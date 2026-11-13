# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 65 files · ~44,757 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 826 nodes · 2551 edges · 38 communities (35 shown, 3 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 321 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5d441044`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- ToolError
- desktop.py
- Window
- ToolError
- run_batch
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
- time
- test_runner.py
- README.md
- swarmote_desktop.py
- ProfileRegistry
- Danh mục ảnh nằm trong dự án
- Giao diện vận hành
- Amazon trên Swarmote
- Nghiên cứu và tích hợp Swarmote
- PLAN.md
- Quy tắc tự động hóa sau menu ba gạch
- Bàn giao trạng thái dự án — 13/11/2026
- Amazon Android Tool — Giai đoạn A/B
- test_swarmote_navigation.py
- Thiết kế OTP cho từng Profile
- Kiểm tra độ phủ Graphify — 13/11/2026
- settings.py
- ToolError
- batch.py
- runner.py
- ProxyConfig

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 177 edges
2. `CloudPhone` - 76 edges
3. `Window` - 64 edges
4. `RunJob` - 44 edges
5. `main()` - 37 edges
6. `build_common_steps()` - 35 edges
7. `RunnerTests` - 34 edges
8. `AttemptDeadline` - 33 edges
9. `_read_nodes()` - 32 edges
10. `ProfileRegistry` - 31 edges

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

## Communities (38 total, 3 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.09
Nodes (38): main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play() (+30 more)

### Community 1 - "ToolError"
Cohesion: 0.08
Nodes (49): _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp(), name() (+41 more)

### Community 2 - "desktop.py"
Cohesion: 0.08
Nodes (12): _automatic_resume_slots(), _crystal_art(), main(), attempt_seconds(), PostMenuSession, PostMenuStep, AccountData, RunJob (+4 more)

### Community 3 - "Window"
Cohesion: 0.06
Nodes (13): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), validate_card(), _edge_light() (+5 more)

### Community 4 - "ToolError"
Cohesion: 0.08
Nodes (32): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+24 more)

### Community 5 - "run_batch"
Cohesion: 0.22
Nodes (7): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), Các bước

### Community 6 - "RunnerTests"
Cohesion: 0.09
Nodes (9): RunnerTests, create(), resume(), create(), failed_start(), resume(), run(), failed() (+1 more)

### Community 7 - "read_otp"
Cohesion: 0.12
Nodes (4): extract_otp(), _NoRedirect, read_otp(), OtpTests

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 10 - "BatchDraft"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (28): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại, Chung b8 — Proceed to create an account (+20 more)

### Community 12 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 13 - "BatchDraft"
Cohesion: 0.15
Nodes (9): BatchDraft, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng (+1 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.12
Nodes (16): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13, Nút New Profile trên Swarmote — 13/11/2026 (+8 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.12
Nodes (17): q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên, q1 ảnh 08 — Chọn SMS thay WhatsApp (+9 more)

### Community 17 - "time"
Cohesion: 0.16
Nodes (7): install_amazon(), open_adb_shell(), _phone_window(), show_apps(), _wait_for(), FakeControl, InstallTests

### Community 18 - "test_runner.py"
Cohesion: 0.16
Nodes (5): ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, lookup(), broken()

### Community 19 - "README.md"
Cohesion: 0.38
Nodes (3): Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 20 - "swarmote_desktop.py"
Cohesion: 0.15
Nodes (11): inspect(), _main_window(), _profile_row_status(), profile_status(), _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together() (+3 more)

### Community 21 - "ProfileRegistry"
Cohesion: 0.26
Nodes (3): ProfileRegistry, absent(), ProfileRegistryTests

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

### Community 30 - "test_swarmote_navigation.py"
Cohesion: 0.16
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 31 - "Thiết kế OTP cho từng Profile"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 32 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 33 - "settings.py"
Cohesion: 0.23
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 34 - "ToolError"
Cohesion: 0.26
Nodes (10): ToolError, _activate_manager(), _create_profile_form(), _descendants(), _invoke(), _one(), _profile_checkbox(), _profile_form_open() (+2 more)

### Community 35 - "batch.py"
Cohesion: 0.32
Nodes (5): BatchItem, parse_proxy_line(), prepare_five(), ready_for_registration(), BatchSafetyTests

### Community 36 - "runner.py"
Cohesion: 0.20
Nodes (4): ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyTestFailed, unavailable()

### Community 37 - "ProxyConfig"
Cohesion: 0.24
Nodes (4): create_profile(), ProxyConfig, Mục tiêu và bằng chứng, CreationWindowVisibilityTests

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 250 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `ToolError`, `desktop.py`, `Window`, `batch.py`, `ToolError`, `settings.py`, `read_otp`, `runner.py`, `run_batch`, `ProxyConfig`, `RunnerTests`, `BatchDraft`, `time`, `test_runner.py`, `swarmote_desktop.py`, `ProfileRegistry`, `test_swarmote_navigation.py`?**
  _High betweenness centrality (0.443) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `ToolError` (e.g. with `_visible()` and `BatchDraft`) actually correct?**
  _`ToolError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08842105263157894 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `ToolError` to `ToolError`, `desktop.py`, `ToolError`, `README.md`, `Quy tắc tự động hóa sau menu ba gạch`, `Bàn giao trạng thái dự án — 13/11/2026`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Should `ToolError` be split into smaller, more focused modules?**
  _Cohesion score 0.07653508771929825 - nodes in this community are weakly interconnected._
# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~52,464 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 888 nodes · 2770 edges · 36 communities (32 shown, 4 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 350 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `10bc8e71`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- CloudPhone
- wait_for_new_otp
- Window
- ToolError
- swarmote_desktop.py
- RunnerTests
- desktop.py
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- settings.py
- test_swarmote_navigation.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- ProxyConfig
- ToolError
- runner.py
- profile_status
- Danh mục ảnh nằm trong dự án
- Đã có trong graph
- unittest
- Giao diện vận hành
- Nghiên cứu và tích hợp Swarmote
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- Amazon Android Tool — Giai đoạn A/B
- File dự án mà Graphify không phân tích trực tiếp
- OTP_DESIGN.md
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026
- Kiểm tra độ phủ Graphify — 13/11/2026
- Điều hướng hai dạng menu ba gạch
- PLAN.md
- Luồng q1 từ menu ba gạch tới nhập OTP

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 185 edges
2. `CloudPhone` - 81 edges
3. `Window` - 65 edges
4. `build_common_steps()` - 50 edges
5. `RunJob` - 46 edges
6. `Q1FlowTests` - 46 edges
7. `main()` - 37 edges
8. `AttemptDeadline` - 37 edges
9. `_read_nodes()` - 34 edges
10. `node()` - 34 edges

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
Nodes (43): BatchItem, parse_proxy_line(), prepare_five(), main(), parser(), report(), adb(), app_data_dir() (+35 more)

### Community 1 - "CloudPhone"
Cohesion: 0.06
Nodes (62): _ActionNotResolved, _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp() (+54 more)

### Community 2 - "wait_for_new_otp"
Cohesion: 0.11
Nodes (7): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 3 - "Window"
Cohesion: 0.06
Nodes (12): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), validate_card(), _edge_light() (+4 more)

### Community 4 - "ToolError"
Cohesion: 0.08
Nodes (29): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+21 more)

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.14
Nodes (18): _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _open_profiles(), _profile_checkbox() (+10 more)

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (14): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+6 more)

### Community 7 - "desktop.py"
Cohesion: 0.10
Nodes (11): _automatic_resume_slots(), route(), attempt_seconds(), PostMenuSession, PostMenuStep, AccountData, RunJob, DesktopResumeTests (+3 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.36
Nodes (3): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.05
Nodes (32): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ (+24 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (31): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+23 more)

### Community 12 - "settings.py"
Cohesion: 0.08
Nodes (11): BatchDraft, _crystal_art(), main(), save(), default_path(), AppSettings, load_settings(), save_settings() (+3 more)

### Community 13 - "test_swarmote_navigation.py"
Cohesion: 0.21
Nodes (4): control(), ProfilesNavigationTests, descendants(), descendants()

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (18): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+10 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 17 - "ProxyConfig"
Cohesion: 0.19
Nodes (4): create_profile(), ProxyConfig, Mục tiêu và bằng chứng, CreationWindowVisibilityTests

### Community 18 - "ToolError"
Cohesion: 0.22
Nodes (10): ToolError, _nodes(), open_home_menu(), ready_for_home_menu(), _tap(), install_amazon(), open_adb_shell(), _phone_window() (+2 more)

### Community 19 - "runner.py"
Cohesion: 0.22
Nodes (4): ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyTestFailed, unavailable()

### Community 20 - "profile_status"
Cohesion: 0.15
Nodes (13): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), _profile_row_status(), profile_status() (+5 more)

### Community 21 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 22 - "Đã có trong graph"
Cohesion: 0.40
Nodes (3): _activate_manager(), _unfiltered_single_page(), Đã có trong graph

### Community 24 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 27 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 28 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.40
Nodes (5): Amazon Android Tool — Giai đoạn A/B, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 29 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 30 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 31 - "Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 32 - "Kiểm tra độ phủ Graphify — 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 33 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.67
Nodes (3): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 264 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `CloudPhone`, `wait_for_new_otp`, `Window`, `ToolError`, `swarmote_desktop.py`, `RunnerTests`, `desktop.py`, `settings.py`, `test_swarmote_navigation.py`, `ProxyConfig`, `runner.py`, `profile_status`, `Đã có trong graph`?**
  _High betweenness centrality (0.438) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07118967988533206 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `CloudPhone` to `wait_for_new_otp`, `Luồng q1 từ menu ba gạch tới nhập OTP`, `ToolError`, `desktop.py`, `PROJECT_INDEX.md`, `ToolError`, `Đã có trong graph`, `Quy tắc tự động hóa sau menu ba gạch`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Should `CloudPhone` be split into smaller, more focused modules?**
  _Cohesion score 0.05652951699463327 - nodes in this community are weakly interconnected._
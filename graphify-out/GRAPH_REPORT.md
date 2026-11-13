# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~50,111 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 866 nodes · 2692 edges · 45 communities (37 shown, 8 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 342 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d0bb0b9c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- build_common_steps
- ToolError
- Window
- ToolError
- start_profile
- RunnerTests
- ProxyConfig
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- CloudPhone
- AccountData
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- BatchDraft
- RunJob
- _read_nodes
- ProfilesNavigationTests
- run_batch
- runner.py
- time
- Danh mục ảnh nằm trong dự án
- Nghiên cứu và tích hợp Swarmote
- Giao diện vận hành
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- Amazon Android Tool — Giai đoạn A/B
- File dự án mà Graphify không phân tích trực tiếp
- GRAPH_AUDIT.md
- OTP_DESIGN.md
- MENU_ROUTING.md
- Bàn giao trạng thái dự án — 13/11/2026
- PLAN.md
- ._label
- account_flow.py
- FakeControl
- desktop.py
- route_list_menu
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- Đã có trong graph

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 177 edges
2. `CloudPhone` - 79 edges
3. `Window` - 64 edges
4. `RunJob` - 45 edges
5. `build_common_steps()` - 42 edges
6. `Q1FlowTests` - 38 edges
7. `main()` - 37 edges
8. `AttemptDeadline` - 35 edges
9. `_read_nodes()` - 34 edges
10. `RunnerTests` - 34 edges

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

## Communities (45 total, 8 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.11
Nodes (34): main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play() (+26 more)

### Community 1 - "build_common_steps"
Cohesion: 0.12
Nodes (6): build_common_steps(), build_q1_steps(), category(), Phần riêng từng máy, node(), Q1FlowTests

### Community 2 - "ToolError"
Cohesion: 0.05
Nodes (22): ToolError, save(), _nodes(), open_home_menu(), _tap(), extract_otp(), _NoRedirect, read_otp() (+14 more)

### Community 4 - "ToolError"
Cohesion: 0.09
Nodes (25): cloud_adb(), cloud_serials(), open_amazon(), foreground(), package_path(), probe(), prop(), reported_installer() (+17 more)

### Community 5 - "start_profile"
Cohesion: 0.15
Nodes (16): _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _profile_checkbox(), _profile_form_open() (+8 more)

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (14): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+6 more)

### Community 7 - "ProxyConfig"
Cohesion: 0.08
Nodes (15): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), parse_column(), parse_records(), _table_cells() (+7 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.06
Nodes (27): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật (+19 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (30): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại (+22 more)

### Community 12 - "CloudPhone"
Cohesion: 0.14
Nodes (10): home_visible(), resume_common_index(), verify_menu_open(), visit_home(), CloudPhone, reconcile(), AttemptDeadline, type_characters() (+2 more)

### Community 13 - "AccountData"
Cohesion: 0.21
Nodes (3): _automatic_resume_slots(), AccountData, DesktopResumeTests

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (19): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+11 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 18 - "RunJob"
Cohesion: 0.16
Nodes (6): attempt_seconds(), PostMenuSession, PostMenuStep, RunJob, PostMenuTests, first_step()

### Community 19 - "_read_nodes"
Cohesion: 0.24
Nodes (25): _at_or_after(), continue_number(), country(), create_account(), enter_otp(), focus_phone(), name(), phone_number() (+17 more)

### Community 20 - "ProfilesNavigationTests"
Cohesion: 0.16
Nodes (7): _open_profiles(), ProfileCreateNotSubmitted, visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 21 - "run_batch"
Cohesion: 0.16
Nodes (10): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), _profile_row_status(), profile_status() (+2 more)

### Community 22 - "runner.py"
Cohesion: 0.22
Nodes (3): ProfileManagerWindowError, ProxyTestFailed, unavailable()

### Community 23 - "time"
Cohesion: 0.25
Nodes (6): ready_for_home_menu(), install_amazon(), open_adb_shell(), _phone_window(), show_apps(), _wait_for()

### Community 24 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 26 - "Giao diện vận hành"
Cohesion: 0.40
Nodes (4): Bố cục, Giao diện vận hành, Hướng thị giác, Quy tắc

### Community 27 - "Quy tắc tự động hóa sau menu ba gạch"
Cohesion: 0.40
Nodes (5): Nhận diện giao diện lúc chạy, Nhập liệu và lỗi, Quy tắc tự động hóa sau menu ba gạch, Trạng thái hiện tại của dự án, Từng máy độc lập

### Community 28 - "Amazon trên Swarmote"
Cohesion: 0.40
Nodes (4): Amazon trên Swarmote, Người dùng và công việc, Nền tảng, Điều chưa xác minh

### Community 29 - "Amazon Android Tool — Giai đoạn A/B"
Cohesion: 0.40
Nodes (5): Amazon Android Tool — Giai đoạn A/B, Sử dụng, Trạng thái nghiệm thu, Yêu cầu, Điện thoại đám mây Swarmote

### Community 30 - "File dự án mà Graphify không phân tích trực tiếp"
Cohesion: 0.40
Nodes (5): File dự án mà Graphify không phân tích trực tiếp, .gitignore, Launch Swarmote Tool.pyw, pyproject.toml, Ảnh PNG trong dự án

### Community 31 - "GRAPH_AUDIT.md"
Cohesion: 0.67
Nodes (3): Cách kiểm tra sau mỗi sửa đổi, Giới hạn đã xác nhận, Kiểm tra độ phủ Graphify — 13/11/2026

### Community 32 - "OTP_DESIGN.md"
Cohesion: 0.50
Nodes (3): Nối vào bước tạo tài khoản sau khi xác minh màn hình Amazon, Thiết kế OTP cho từng Profile, Đã chuẩn bị

### Community 33 - "MENU_ROUTING.md"
Cohesion: 0.27
Nodes (6): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 34 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.67
Nodes (3): Bàn giao trạng thái dự án — 13/11/2026, Mục tiêu và quy tắc đã chốt, Tài liệu chi tiết

### Community 37 - "account_flow.py"
Cohesion: 0.22
Nodes (12): _bounds(), _button(), _find_scrolling(), _national_phone(), _parse_ui_nodes(), _RegistrationState, _scroll_up(), _text() (+4 more)

### Community 39 - "desktop.py"
Cohesion: 0.12
Nodes (5): validate_card(), _crystal_art(), main(), otp_token(), validate_otp_url()

### Community 41 - "route_list_menu"
Cohesion: 0.33
Nodes (4): menu_layout(), route_list_menu(), route(), Mã hiện có

### Community 42 - "Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 43 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 44 - "Đã có trong graph"
Cohesion: 0.40
Nodes (3): _activate_manager(), _unfiltered_single_page(), Đã có trong graph

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 262 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `build_common_steps`, `Window`, `ToolError`, `start_profile`, `RunnerTests`, `ProxyConfig`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`, `CloudPhone`, `BatchDraft`, `RunJob`, `_read_nodes`, `ProfilesNavigationTests`, `run_batch`, `runner.py`, `time`, `account_flow.py`, `desktop.py`, `._apply_bulk_text`, `Đã có trong graph`?**
  _High betweenness centrality (0.438) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `ToolError` (e.g. with `_visible()` and `BatchDraft`) actually correct?**
  _`ToolError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10855094726062468 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `build_common_steps` to `MENU_ROUTING.md`, `ToolError`, `account_flow.py`, `route_list_menu`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`, `CloudPhone`, `Đã có trong graph`, `RunJob`, `_read_nodes`, `Quy tắc tự động hóa sau menu ba gạch`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.12477718360071301 - nodes in this community are weakly interconnected._
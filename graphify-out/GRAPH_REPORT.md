# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~53,312 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 898 nodes · 2815 edges · 45 communities (39 shown, 6 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 356 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a140edb4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- build_common_steps
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
- ToolError
- account_flow.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- desktop.py
- _read_nodes
- desktop.py
- profile_status
- Danh mục ảnh nằm trong dự án
- ProfileRegistry
- RunJob
- Giao diện vận hành
- Nghiên cứu và tích hợp Swarmote
- Quy tắc tự động hóa sau menu ba gạch
- Amazon trên Swarmote
- Amazon Android Tool — Giai đoạn A/B
- File dự án mà Graphify không phân tích trực tiếp
- OTP_DESIGN.md
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026
- Kiểm tra độ phủ Graphify — 13/11/2026
- MENU_ROUTING.md
- PLAN.md
- CloudPhone
- visit_home
- ProfilesNavigationTests
- _create_profile_form
- Bàn giao trạng thái dự án — 13/11/2026
- test_q1_flow.py
- _main_window
- open_home_menu
- FakeControl

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 187 edges
2. `CloudPhone` - 84 edges
3. `Window` - 65 edges
4. `build_common_steps()` - 51 edges
5. `Q1FlowTests` - 49 edges
6. `RunJob` - 46 edges
7. `AttemptDeadline` - 39 edges
8. `main()` - 37 edges
9. `node()` - 37 edges
10. `_read_nodes()` - 34 edges

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

## Communities (45 total, 6 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.09
Nodes (38): main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play() (+30 more)

### Community 1 - "build_common_steps"
Cohesion: 0.09
Nodes (7): build_common_steps(), build_q1_steps(), category(), Phần riêng từng máy, node(), Q1FlowTests, provider_read()

### Community 2 - "wait_for_new_otp"
Cohesion: 0.11
Nodes (7): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 3 - "Window"
Cohesion: 0.06
Nodes (14): BatchDraft, validate_card(), _edge_light(), Window, otp_token(), 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc (+6 more)

### Community 4 - "ToolError"
Cohesion: 0.08
Nodes (25): cloud_adb(), cloud_screenshot(), cloud_serials(), foreground(), package_path(), probe(), prop(), reported_installer() (+17 more)

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.15
Nodes (17): open_amazon(), ready_for_home_menu(), _descendants(), install_amazon(), _one(), open_adb_shell(), _phone_window(), _profile_checkbox() (+9 more)

### Community 6 - "RunnerTests"
Cohesion: 0.09
Nodes (9): RunnerTests, create(), resume(), create(), failed_start(), resume(), run(), failed() (+1 more)

### Community 7 - "desktop.py"
Cohesion: 0.17
Nodes (6): reconcile(), route(), PostMenuSession, PostMenuStep, PostMenuTests, first_step()

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.06
Nodes (27): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật (+19 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (31): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+23 more)

### Community 12 - "ToolError"
Cohesion: 0.20
Nodes (8): BatchItem, parse_proxy_line(), prepare_five(), ToolError, create_profile(), ProxyConfig, BatchSafetyTests, CreationWindowVisibilityTests

### Community 13 - "account_flow.py"
Cohesion: 0.17
Nodes (19): _ActionNotResolved, _bounds(), _button(), _find_scrolling(), _form_action(), _has(), home_visible(), _parse_ui_nodes() (+11 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (19): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+11 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 17 - "desktop.py"
Cohesion: 0.06
Nodes (16): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), _crystal_art(), main() (+8 more)

### Community 18 - "_read_nodes"
Cohesion: 0.21
Nodes (27): _at_or_after(), continue_number(), country(), create_account(), enter_otp(), focus_otp(), focus_phone(), name() (+19 more)

### Community 19 - "desktop.py"
Cohesion: 0.19
Nodes (4): ProfileManagerWindowError, ProfileNotFound, lookup(), unavailable()

### Community 20 - "profile_status"
Cohesion: 0.22
Nodes (7): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), Các bước

### Community 21 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 22 - "ProfileRegistry"
Cohesion: 0.24
Nodes (4): ProfileRegistry, absent(), ProfileRegistryTests, broken()

### Community 23 - "RunJob"
Cohesion: 0.22
Nodes (4): _automatic_resume_slots(), AccountData, RunJob, DesktopResumeTests

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

### Community 33 - "MENU_ROUTING.md"
Cohesion: 0.27
Nodes (6): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch, Luồng q1 từ menu ba gạch tới nhập OTP, Thử trên q1 đã có, Luồng q2 từ menu ba gạch

### Community 35 - "CloudPhone"
Cohesion: 0.17
Nodes (7): verify_menu_open(), CloudPhone, attempt_seconds(), AttemptDeadline, type_characters(), build_q2_steps(), Q2FlowTests

### Community 37 - "ProfilesNavigationTests"
Cohesion: 0.17
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "_create_profile_form"
Cohesion: 0.16
Nodes (9): _activate_manager(), _create_profile_form(), _invoke(), _profile_form_open(), ProfileCreateNotSubmitted, ProxyTestFailed, _select_radio(), _unfiltered_single_page() (+1 more)

### Community 40 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.67
Nodes (3): Bàn giao trạng thái dự án — 13/11/2026, Mục tiêu và quy tắc đã chốt, Tài liệu chi tiết

### Community 41 - "test_q1_flow.py"
Cohesion: 0.25
Nodes (4): menu_layout(), resume_common_index(), route_list_menu(), Quy tắc chạy

### Community 42 - "_main_window"
Cohesion: 0.22
Nodes (6): inspect(), _main_window(), _select_profile_rows(), _selected_profile_names(), start_profiles_together(), _wait_for_selected()

### Community 43 - "open_home_menu"
Cohesion: 0.31
Nodes (4): _nodes(), open_home_menu(), _tap(), HomeMenuTests

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 265 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `build_common_steps`, `wait_for_new_otp`, `Window`, `ToolError`, `swarmote_desktop.py`, `RunnerTests`, `desktop.py`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`, `account_flow.py`, `desktop.py`, `_read_nodes`, `desktop.py`, `profile_status`, `ProfileRegistry`, `CloudPhone`, `visit_home`, `ProfilesNavigationTests`, `_create_profile_form`, `unittest`, `test_q1_flow.py`, `_main_window`, `open_home_menu`?**
  _High betweenness centrality (0.437) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 29 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09181784524250278 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `build_common_steps` to `MENU_ROUTING.md`, `wait_for_new_otp`, `CloudPhone`, `ToolError`, `visit_home`, `_create_profile_form`, `desktop.py`, `test_q1_flow.py`, `ToolError`, `account_flow.py`, `_read_nodes`, `RunJob`, `Quy tắc tự động hóa sau menu ba gạch`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.09065679925994449 - nodes in this community are weakly interconnected._
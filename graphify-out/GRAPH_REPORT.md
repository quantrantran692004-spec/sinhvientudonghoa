# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~53,587 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 899 nodes · 2822 edges · 36 communities (28 shown, 8 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 360 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e9e4c84f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- build_common_steps
- wait_for_new_otp
- Window
- ToolError
- runner.py
- RunnerTests
- desktop.py
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- parse_records
- account_flow.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- profile_registry.py
- _read_nodes
- profile_status
- profile_status
- BatchDraft
- ._label
- _find_scrolling
- ._apply_bulk_text
- Nghiên cứu và tích hợp Swarmote
- validate_card
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- build_q1_steps
- CloudPhone
- ProfilesNavigationTests
- _create_profile_form
- test_q1_flow.py
- _main_window
- FakeControl

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 187 edges
2. `CloudPhone` - 84 edges
3. `Window` - 65 edges
4. `build_common_steps()` - 52 edges
5. `Q1FlowTests` - 50 edges
6. `RunJob` - 46 edges
7. `AttemptDeadline` - 39 edges
8. `node()` - 38 edges
9. `main()` - 37 edges
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

## Communities (36 total, 8 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.06
Nodes (52): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), _table_cells(), _url_from_cell(), main() (+44 more)

### Community 1 - "build_common_steps"
Cohesion: 0.11
Nodes (4): build_common_steps(), node(), Q1FlowTests, provider_read()

### Community 2 - "wait_for_new_otp"
Cohesion: 0.11
Nodes (7): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 4 - "ToolError"
Cohesion: 0.08
Nodes (32): cloud_adb(), cloud_screenshot(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe() (+24 more)

### Community 5 - "runner.py"
Cohesion: 0.18
Nodes (5): ready_for_home_menu(), install_amazon(), open_adb_shell(), _phone_window(), show_apps()

### Community 6 - "RunnerTests"
Cohesion: 0.07
Nodes (14): ProfileRegistry, absent(), ProfileRegistryTests, lookup(), broken(), RunnerTests, create(), resume() (+6 more)

### Community 7 - "desktop.py"
Cohesion: 0.07
Nodes (13): _automatic_resume_slots(), _crystal_art(), main(), route(), attempt_seconds(), PostMenuSession, PostMenuStep, AccountData (+5 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.05
Nodes (45): Hướng dẫn khi tiếp tục dự án, amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án (+37 more)

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.07
Nodes (25): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc (+17 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (31): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+23 more)

### Community 12 - "parse_records"
Cohesion: 0.21
Nodes (3): parse_column(), parse_records(), BulkInputTests

### Community 13 - "account_flow.py"
Cohesion: 0.19
Nodes (14): _ActionNotResolved, _bounds(), _button(), _form_action(), _has(), _parse_ui_nodes(), _read_nodes_once(), _RegistrationState (+6 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (18): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+10 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 17 - "profile_registry.py"
Cohesion: 0.21
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 18 - "_read_nodes"
Cohesion: 0.19
Nodes (28): _at_or_after(), continue_number(), create_account(), enter_otp(), focus_otp(), focus_phone(), name(), phone_number() (+20 more)

### Community 19 - "profile_status"
Cohesion: 0.31
Nodes (6): _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, Nút New Profile trên Swarmote — 13/11/2026

### Community 20 - "profile_status"
Cohesion: 0.22
Nodes (7): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), Các bước

### Community 23 - "_find_scrolling"
Cohesion: 0.39
Nodes (4): country(), _find_scrolling(), _text(), _unique()

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

### Community 27 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 31 - "build_q1_steps"
Cohesion: 0.18
Nodes (7): resume_common_index(), build_q1_steps(), category(), Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Phần riêng từng máy, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

### Community 35 - "CloudPhone"
Cohesion: 0.23
Nodes (3): verify_menu_open(), AttemptDeadline, type_characters()

### Community 37 - "ProfilesNavigationTests"
Cohesion: 0.15
Nodes (8): _descendants(), _open_profiles(), visible_profile_names(), _wait_for(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 38 - "_create_profile_form"
Cohesion: 0.16
Nodes (14): _activate_manager(), _create_profile_form(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), ProfileCreateNotSubmitted, ProfileManagerWindowError (+6 more)

### Community 41 - "test_q1_flow.py"
Cohesion: 0.16
Nodes (9): menu_layout(), _national_phone(), route_list_menu(), Quy tắc chạy, Bàn giao trạng thái dự án — 13/11/2026, Mã hiện có, Mục tiêu và quy tắc đã chốt, Trạng thái kiểm chứng và giới hạn (+1 more)

### Community 42 - "_main_window"
Cohesion: 0.17
Nodes (8): inspect(), _main_window(), _select_profile_rows(), _selected_profile_names(), start_profile(), start_profiles_together(), _swarmote_exe(), _wait_for_selected()

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 265 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `core.py` to `build_common_steps`, `wait_for_new_otp`, `Window`, `ToolError`, `runner.py`, `RunnerTests`, `desktop.py`, `parse_records`, `account_flow.py`, `profile_registry.py`, `_read_nodes`, `profile_status`, `profile_status`, `BatchDraft`, `_find_scrolling`, `._apply_bulk_text`, `validate_card`, `CloudPhone`, `ProfilesNavigationTests`, `_create_profile_form`, `unittest`, `test_q1_flow.py`, `_main_window`?**
  _High betweenness centrality (0.437) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 29 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05772113943028486 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `build_common_steps` to `core.py`, `wait_for_new_otp`, `CloudPhone`, `ToolError`, `_create_profile_form`, `desktop.py`, `PROJECT_INDEX.md`, `test_q1_flow.py`, `account_flow.py`, `_read_nodes`, `_find_scrolling`, `build_q1_steps`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.1073170731707317 - nodes in this community are weakly interconnected._
# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~52,079 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 883 nodes · 2755 edges · 22 communities (20 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 347 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5154d3b3`
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
- start_profiles_together
- _main_window
- unittest
- Nghiên cứu và tích hợp Swarmote

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 182 edges
2. `CloudPhone` - 80 edges
3. `Window` - 65 edges
4. `build_common_steps()` - 49 edges
5. `RunJob` - 46 edges
6. `Q1FlowTests` - 44 edges
7. `main()` - 37 edges
8. `AttemptDeadline` - 36 edges
9. `RunnerTests` - 34 edges
10. `_read_nodes()` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Trạng thái hiện tại của dự án` --references--> `build_common_steps()`  [INFERRED]
  POST_MENU_REQUIREMENTS.md → amazon_android/account_flow.py
- `Thử trên q1 đã có` --references--> `build_common_steps()`  [INFERRED]
  Q1_FLOW.md → amazon_android/account_flow.py
- `Luồng q2 từ menu ba gạch` --references--> `build_common_steps()`  [INFERRED]
  Q2_FLOW.md → amazon_android/account_flow.py
- `Các bước` --references--> `prepare_five()`  [INFERRED]
  plans/003-runner-states.md → amazon_android/batch.py
- `Sử dụng` --references--> `doctor()`  [INFERRED]
  README.md → amazon_android/core.py

## Import Cycles
- None detected.

## Communities (22 total, 2 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.07
Nodes (44): BatchItem, parse_proxy_line(), prepare_five(), _table_cells(), main(), parser(), report(), adb() (+36 more)

### Community 1 - "CloudPhone"
Cohesion: 0.06
Nodes (63): _ActionNotResolved, _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp() (+55 more)

### Community 2 - "wait_for_new_otp"
Cohesion: 0.11
Nodes (6): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests

### Community 3 - "Window"
Cohesion: 0.06
Nodes (12): BulkRecord, lines(), parse_column(), parse_records(), _url_from_cell(), validate_card(), _edge_light(), Window (+4 more)

### Community 4 - "ToolError"
Cohesion: 0.08
Nodes (37): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+29 more)

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.17
Nodes (16): _activate_manager(), _create_profile_form(), _descendants(), _invoke(), _one(), _profile_checkbox(), _profile_form_open(), _profile_row_status() (+8 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (24): emit(), ProfileRegistry, run_batch(), fill_slots(), refresh_slots(), visible_lookup(), ProfileLookupError, ProfileNotFound (+16 more)

### Community 7 - "desktop.py"
Cohesion: 0.07
Nodes (13): _automatic_resume_slots(), reconcile(), route(), attempt_seconds(), PostMenuSession, PostMenuStep, type_characters(), AccountData (+5 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.19
Nodes (3): BatchStartTests, descendants(), FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.05
Nodes (45): Hướng dẫn khi tiếp tục dự án, amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án (+37 more)

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.05
Nodes (30): BatchDraft, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng (+22 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (31): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+23 more)

### Community 12 - "settings.py"
Cohesion: 0.11
Nodes (9): _crystal_art(), main(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path() (+1 more)

### Community 13 - "test_swarmote_navigation.py"
Cohesion: 0.16
Nodes (7): _open_profiles(), ProfileCreateNotSubmitted, visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (18): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+10 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 17 - "ProxyConfig"
Cohesion: 0.14
Nodes (8): create_profile(), ProxyConfig, Giới hạn và lựa chọn cần xác minh, Kế hoạch sửa luồng mẻ Swarmote, Kết luận đã xác minh, Quy trình đích, Thứ tự thực hiện, CreationWindowVisibilityTests

### Community 18 - "start_profiles_together"
Cohesion: 0.16
Nodes (7): _select_profile_rows(), _selected_profile_names(), start_profiles_together(), _wait_for_selected(), checkbox(), toggle(), FakeBox

### Community 19 - "_main_window"
Cohesion: 0.22
Nodes (5): inspect(), _main_window(), ProfileManagerWindowError, _swarmote_exe(), unavailable()

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 263 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `CloudPhone`, `wait_for_new_otp`, `Window`, `swarmote_desktop.py`, `RunnerTests`, `desktop.py`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`, `settings.py`, `test_swarmote_navigation.py`, `ProxyConfig`, `start_profiles_together`, `_main_window`?**
  _High betweenness centrality (0.436) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_visible()`) actually correct?**
  _`ToolError` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0694249649368864 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `CloudPhone` to `wait_for_new_otp`, `ToolError`, `swarmote_desktop.py`, `desktop.py`, `PROJECT_INDEX.md`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Should `CloudPhone` be split into smaller, more focused modules?**
  _Cohesion score 0.05832258064516129 - nodes in this community are weakly interconnected._
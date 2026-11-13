# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~51,524 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 876 nodes · 2738 edges · 23 communities (17 shown, 6 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 345 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `de2dad55`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- CloudPhone
- wait_for_new_otp
- Window
- ToolError
- ToolError
- RunnerTests
- desktop.py
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- settings.py
- bulk_input.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- desktop.py
- parse_records
- otp.py
- validate_card
- unittest
- Nghiên cứu và tích hợp Swarmote

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 181 edges
2. `CloudPhone` - 80 edges
3. `Window` - 65 edges
4. `RunJob` - 46 edges
5. `build_common_steps()` - 45 edges
6. `Q1FlowTests` - 42 edges
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

## Communities (23 total, 6 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.08
Nodes (39): _table_cells(), main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names() (+31 more)

### Community 1 - "CloudPhone"
Cohesion: 0.06
Nodes (60): _ActionNotResolved, _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp() (+52 more)

### Community 2 - "wait_for_new_otp"
Cohesion: 0.16
Nodes (7): extract_otp(), read_otp(), _read_otp_in_browser(), timeout_ms(), validate_otp_url(), wait_for_new_otp(), OtpTests

### Community 3 - "Window"
Cohesion: 0.07
Nodes (12): BatchDraft, _edge_light(), Window, 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi (+4 more)

### Community 4 - "ToolError"
Cohesion: 0.08
Nodes (32): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+24 more)

### Community 5 - "ToolError"
Cohesion: 0.06
Nodes (46): BatchItem, parse_proxy_line(), prepare_five(), ToolError, ready_for_home_menu(), _activate_manager(), create_profile(), _create_profile_form() (+38 more)

### Community 6 - "RunnerTests"
Cohesion: 0.05
Nodes (24): emit(), ProfileRegistry, _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), ProfileLookupError (+16 more)

### Community 7 - "desktop.py"
Cohesion: 0.07
Nodes (11): _automatic_resume_slots(), attempt_seconds(), PostMenuSession, PostMenuStep, type_characters(), AccountData, RunJob, DesktopResumeTests (+3 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 9 - "PROJECT_INDEX.md"
Cohesion: 0.05
Nodes (45): Hướng dẫn khi tiếp tục dự án, amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án (+37 more)

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.06
Nodes (26): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước (+18 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (30): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại (+22 more)

### Community 12 - "settings.py"
Cohesion: 0.19
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (19): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+11 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 18 - "parse_records"
Cohesion: 0.19
Nodes (4): lines(), parse_column(), parse_records(), BulkInputTests

### Community 25 - "Nghiên cứu và tích hợp Swarmote"
Cohesion: 0.40
Nodes (4): Hành vi có bằng chứng, Kiểm thử còn lại, Nghiên cứu và tích hợp Swarmote, Phần đã áp dụng

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 261 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `CloudPhone`, `wait_for_new_otp`, `Window`, `ToolError`, `RunnerTests`, `desktop.py`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`, `settings.py`, `bulk_input.py`, `desktop.py`, `parse_records`, `otp.py`, `validate_card`?**
  _High betweenness centrality (0.435) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_visible()`) actually correct?**
  _`ToolError` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08179012345679013 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `CloudPhone` to `wait_for_new_otp`, `ToolError`, `ToolError`, `desktop.py`, `PROJECT_INDEX.md`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Should `CloudPhone` be split into smaller, more focused modules?**
  _Cohesion score 0.0631184407796102 - nodes in this community are weakly interconnected._
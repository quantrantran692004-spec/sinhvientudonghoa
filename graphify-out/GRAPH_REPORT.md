# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~53,183 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 897 nodes · 2812 edges · 41 communities (35 shown, 6 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 356 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `930932a4`
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
- settings.py
- account_flow.py
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- ToolError
- _read_nodes
- desktop.py
- profile_status
- Danh mục ảnh nằm trong dự án
- ProfileRegistry
- desktop.py
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
- ._refresh_devices
- validate_otp_url
- build_q1_steps
- Bàn giao trạng thái dự án — 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 187 edges
2. `CloudPhone` - 84 edges
3. `Window` - 65 edges
4. `build_common_steps()` - 51 edges
5. `Q1FlowTests` - 48 edges
6. `RunJob` - 46 edges
7. `AttemptDeadline` - 39 edges
8. `main()` - 37 edges
9. `node()` - 36 edges
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

## Communities (41 total, 6 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.09
Nodes (39): _table_cells(), main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names() (+31 more)

### Community 1 - "build_common_steps"
Cohesion: 0.11
Nodes (4): build_common_steps(), node(), Q1FlowTests, provider_read()

### Community 2 - "wait_for_new_otp"
Cohesion: 0.11
Nodes (6): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), wait_for_new_otp(), OtpTests

### Community 4 - "ToolError"
Cohesion: 0.09
Nodes (26): cloud_adb(), cloud_screenshot(), cloud_serials(), open_amazon(), foreground(), package_path(), probe(), prop() (+18 more)

### Community 5 - "swarmote_desktop.py"
Cohesion: 0.05
Nodes (37): ready_for_home_menu(), _activate_manager(), _create_profile_form(), _descendants(), inspect(), install_amazon(), _invoke(), _main_window() (+29 more)

### Community 6 - "RunnerTests"
Cohesion: 0.09
Nodes (8): RunnerTests, create(), resume(), create(), failed_start(), resume(), run(), run()

### Community 7 - "desktop.py"
Cohesion: 0.20
Nodes (6): attempt_seconds(), PostMenuSession, PostMenuStep, RunJob, PostMenuTests, first_step()

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.06
Nodes (27): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Các bước, Kiểm tra bắt buộc, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật (+19 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.06
Nodes (31): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11 — Lấy và gõ OTP SMS, Chung b11a — Chạm ô OTP trên màn SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1 (+23 more)

### Community 12 - "settings.py"
Cohesion: 0.19
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 13 - "account_flow.py"
Cohesion: 0.16
Nodes (16): _ActionNotResolved, _bounds(), _button(), _find_scrolling(), _form_action(), _national_phone(), _parse_ui_nodes(), _RegistrationState (+8 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.08
Nodes (23): _nodes(), open_home_menu(), _tap(), HomeMenuTests, Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng (+15 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 17 - "ToolError"
Cohesion: 0.06
Nodes (24): BatchItem, parse_proxy_line(), prepare_five(), BatchDraft, BulkRecord, lines(), parse_column(), parse_records() (+16 more)

### Community 18 - "_read_nodes"
Cohesion: 0.20
Nodes (25): _at_or_after(), continue_number(), country(), create_account(), enter_otp(), focus_otp(), focus_phone(), name() (+17 more)

### Community 19 - "desktop.py"
Cohesion: 0.13
Nodes (7): ProfileCreateNotSubmitted, ProfileManagerWindowError, ProfileNotFound, ProxyTestFailed, lookup(), unavailable(), failed()

### Community 20 - "profile_status"
Cohesion: 0.23
Nodes (6): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup()

### Community 21 - "Danh mục ảnh nằm trong dự án"
Cohesion: 0.29
Nodes (7): amazon_android/assets/obsidian_prism.png, assets/ui_history/reset_check.png, assets/ui_history/ui-12.png, assets/ui_history/ui_palette_preview.png, assets/ui_history/ui-preview.png, assets/ui_history/ui-screenshot.png, Danh mục ảnh nằm trong dự án

### Community 22 - "ProfileRegistry"
Cohesion: 0.22
Nodes (4): ProfileRegistry, absent(), ProfileRegistryTests, broken()

### Community 23 - "desktop.py"
Cohesion: 0.12
Nodes (5): _automatic_resume_slots(), _crystal_art(), main(), AccountData, DesktopResumeTests

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
Cohesion: 0.20
Nodes (7): resume_common_index(), CloudPhone, reconcile(), AttemptDeadline, type_characters(), build_q2_steps(), Q2FlowTests

### Community 36 - "visit_home"
Cohesion: 0.16
Nodes (8): menu_layout(), _read_nodes_once(), route_list_menu(), _UiReadIncomplete, visit_home(), route(), Quy tắc chạy, Mã hiện có

### Community 39 - "build_q1_steps"
Cohesion: 0.24
Nodes (7): _ensure_menu(), _tap(), build_q1_steps(), category(), action(), pets(), Phần riêng từng máy

### Community 40 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.67
Nodes (3): Bàn giao trạng thái dự án — 13/11/2026, Mục tiêu và quy tắc đã chốt, Tài liệu chi tiết

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 265 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `build_common_steps`, `wait_for_new_otp`, `Window`, `ToolError`, `swarmote_desktop.py`, `RunnerTests`, `desktop.py`, `settings.py`, `account_flow.py`, `Biên bản kiểm tra thực tế — 2026-11-12`, `_read_nodes`, `desktop.py`, `profile_status`, `ProfileRegistry`, `desktop.py`, `CloudPhone`, `visit_home`, `._refresh_devices`, `validate_otp_url`, `build_q1_steps`?**
  _High betweenness centrality (0.437) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_tap_for_transition()`) actually correct?**
  _`ToolError` has 29 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08558108558108558 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `build_common_steps` to `MENU_ROUTING.md`, `wait_for_new_otp`, `CloudPhone`, `ToolError`, `swarmote_desktop.py`, `visit_home`, `desktop.py`, `build_q1_steps`, `account_flow.py`, `ToolError`, `_read_nodes`, `Quy tắc tự động hóa sau menu ba gạch`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Should `build_common_steps` be split into smaller, more focused modules?**
  _Cohesion score 0.11025641025641025 - nodes in this community are weakly interconnected._
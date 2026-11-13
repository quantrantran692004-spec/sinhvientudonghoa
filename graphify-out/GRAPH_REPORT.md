# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~51,297 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 874 nodes · 2728 edges · 37 communities (31 shown, 6 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 344 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a67c8b5f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- CloudPhone
- profile_status
- Window
- ToolError
- start_profile
- RunnerTests
- desktop.py
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Danh mục từng bước đã biết — 13/11/2026
- settings.py
- BatchDraft
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- ProfileRegistry
- ProxyConfig
- ProfilesNavigationTests
- runner.py
- runner.py
- unittest
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
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 181 edges
2. `CloudPhone` - 80 edges
3. `Window` - 65 edges
4. `RunJob` - 46 edges
5. `build_common_steps()` - 43 edges
6. `Q1FlowTests` - 41 edges
7. `main()` - 37 edges
8. `AttemptDeadline` - 36 edges
9. `RunnerTests` - 34 edges
10. `_read_nodes()` - 33 edges

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

## Communities (37 total, 6 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.08
Nodes (39): _table_cells(), main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names() (+31 more)

### Community 1 - "CloudPhone"
Cohesion: 0.06
Nodes (56): _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp(), focus_phone() (+48 more)

### Community 2 - "profile_status"
Cohesion: 0.18
Nodes (10): visible_lookup(), _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, _unfiltered_single_page(), Thiết kế yêu cầu, lookup() (+2 more)

### Community 3 - "Window"
Cohesion: 0.05
Nodes (13): validate_card(), _edge_light(), Window, extract_otp(), _NoRedirect, otp_token(), read_otp(), _read_otp_in_browser() (+5 more)

### Community 4 - "ToolError"
Cohesion: 0.09
Nodes (29): cloud_adb(), cloud_serials(), CloudPhone, foreground(), package_path(), probe(), prop(), reported_installer() (+21 more)

### Community 5 - "start_profile"
Cohesion: 0.12
Nodes (26): open_amazon(), ToolError, ready_for_home_menu(), _activate_manager(), _create_profile_form(), _descendants(), inspect(), install_amazon() (+18 more)

### Community 6 - "RunnerTests"
Cohesion: 0.09
Nodes (9): RunnerTests, create(), resume(), create(), failed_start(), resume(), run(), failed() (+1 more)

### Community 7 - "desktop.py"
Cohesion: 0.09
Nodes (11): _automatic_resume_slots(), reconcile(), route(), attempt_seconds(), PostMenuSession, AccountData, RunJob, DesktopResumeTests (+3 more)

### Community 8 - ".test_only_confirmed_target_names_are_selected_for_one_start_command"
Cohesion: 0.11
Nodes (6): BatchStartTests, checkbox(), toggle(), descendants(), FakeBox, FakeButton

### Community 10 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.05
Nodes (32): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng, 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ (+24 more)

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (30): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại (+22 more)

### Community 12 - "settings.py"
Cohesion: 0.12
Nodes (9): _crystal_art(), main(), save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path() (+1 more)

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.11
Nodes (18): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+10 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 17 - "ProfileRegistry"
Cohesion: 0.26
Nodes (3): ProfileRegistry, absent(), ProfileRegistryTests

### Community 18 - "ProxyConfig"
Cohesion: 0.10
Nodes (12): BatchItem, parse_proxy_line(), prepare_five(), BulkRecord, lines(), parse_column(), parse_records(), _url_from_cell() (+4 more)

### Community 20 - "ProfilesNavigationTests"
Cohesion: 0.18
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 21 - "runner.py"
Cohesion: 0.15
Nodes (6): create_profile(), ProfileCreateNotSubmitted, ProfileManagerWindowError, ProxyTestFailed, Mục tiêu và bằng chứng, unavailable()

### Community 22 - "runner.py"
Cohesion: 0.24
Nodes (6): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), Các bước

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

### Community 42 - "Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 261 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `start_profile` to `core.py`, `CloudPhone`, `profile_status`, `Window`, `ToolError`, `RunnerTests`, `desktop.py`, `settings.py`, `BatchDraft`, `ProfileRegistry`, `ProxyConfig`, `unittest`, `ProfilesNavigationTests`, `runner.py`, `runner.py`?**
  _High betweenness centrality (0.438) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `ToolError` (e.g. with `_read_nodes()` and `_visible()`) actually correct?**
  _`ToolError` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07846018219218337 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `CloudPhone` to `MENU_ROUTING.md`, `Window`, `ToolError`, `start_profile`, `desktop.py`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`, `Quy tắc tự động hóa sau menu ba gạch`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Should `CloudPhone` be split into smaller, more focused modules?**
  _Cohesion score 0.06349862258953168 - nodes in this community are weakly interconnected._
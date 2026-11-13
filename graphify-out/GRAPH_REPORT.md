# Graph Report - sinhvien  (2026-11-13)

## Corpus Check
- 66 files · ~50,815 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .pyw 1)

## Summary
- 870 nodes · 2709 edges · 42 communities (37 shown, 5 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 341 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a979ff41`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- CloudPhone
- otp.py
- Window
- ToolError
- start_profile
- RunnerTests
- desktop.py
- .test_only_confirmed_target_names_are_selected_for_one_start_command
- PROJECT_INDEX.md
- plans/README.md
- Danh mục từng bước đã biết — 13/11/2026
- settings.py
- BatchDraft
- Biên bản kiểm tra thực tế — 2026-11-12
- amazon-android-tool
- Ảnh hướng dẫn q1/q2 lưu cục bộ
- batch.py
- ProxyConfig
- ProfilesNavigationTests
- profile_status
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
- Điều hướng hai dạng menu ba gạch
- Bàn giao trạng thái dự án — 13/11/2026
- PLAN.md
- 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật
- 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng
- 004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ
- 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ
- Luồng q1 từ menu ba gạch tới nhập OTP
- Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

## God Nodes (most connected - your core abstractions)
1. `ToolError` - 179 edges
2. `CloudPhone` - 79 edges
3. `Window` - 65 edges
4. `RunJob` - 46 edges
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

## Communities (42 total, 5 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.09
Nodes (38): main(), parser(), report(), adb(), app_data_dir(), available_memory_mb(), avd_names(), check_play() (+30 more)

### Community 1 - "CloudPhone"
Cohesion: 0.07
Nodes (53): _at_or_after(), _bounds(), build_common_steps(), continue_number(), country(), create_account(), enter_otp(), focus_phone() (+45 more)

### Community 2 - "otp.py"
Cohesion: 0.11
Nodes (7): extract_otp(), _NoRedirect, read_otp(), _read_otp_in_browser(), timeout_ms(), wait_for_new_otp(), OtpTests

### Community 3 - "Window"
Cohesion: 0.05
Nodes (13): BulkRecord, lines(), parse_column(), parse_records(), _table_cells(), _url_from_cell(), validate_card(), _edge_light() (+5 more)

### Community 4 - "ToolError"
Cohesion: 0.09
Nodes (34): cloud_adb(), cloud_serials(), CloudPhone, open_amazon(), foreground(), package_path(), probe(), prop() (+26 more)

### Community 5 - "start_profile"
Cohesion: 0.13
Nodes (19): _activate_manager(), _create_profile_form(), _descendants(), inspect(), _invoke(), _main_window(), _one(), _profile_checkbox() (+11 more)

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
Cohesion: 0.36
Nodes (3): Hướng dẫn khi tiếp tục dự án, Bản đồ repository, Luồng q2 từ menu ba gạch

### Community 10 - "plans/README.md"
Cohesion: 0.20
Nodes (5): Giới hạn và lựa chọn cần xác minh, Kế hoạch sửa luồng mẻ Swarmote, Kết luận đã xác minh, Quy trình đích, Thứ tự thực hiện

### Community 11 - "Danh mục từng bước đã biết — 13/11/2026"
Cohesion: 0.07
Nodes (30): Chung b10 — Chuyển WhatsApp sang SMS, Chung b11a — Lấy và gõ OTP SMS, Chung b11b — Bấm Create your Amazon account, Chung b4 — Sign In từ menu, Chung b4a — Chạm ô SĐT, Chung b5 — Gõ số điện thoại, Chung b6 — Chọn United States +1, Chung b7 — Continue số điện thoại (+22 more)

### Community 12 - "settings.py"
Cohesion: 0.23
Nodes (7): save(), default_path(), AppSettings, load_settings(), save_settings(), settings_path(), SettingsTests

### Community 14 - "Biên bản kiểm tra thực tế — 2026-11-12"
Cohesion: 0.12
Nodes (17): Biên bản kiểm tra thực tế — 2026-11-12, Cập nhật luồng mẻ trước đó — 2026-11-13, Giao diện sáng, dễ đọc — 2026-11-13, Hướng Swarmote theo ảnh người dùng, Luồng tạo và mở song song — 2026-11-13, Menu ba gạch dạng danh sách — 2026-11-13, Mẻ 12 máy và tên cố định — 2026-11-13, Nút Làm lại / mẻ mới — 2026-11-13 (+9 more)

### Community 16 - "Ảnh hướng dẫn q1/q2 lưu cục bộ"
Cohesion: 0.10
Nodes (20): Menu chung ảnh 01 — Danh sách chữ, q1 ảnh 01 — Menu và ba thẻ, q1 ảnh 02 — Sign In cuối menu, q1 ảnh 03 — Nhập số điện thoại, q1 ảnh 04 — Chọn mã quốc gia, q1 ảnh 05 — Continue số điện thoại, q1 ảnh 06 — Tạo tài khoản mới, q1 ảnh 07 — Form tên (+12 more)

### Community 18 - "batch.py"
Cohesion: 0.40
Nodes (4): BatchItem, parse_proxy_line(), prepare_five(), BatchSafetyTests

### Community 19 - "ProxyConfig"
Cohesion: 0.27
Nodes (3): create_profile(), ProxyConfig, CreationWindowVisibilityTests

### Community 20 - "ProfilesNavigationTests"
Cohesion: 0.18
Nodes (6): _open_profiles(), visible_profile_names(), control(), ProfilesNavigationTests, descendants(), descendants()

### Community 21 - "profile_status"
Cohesion: 0.31
Nodes (6): _profile_row_status(), profile_status(), ProfileLookupError, ProfileNotFound, Thiết kế yêu cầu, Nút New Profile trên Swarmote — 13/11/2026

### Community 22 - "runner.py"
Cohesion: 0.12
Nodes (11): emit(), _prepare_phone(), run_batch(), fill_slots(), refresh_slots(), visible_lookup(), ProfileCreateNotSubmitted, ProfileManagerWindowError (+3 more)

### Community 23 - "time"
Cohesion: 0.14
Nodes (8): ready_for_home_menu(), install_amazon(), open_adb_shell(), _phone_window(), show_apps(), _wait_for(), FakeControl, InstallTests

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

### Community 33 - "Điều hướng hai dạng menu ba gạch"
Cohesion: 0.67
Nodes (3): Bằng chứng và phạm vi, Kiểm chứng, Điều hướng hai dạng menu ba gạch

### Community 34 - "Bàn giao trạng thái dự án — 13/11/2026"
Cohesion: 0.67
Nodes (3): Bàn giao trạng thái dự án — 13/11/2026, Mục tiêu và quy tắc đã chốt, Tài liệu chi tiết

### Community 36 - "003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật"
Cohesion: 0.25
Nodes (8): 003 — Một quy trình hai pha với trạng thái, dừng và tiếp tục thật, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Quy trình đích, Rủi ro và bảo trì, Điều kiện dừng

### Community 37 - "001 — Tách dữ liệu từng mẻ và đối chiếu số hàng"
Cohesion: 0.29
Nodes (7): 001 — Tách dữ liệu từng mẻ và đối chiếu số hàng, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Thiết kế yêu cầu, Điều kiện dừng

### Community 38 - "004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ"
Cohesion: 0.29
Nodes (7): 004 — Làm giao diện phản ánh sự thật và đo tốc độ mẻ, Các bước, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 39 - "002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ"
Cohesion: 0.33
Nodes (6): 002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ, Kiểm tra bắt buộc, Mục tiêu và bằng chứng, Phạm vi, Rủi ro và bảo trì, Điều kiện dừng

### Community 42 - "Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026"
Cohesion: 0.67
Nodes (3): Cách xử lý ảnh tiếp theo, Phần dùng chung đã được hướng dẫn, Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026

## Knowledge Gaps
- **1 isolated node(s):** `amazon-android-tool`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 261 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolError` connect `ToolError` to `core.py`, `CloudPhone`, `otp.py`, `Window`, `start_profile`, `RunnerTests`, `desktop.py`, `002 — Gán qN duy nhất và không dùng nhầm proxy của Profile cũ`, `settings.py`, `BatchDraft`, `test_runner.py`, `batch.py`, `ProxyConfig`, `ProfilesNavigationTests`, `profile_status`, `runner.py`, `time`?**
  _High betweenness centrality (0.437) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `ToolError` (e.g. with `_visible()` and `BatchDraft`) actually correct?**
  _`ToolError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `amazon-android-tool` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09081081081081081 - nodes in this community are weakly interconnected._
- **Why does `build_common_steps()` connect `CloudPhone` to `otp.py`, `ToolError`, `start_profile`, `desktop.py`, `Luồng q1 từ menu ba gạch tới nhập OTP`, `PROJECT_INDEX.md`, `Tiến độ hướng dẫn bằng ảnh — cập nhật 13/11/2026`, `Quy tắc tự động hóa sau menu ba gạch`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CloudPhone` (e.g. with `build_common_steps()` and `_ensure_menu()`) actually correct?**
  _`CloudPhone` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Should `CloudPhone` be split into smaller, more focused modules?**
  _Cohesion score 0.06651411136536994 - nodes in this community are weakly interconnected._
# Amazon Android Tool — Giai đoạn A/B

Xem [PROJECT_INDEX.md](PROJECT_INDEX.md) để đi tới toàn bộ mã, tài liệu từng bước, ảnh hướng dẫn, kiểm chứng và cây Graphify.

Giao diện desktop nhận tối đa 12 Profile Swarmote mỗi mẻ. Sau khi tạo và xác nhận một Profile, tool gửi Start ngay nếu mẻ còn chỗ máy Running, rồi tiếp tục tạo Profile kế tiếp trong khi điện thoại trước đang cài Amazon. Mỗi điện thoại được mở Amazon và đưa tới menu ba gạch. Các lệnh Android Emulator cục bộ nằm ở phần dưới.

Người dùng đã chọn hướng điện thoại đám mây Swarmote để tránh thời gian boot emulator cục bộ. Đã xác minh ADB và mở Amazon Shopping trên một Profile Swarmote thật; xem [VERIFICATION.md](VERIFICATION.md). Lệnh emulator ở phần dưới vẫn dành riêng cho Android Emulator cục bộ.

## Điện thoại đám mây Swarmote

Mở giao diện bằng cách nhấp đúp `Launch Swarmote Tool.pyw` trong File Explorer hoặc chạy `pythonw -m amazon_android.desktop` tại thư mục dự án. Cài dependencies một lần bằng `python -m pip install -e .`.

Trên máy Windows khác, cài các thư viện từ thư mục dự án bằng `python -m pip install -e .` với Python 3.11 trở lên. Lệnh này cài cả Playwright. Máy cần có Chrome hoặc Edge. Tool đọc OTP trực tiếp bằng Chrome ẩn và thử Edge ẩn nếu Chrome không mở hoặc không đọc được trang. Sau đó mở tool bằng `python -m amazon_android.desktop` để dùng đúng môi trường vừa cài. Nhập URL OTP riêng cho từng máy trong mẻ mới.

Trong mục **Dán nhanh theo danh sách** có hai ô. Dán 1–12 dòng proxy vào ô **Proxy**. Dán cả bảng `SĐT | Mật khẩu | Tên | Thẻ | URL OTP` vào ô **Thông tin Amazon** bằng Ctrl+V hoặc nút **Dán clipboard**. Bảng Markdown có hàng gạch phân cách, cột trống và link URL dạng `[nhãn](URL)` đều được nhận; thẻ có dạng `số thẻ|tháng|năm`. Tool lấy ba cột đầu, thẻ và URL OTP trên **cùng hàng**, kể cả khi bản sao có nhiều cột trống xen giữa. Hàng dữ liệu 1 vào Máy 1, hàng 12 vào Máy 12 và vẫn hiện đủ 12 hàng trước khi dán proxy. Mỗi URL OTP phải là `https://apifc.net/smsrecord?token=...` và mỗi máy dùng token riêng. Khi chạy mẻ, số proxy phải đủ cho số hàng Amazon. Bảng phân bổ hiện đuôi thẻ và URL để kiểm tra; chọn hàng để xem URL đầy đủ. Thẻ chỉ được giữ trong bộ nhớ phiên và chưa được dùng trong luồng tạo tài khoản hiện tại.

Chỉ dán proxy cũng có thể chạy; bảng thông tin Amazon là tùy chọn. Sau một mẻ, bấm **Làm lại / mẻ mới** để nhập bộ 3, 5, 4… máy tiếp theo. Nút này xóa dữ liệu nhập trên giao diện nhưng không xóa Profile Swarmote. Mỗi mẻ dùng cố định Máy 1 = q1 đến Máy 12 = q12; trước khi tạo, tool xác nhận tên đó chưa tồn tại trong Swarmote. Nếu tên đã có, tool báo lỗi thay vì đổi sang q13, q14… hoặc dùng nhầm proxy cũ. Khi tên chưa có, tool đưa cửa sổ Swarmote lên trước, bấm **New Profile** và xác nhận form tạo đã mở rồi mới điền tên/proxy. Dữ liệu mẻ đang chạy bị khóa để không lệch với job đã gửi.

Nếu lỗi được xác định trước khi gửi Create, bấm **Chạy** để thử lại mẻ hiện tại mà không phải dán lại dữ liệu. Trong bảng, bấm **Lỗi · bấm xem** để đọc nguyên nhân từng máy. Nếu Create đã được gửi nhưng kết quả chưa chắc chắn, tool dừng để tránh tạo trùng. Đóng và mở lại tool sẽ bắt đầu phiên mới; dữ liệu mẻ cũ không được khôi phục.

Trong **Settings**, chọn tối đa 1–12 máy Running của mẻ; mặc định là 1 và lựa chọn được lưu cho những phiên sau. Ví dụ với 12 proxy và giới hạn 2, q1 được tạo rồi gửi Start, q2 được tạo trong lúc q1 khởi động/cài Amazon và cũng được Start. q3–q12 tiếp tục được tạo nhưng đợi chỗ trống. Khi bạn Stop một máy về trạng thái Offline trong Swarmote, tool tự mở Profile đang đợi đầu tiên; chỉ đóng cửa sổ điện thoại mà Profile vẫn Running sẽ không giải phóng chỗ. Tool không tự đóng máy đã mở; nút Dừng ngắt hàng đợi sau bước hiện tại. Các bước cài Amazon chạy song song trên các cửa sổ điện thoại, còn thao tác tạo Profile dùng cửa sổ quản lý Swarmote theo thứ tự. Profile có sẵn ngoài mẻ không được Start lại bởi mẻ mới.

Giao diện giữ proxy, thông tin Amazon, thẻ, URL OTP và trạng thái mẻ trong bộ nhớ phiên, không ghi chúng vào SQLite/CSV. Bảng hiển thị trạng thái OTP ban đầu **Chưa yêu cầu mã**. Bộ đọc OTP tách sáu chữ số từ phản hồi `yes|Amazon: ... is your sign-in code.` sau khi bấm gửi SMS bằng trình duyệt ẩn. **q1 và q2** đã nối từ menu ba gạch tới OTP SMS và bấm `Create your Amazon account`; xem [Q1_FLOW.md](Q1_FLOW.md) và [Q2_FLOW.md](Q2_FLOW.md). Chỉ b1–b3 khác theo máy; b4–b11 dùng cùng một luồng nhưng mỗi máy có dữ liệu, OTP và đồng hồ riêng. q3–q12 vẫn dừng ở menu. q1 đã có báo cáo lỗi thật và mã đã sửa, q2 được báo đứng ở menu; các sửa mới chưa được kiểm tra lại trên máy thật.

Nếu menu ba gạch hiện dạng danh sách chữ, tool nhận diện từ cây UI của máy, bấm Home, chỉ xem 2–5 giây, trở lại menu và làm b4 Sign In. Menu dạng thẻ vẫn chạy b1–b3 riêng của q1/q2. Xem [MENU_ROUTING.md](MENU_ROUTING.md); nhánh này đã qua test mô phỏng, chưa thử máy thật.

Nếu Profile q1/q2 đã được lưu ở mốc `MENU_OPEN` từ lượt trước, nút Tiếp tục sẽ nối lại ADB serial của máy đang Running rồi chạy b1 riêng của máy đó. Khi không có hàng Amazon, serial ADB hoặc máy đang Offline, hàng máy sẽ hiện lý do thay vì chỉ ghi đã tới menu.

Để thử **q1 hoặc q2 đã có sẵn**: Start máy tương ứng trong Swarmote và mở Amazon tới menu ba gạch; trong tool dán 1–12 hàng `SĐT | Mật khẩu | Tên | Thẻ | URL OTP` (có thể có cột trống trong bản sao), chọn Máy 1 hoặc 2 rồi bấm **Thử qN từ menu ba gạch**. Các hàng khác vẫn hiển thị và giữ nguyên dữ liệu; q1/q2 có thể chạy độc lập. Tool xác nhận đúng Profile đang Running và menu trên ADB serial của máy đó trước khi bắt đầu. Nút **Chạy máy trong mẻ** dành cho mẻ tạo Profile mới. Nếu bước nào lỗi, sửa trực tiếp trên máy đó rồi bấm **Tiếp tục** ở đúng hàng. Nút **Làm lại / mẻ mới** xóa dữ liệu và tiến độ trong tool, không xóa Profile Swarmote.

Khung điều phối sau menu có đồng hồ lượt riêng và nút **Tiếp tục** cho máy lỗi. Quy tắc gõ từng ký tự, dừng tại màn hình lỗi và chu kỳ thời hạn 3–4–5–4 phút được ghi trong [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md). Kết quả sau nút Create chưa được xác nhận, nên trạng thái hoàn tất chỉ có nghĩa đã xong các bước được hướng dẫn.

Swarmote có "Batch Create" và "Batch Import" trên form tạo Profile. Bản tool này chưa dùng chúng: Batch Create yêu cầu proxy đã lưu trong Swarmote, còn kết quả/định dạng của Batch Import chưa được xác minh. Pha tạo Profile vẫn đi qua "Single Create" để Test proxy và xác nhận từng máy.

Bản Swarmote đang cài có ADB đi qua đường hầm SSH cục bộ khi mở `Terminal > ADB Shell` trong một Profile đang chạy. Công cụ dùng ADB mà Swarmote đóng gói, không đọc khóa SSH hoặc gọi API riêng của Swarmote.

```powershell
python -m amazon_android.cli cloud-scan
python -m amazon_android.cli cloud-open-amazon 127.0.0.1:PORT
python -m amazon_android.cli swarmote-inspect
python -m amazon_android.cli swarmote-create-profile --name "Amazon Test" --host proxy.example --port 12345 --username USER
python -m amazon_android.cli swarmote-status "Amazon Test"
python -m amazon_android.cli swarmote-start "Amazon Test"
python -m amazon_android.cli swarmote-adb-shell "Amazon Test"
python -m amazon_android.cli swarmote-install-amazon "Amazon Test"
python -m amazon_android.cli swarmote-ready "Amazon Test"
```

`cloud-scan` chỉ báo thiết bị ADB thật khi cổng local thuộc tiến trình Swarmote và kiểm tra package Amazon Shopping bằng Android Package Manager. `cloud-open-amazon` mở ứng dụng và xác nhận tiến trình/cửa sổ trước. Nếu ADB chưa có đường hầm, lệnh báo danh sách trống; không báo thành công dựa trên ảnh. Nguồn APK từ App Center Swarmote vẫn chưa xác minh là Google Play, dù Android có báo tên installer.

`swarmote-inspect` chỉ đọc cây UI Automation, không chiếm chuột. `swarmote-create-profile` điền proxy SOCKS5 trực tiếp trong biểu mẫu tạo một Profile Swarmote, hỏi mật khẩu proxy trong terminal. Nó dùng UIA Value/Invoke/Selection patterns, không gửi chuột hay bàn phím Windows. Nếu lệnh báo chưa xác định kết quả, phải chạy `swarmote-status` trước khi thử lại để tránh tạo trùng. `swarmote-ready` khởi chạy một Profile có sẵn, cài Amazon từ App Store Swarmote nếu thiếu, xác minh package qua ADB và đi tới ô nhập email/số điện thoại của Amazon. Chưa có lệnh gửi đăng ký tài khoản.

Lệnh CLI `swarmote-batch-five` là đường thử nghiệm cũ, chỉ nhận đúng 5 dòng và dừng ở màn đăng nhập Amazon. Nó chưa dùng registry qN hoặc trạng thái tiếp tục của giao diện desktop; hãy dùng giao diện cho các mẻ 1–12 máy. Lệnh CLI chưa được kiểm thử end-to-end trên 5 Profile thật.

ADB của Android SDK dùng server port 5038 để không khởi động lại ADB 36 của Swarmote trên cổng mặc định 5037.

## Yêu cầu

- Windows 10/11, Python 3.11+ và Java.
- Android SDK Command-line Tools, Platform Tools, Emulator và Google Play system image Android 35 x86_64.
- Google Play có thể yêu cầu người dùng đăng nhập và tự bấm cài Amazon Shopping.
- Nên có ít nhất 2.3 GB RAM trống cho thiết bị đầu và 3 GB trống trước khi bật thiết bị thứ hai. Chương trình từ chối khởi động nếu thiếu.

## Sử dụng

Từ PowerShell tại thư mục dự án:

```powershell
python -m amazon_android.cli doctor
python -m amazon_android.cli setup-sdk
python -m amazon_android.cli create-avd 1
python -m amazon_android.cli start 1
python -m amazon_android.cli status 1
python -m amazon_android.cli check-play 1
python -m amazon_android.cli install-amazon 1
python -m amazon_android.cli open-amazon 1
python -m amazon_android.cli stop 1
```

`setup-sdk` chỉ tải từ kho chính thức Google, kiểm checksum và yêu cầu xác nhận trong terminal trước khi tải/cài. Người dùng tự chấp nhận giấy phép SDK. Có thể cài SDK bằng Android Studio theo hướng dẫn chính thức rồi chạy `doctor`.

Thiết bị thứ hai: `create-avd 2`, sau đó `start 2 --allow-second`. Lệnh `devices`, `logs 1`, `test-report` cho thấy trạng thái và bằng chứng. Trạng thái SQLite nằm tại `%LOCALAPPDATA%\AmazonAndroidTool\state.sqlite3`. Không lưu mật khẩu hay OTP.

Nếu ADB bị treo, `emergency-stop 1` chỉ dừng tiến trình emulator khớp cả tên AVD và cổng đã cấu hình. `status 1` hiển thị CPU toàn máy, RAM trống và RAM tiến trình emulator.

Chỉ khi người dùng chủ động chấp nhận rủi ro thiếu RAM, `start 1 --force-low-memory` mới bỏ qua ngưỡng bộ nhớ cho lần chạy đó. Nhật ký ghi lại giá trị RAM lúc bắt đầu. Mặc định vẫn chặn khởi động khi thiếu RAM.

Lệnh `install-amazon` không tự xác nhận cài đặt trên Google Play. Nó chỉ báo thành công sau khi Android Package Manager trả về package và nguồn cài `com.android.vending`. Nếu bị hạn chế khu vực/tương thích, hết thời gian chờ sẽ báo lỗi. Lệnh `open-amazon` xác nhận riêng ứng dụng còn tiến trình và có cửa sổ được focus.

## Trạng thái nghiệm thu

Chạy `python -m amazon_android.cli test-report` trên máy đích. Chỉ TEST 01/02 được đánh giá tức thời từ ADB. Các phép thử khác giữ `NOT TESTED` cho tới khi có quy trình thực nghiệm riêng trên Android/Amazon thật.

# Bàn giao trạng thái dự án — 13/11/2026

## Mục tiêu và quy tắc đã chốt

Tool desktop CustomTkinter điều khiển Swarmote/Amazon Shopping cho tối đa 12 máy. Mỗi hàng Amazon chứa SĐT, mật khẩu, tên, thẻ và URL OTP riêng; hàng n gắn Máy n. Bảng Markdown có cột trống, hàng gạch phân cách, thẻ `số|tháng|năm` viết `\|`, và link URL dạng `[nhãn](URL)` phải được đọc đúng. Bảng chỉ hiện đuôi thẻ; dữ liệu giữ trong bộ nhớ phiên. Thẻ chưa được dùng trong b1–b11.

Từ menu ba gạch, chỉ b1–b3 khác nhau theo máy. b4 Sign In đến b11 nhập OTP SMS rồi bấm Create dùng chung. Người dùng sẽ hướng dẫn b1–b3 của từng máy; hiện đã có q1 và q2. Mỗi máy có ADB serial, SĐT, URL OTP, mã, trạng thái gửi, đồng hồ và điểm dừng/tiếp tục riêng. Gõ từng ký tự, không dán vào Android. Nếu lỗi, dừng ngay tại bước đó; người dùng sửa trên máy rồi bấm Tiếp tục. Chu kỳ thời hạn mỗi máy: 3, 4, 5, 4 phút rồi lặp lại; tính lại khi Tiếp tục. Đồng hồ kết thúc khi OTP SMS đã nhập đúng, sau đó bấm Create.

Menu ba gạch có thêm biến thể dạng danh sách: trên các máy đã nối sau menu, đọc cây UI hiện tại; nếu thấy danh sách chữ, bấm Home, chỉ xem/chờ 2–5 giây, quay lại menu rồi làm b4 Sign In. Dạng thẻ vẫn chạy b1–b3 riêng. Không cuộn Home và không dùng tọa độ ảnh. Xem [MENU_ROUTING.md](MENU_ROUTING.md) cùng ảnh trong `flow_images/shared/`. q3–q12 vẫn chưa được bật sau menu.

## Mã hiện có

- `amazon_android/bulk_input.py`, `batch_state.py`, `desktop.py`, `runner.py`: ánh xạ hàng, dữ liệu thẻ/OTP, UI 12 máy; khi gắn q1, 12 hàng vẫn hiện.
- `amazon_android/otp.py`: xác thực URL APIFC, tách đúng 6 số từ phản hồi Amazon và đọc sau khi gửi SMS; Chrome và Edge ẩn dùng để đọc OTP. APIFC không cung cấp dấu thời gian để chứng minh mã là mới khi URL đã có mã cũ.
- `amazon_android/post_menu.py`: phiên riêng từng máy, thời hạn, dừng/tiếp tục cùng bước, gõ từng ký tự.
- `amazon_android/account_flow.py`: nhận diện UI Android, phân loại menu dạng thẻ/danh sách, dùng `route_list_menu` và `visit_home`, cùng `build_common_steps` cho b4–b11. `amazon_android/q1_flow.py`: b1 Gifting, b2 Pets, b3 Fashion and Beauty. `amazon_android/q2_flow.py`: b1 tab Home và xem 2–5 giây, b2 tab Browse menu, b3 Pets. `amazon_android/post_menu.py` chuyển thẳng tới b4 khi menu dạng danh sách. `amazon_android/desktop.py` gắn profile từ menu theo máy được chọn. Không dùng tọa độ ảnh. q1 và q2 được nối; q3–q12 dừng ở menu.
- `amazon_android/swarmote_desktop.py`: khi tạo profile, kiểm tra tên trùng; nếu tên vắng trên danh sách một trang thì không gõ vào ô lọc. Đưa cửa sổ quản lý lên trước để bấm New Profile, xác nhận form trước khi điền, sau đó Test Proxy và Create.
- `Launch Swarmote Tool.pyw` gọi `amazon_android/launcher.py` để mở desktop. Graphify không phân tích trực tiếp `.pyw`; xem [SOURCE_INDEX.md](SOURCE_INDEX.md) cho các file bị bỏ qua.

## Trạng thái kiểm chứng và giới hạn

- B9 Continue và b11 Create dùng chữ, mô tả và quan hệ điều khiển từ cây Android trước. Nếu vẫn mơ hồ, chụp trực tiếp màn Android vào bộ nhớ và tìm nút vàng rộng bên dưới ô đã xác nhận. Nếu có nhiều vùng vàng, chỉ chọn khi vị trí nhãn đúng trong cây UI xác định duy nhất một vùng. B11 kiểm tra SĐT trước nhánh ảnh và đối chiếu OTP nếu phiên đã có mã. Test mô phỏng với vùng vàng và màn SMS. Chưa kiểm tra trên Swarmote thật vì phiên này không tìm thấy ADB.

- Luồng dùng chung tự đọc lại khi ADB hết hạn, lấy file thất bại hoặc trả XML chưa hợp lệ. Trong lúc chờ màn kế tiếp, các lỗi đọc tạm thời được thử lại theo thời hạn. Nếu cú bấm chuyển màn hết hạn ở ADB, kiểm tra màn sau cú bấm trước khi quyết định bước tiếp theo. Gửi SMS và Create vẫn giữ dấu đã bấm để tránh gửi lặp. Khi không thể xác nhận, thông báo ghi màn đọc được và màn cần thấy, không kèm dữ liệu tài khoản. 148 bài test đã qua, gồm cú bấm SMS bị timeout nhưng đã chuyển màn và XML lỗi được đọc lại. Chưa xác minh trên Swarmote thật.

- B11 thử Chrome ẩn, Edge ẩn rồi tự mở một cửa sổ Chrome riêng nếu chưa đọc được mã. Tool dành một phần thời hạn đọc OTP cho cửa sổ này, chờ người dùng xử lý xác minh nếu trang yêu cầu và đóng cửa sổ sau khi lấy mã, hết hạn hoặc dừng. Nếu vẫn lỗi, Tiếp tục giữ phương án nhập tay. Chưa xác minh với APIFC thật.

- B11a chạm ô OTP ngay khi nhận ra màn SMS và xác nhận đúng SĐT. Khi nhận được mã, b11 đọc lại màn, xác nhận đúng SĐT và kiểm tra focus trước khi gõ. Test mô phỏng bao gồm trường hợp nguồn mã lỗi sau khi ô đã được chạm và ô mất focus trong lúc chờ mã. 145 bài test đạt. Ảnh q1 báo đúng chuỗi lỗi 403 của bộ đọc HTTP cũ, đã bỏ khỏi luồng mặc định tại `07ab6d1`. Chưa đọc được q1 thật vì phiên kiểm tra không thấy ADB.

- B9 gặp nhiều Continue khi bàn phím mở. Bộ chọn nhận cả text và content-desc, giữ node nút gốc. Nếu vẫn chưa chọn được, kiểm tra Android có bàn phím đang hiện, đóng bàn phím một lần, đọc lại form, xác nhận SĐT và tên rồi mới bấm Continue. Chưa đối chiếu cây UI của q1 thật vì không thấy ADB trong phiên kiểm tra.

- Ảnh q1 mới cho thấy form tạo tài khoản đã hiện dù b8 báo chưa nhận diện được màn. Bộ nhận diện chung đọc cả `text` và `content-desc`, chấp nhận tiêu đề biến thể và dùng nhãn tên hoặc tiêu đề cùng Mobile number, Continue và một ô nhập hiện hữu. Khi b8 đọc được form đã mở, chuyển sang b9 mà không bấm lại. Mô phỏng đã kiểm tra các biến thể và trường hợp mơ hồ. Chưa đọc được cây UI q1 thật vì không thấy ADB Swarmote.

- Danh sách quốc gia dài. Sau cú vuốt nhanh rồi nhả, nếu màn vẫn hiện các nước nhóm A–S, b6 tiếp tục dùng cú vuốt mạnh. Gần nhóm T/U thì cuộn có kiểm soát và cuộn ngược nếu vượt qua mục Mỹ.

- Ảnh b6 mới cho thấy danh sách đã tới United States nhưng lệnh ADB hết hạn sau 6 giây. B6 dùng lại cây UI đã đọc để chọn mục đang hiện hoặc quyết định cú vuốt đầu. Nếu thao tác đọc cây UI hết hạn ở ADB, thử đọc lại một lần trong thời hạn của máy, không lặp cú vuốt hoặc bấm. Chưa có số đo trên máy thật.

- Tăng lực vuốt đầu ở b6 bằng thao tác 65 ms qua 92% vùng danh sách khi cây UI cung cấp vùng cuộn. Tool đọc lại để xác nhận đúng United States +1 và cuộn ngược ngắn nếu vượt qua mục Mỹ. Giảm khoảng nghỉ cuộn thường và kiểm tra một số lần chuyển màn. Chưa đo quãng vuốt hoặc thời gian trên máy Swarmote thật.

- Trình duyệt có thể khởi động trong lúc chờ SMS. Chỉ điều hướng tới URL của máy khi đủ 4 giây từ lúc bấm gửi và màn SMS đã được nhận diện. Chrome ẩn là mặc định, Edge ẩn dự phòng khi Chrome không mở hoặc không đọc được trang.

- B11 mặc định đọc OTP qua Chrome ẩn và thử Edge ẩn nếu Chrome không mở hoặc không đọc được trang. Máy đích cần cài Chrome hoặc Edge và Playwright qua dependencies. Đã chạy trình duyệt ẩn thật với máy chủ thử nghiệm cục bộ, nhận phản hồi chờ rồi tải lại và tách được 6 số. Chưa xác nhận với URL APIFC của lượt SMS thật. Nếu trình duyệt ẩn không đọc được, dùng phương án mở trình duyệt thường tại Tiếp tục.

- Ở b11, người dùng xác nhận cùng URL có SMS đúng mẫu trong trình duyệt khi tool báo HTTP 403. Bấm Tiếp tục ở máy lỗi để mở URL đúng hàng và dán phản hồi SMS hoặc 6 số vào tool. Tool xác nhận lại số điện thoại trên màn SMS trước khi điền. OTP chỉ giữ trong bộ nhớ. Bộ đọc phân biệt phản hồi có header `cf-mitigated: challenge` với HTTP 403 thông thường. Chưa xác định nguyên nhân 403 trên máy người dùng hoặc kiểm chứng tự đọc URL thật.

- Ảnh q1 mới báo b9 chưa xác nhận được nội dung ô tên dù tên đã hiện. Luồng chung đọc lại tối đa ba lần sau khi gõ, không gõ lặp và chỉ bấm Continue khi nội dung khớp tên của máy. Kiểm tra mô phỏng giá trị tên cập nhật trễ. Chưa xác nhận trên Swarmote thật.

- Sau ảnh q1 dừng tại b4 dù form đã xuất hiện, luồng chung tách b4a chạm ô SĐT thành bước riêng giữa Sign In và gõ số. B4a chờ form, chạm ô và b5 kiểm tra lại focus trước khi gõ. Form cũng được nhận khi có nhãn SĐT, Continue và một ô nhập hiện hữu dù cây UI thiếu tiêu đề. Giảm khoảng nghỉ khi kiểm tra màn và cuộn thường. Chưa kiểm chứng trên Swarmote thật.

- Luồng chung giữ quan hệ cha con trong cây UI Android. Bộ chọn nút quy các nhãn lặp về điều khiển cha có thể bấm trước khi so sánh vùng bấm. Áp dụng cho Sign In, Continue, Proceed to create an account, Send code by SMS và Create your Amazon account. Đã thêm kiểm tra với cây XML mô phỏng, chưa có ADB Swarmote để đối chiếu cây UI thật.

- Máy 2 báo b9 còn nhiều mục Continue sau khi tên đã điền. Bộ chọn chung ưu tiên nút duy nhất nằm dưới và phủ gần hết chiều ngang ô tên khi còn nhiều vùng bấm. Nếu có hai vùng cùng thỏa thì giữ điểm dừng. Kiểm tra mô phỏng, chưa có cây UI của màn lỗi trên máy thật.

- B4–b5 dùng chung nhận diện form `Sign in or create account` có nút Continue và một ô nhập hiện hữu ngay cả khi cây UI thiếu nhãn SĐT. B4 chạm vào ô. B5 kiểm tra lại focus nếu ô chưa được chọn, thử chạm lại trước khi gõ và báo rõ nếu vẫn lỗi. Dùng cho q1, q2 và các máy nối sau. Chưa thử bản sửa trên Swarmote thật.

- B6 dùng một cú vuốt dài và nhanh hướng về cuối danh sách quốc gia, sau đó đọc lại để tìm `United States +1`. Nếu thấy các mục sau Mỹ mà chưa thấy mục cần chọn, tool vuốt ngược ngắn để tìm lại. Áp dụng cho luồng chung. Chưa đo khoảng cuộn thực tế trên Swarmote.

- Luồng SMS dùng chung đợi đủ 4 giây tính từ lúc bấm gửi rồi mới đọc URL OTP. Thời gian chuyển màn được tính vào 4 giây. Nếu người dùng đã gửi tay, tính từ lúc tool nhận ra màn SMS lần đầu. Mỗi lần thử gọi lại URL với yêu cầu kiểm tra lại bộ nhớ đệm. 133 bài kiểm tra đã qua, gồm kiểm tra thời gian chờ còn lại. Chưa xác minh với URL thật.

- Báo cáo mới trên q1 cho thấy b6 cuộn chậm, b9 báo nhiều Continue và b11 nhận HTTP 403 dù Amazon đã xác nhận gửi SMS. Sửa trong `build_common_steps` cho mọi máy. B6 vuốt dài trong vùng danh sách khi nhận diện được và chỉ bấm đúng `United States +1`. B9 gộp các vùng Continue lồng nhau và dùng lại cây UI đã xác nhận ô tên. Giảm khoảng chờ giữa các lần kiểm tra màn. B11 báo rõ lỗi URL OTP và vẫn cho tiếp tục từ mã nhập tay. 133 bài kiểm tra đã qua. `cloud-scan` chưa thấy ADB nên chưa đo tốc độ hay kiểm chứng cây UI thật.

- 131 bài unittest đã qua, gồm nhánh menu danh sách, b4 chọn Sign In khi cây UI có nhãn lặp và dừng khi vẫn mơ hồ, b6 cuộn qua mục US ẩn và b10 bấm SMS trước mọi lần đọc URL; đồng thời các kiểm tra trước đó cho luồng chung b4–b11 và nối lại q2 từ mốc menu đã lưu. Nhánh `MENU_OPEN` nối lại ADB serial trước khi báo q2 đã tới menu; tool báo rõ nếu thiếu hàng Amazon hoặc serial. Test cửa sổ nhận 12 hàng, giữ đúng thẻ/URL theo máy và hiện nút thử q2. Đã thử trực tiếp mở form New Profile và đóng bằng Cancel, không gửi Create. Chưa thử lại trên máy thật.
- Lúc kiểm tra ngày 13/11/2026, Swarmote có q1, q2, q3. Người dùng đã thử q1 và gửi năm ảnh mới: form SĐT cùng lỗi b6/b9/b10; sau đó xác nhận q1 hiện ở form SĐT. Người dùng báo q2 tới menu ba gạch rồi dừng, tool chỉ ghi đã tới menu mà không báo lỗi. Mã có nhánh mốc `MENU_OPEN` cũ không nối lại ADB và các điều kiện âm thầm dừng; đã sửa và test mô phỏng, chưa thử lại q2 thật. Chưa xác minh URL OTP sau gửi hoặc màn sau Create. Lệnh `cloud-scan` trong môi trường phiên này không tìm thấy ADB Swarmote/Android SDK nên không thể tự đọc máy trực tiếp.
- Người dùng gửi tiếp sáu ảnh q1: b6 lỗi khi danh sách quốc gia vẫn ở chữ A, b9 báo nhiều Continue dù form có một nút nhìn thấy, b10 báo HTTP 403 khi vẫn ở màn WhatsApp và nút SMS chưa được bấm. Mã nguồn hiện tại chọn nút b9 theo khả năng bấm/vị trí dưới ô tên, chỉ đọc URL tại b11 sau khi bấm SMS; đã bổ sung lọc bounds cho ô mở mã quốc gia và test hồi quy b6/b10. Các thông báo trên màn phù hợp với tiến trình tool chưa nạp mã mới, nhưng chưa xác minh được tiến trình đó. Không đóng hoặc đặt lại phiên vì hàng nhập chỉ ở RAM. Sáu ảnh mới ở `flow_images/q1/latest_errors/` và [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).
- Người dùng gửi ảnh q1 dừng tại b4 dù menu danh sách hiện Sign In ngay dưới Customer Service. Bộ chọn cũ dùng `_unique` nên dừng khi cây UI có nhãn lặp. Mã mới ưu tiên Sign In có thể bấm, rồi giới hạn theo mốc Customer Service; nếu vẫn nhiều ứng viên thì dừng. Có thể bấm Sign In thủ công rồi Tiếp tục trên phiên cũ; b4 nhận form SĐT hiện tại. Chưa có dump ADB q1 thật, chưa xác minh sửa trên máy. Ảnh lưu `flow_images/q1/15_b4_list_sign_in_ambiguous.png`.
- Tên q1–q12 được cố định cho các slot; tool dừng nếu tên đã có để tránh trùng. Người dùng chưa quyết định sẽ dùng lại q1–q3 hay tạo profile mới tên khác. Đây là câu hỏi cần giải trước khi đổi chính sách tên.
- `graphify.exe` trên máy hiện báo lỗi `uv trampoline failed to canonicalize script path`; `python -m graphify` hoạt động.
- Graphify đã tạo `graphify-out/graph.json`, `graph.html`, `GRAPH_TREE.html` và `GRAPH_REPORT.md`. Xem [GRAPH_AUDIT.md](GRAPH_AUDIT.md) để biết chính xác phần đã lập chỉ mục và phần còn thiếu. Graph chứa AST mã nguồn cùng file/tiêu đề/liên kết tài liệu sau `python -m graphify update .`. Xem [ASSET_INDEX.md](ASSET_INDEX.md) cho sáu PNG giao diện (năm ảnh lịch sử đã gom vào `assets/ui_history/`) và [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md) cho hai mươi ba ảnh q1/q2 cùng một ảnh menu chung trong `flow_images/`. Các ảnh này được đưa lên repository công khai theo yêu cầu bàn giao; có thể hiển thị SĐT/OTP trên ảnh gốc. Nội dung pixel chưa được trích xuất ngữ nghĩa vì không có LLM API key hoặc Ollama; phải mở ảnh gốc khi cần. Các cạnh INFERRED của Graphify có thể sai, cần đối chiếu mã. Xem số node/cạnh hiện tại trong `GRAPH_REPORT.md` để tránh dùng số cũ.

## Tài liệu chi tiết

**Đây là quy trình đang được hướng dẫn từng ảnh, chưa phải quy trình đầy đủ.** Đọc [STEP_INVENTORY.md](STEP_INVENTORY.md) để thấy từng mốc P01–P08a, q1/q2 b1–b3, b4–b11 và các mốc chưa có ảnh. Đọc [FLOW_PROGRESS.md](FLOW_PROGRESS.md) để biết mức kiểm chứng. Sau đó đọc [POST_MENU_REQUIREMENTS.md](POST_MENU_REQUIREMENTS.md), [MENU_ROUTING.md](MENU_ROUTING.md), [Q1_FLOW.md](Q1_FLOW.md), [Q2_FLOW.md](Q2_FLOW.md), [OTP_DESIGN.md](OTP_DESIGN.md), [VERIFICATION.md](VERIFICATION.md), [README.md](README.md). Không suy ra q3–q12 đã được tự động hóa chỉ vì b4–b11 dùng chung.

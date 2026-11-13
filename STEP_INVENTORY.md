# Danh mục từng bước đã biết — 13/11/2026

Tài liệu này là bản đồ từng mốc để phiên sau không coi ảnh chưa gửi là bước đã hoàn thành. Ảnh gốc q1/q2 đã lưu và ánh xạ tại [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md); mở ảnh đó khi cần xem UI. `Đã nối mã` khác với `đã chạy thật`. Các bước được ghi từ hướng dẫn người dùng và mã hiện tại; không suy ra màn chưa có ảnh. Dữ liệu nhạy cảm không ghi vào file này.

## P01 — Dán và gán hàng dữ liệu

Dán 1–12 hàng `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`. Cột trống, hàng gạch Markdown, thẻ có `\|` và link URL Markdown được nhận. Hàng n gắn Máy n, không tráo SĐT/URL. Thẻ và mật khẩu chỉ gắn dữ liệu, chưa dùng trong ảnh b1–b11. **Đã nối mã, đã test mô phỏng.**

## P02 — Kiểm tra proxy và tên Profile

Mỗi máy cần proxy tương ứng khi tạo profile mới. Tool kiểm tra tên qN đã tồn tại hay chưa; không tạo trùng hoặc tự đổi tên. Trên danh sách một trang, không gõ qN vào ô lọc chỉ để xác định vắng. **Đã nối mã; q1–q3 được thấy có sẵn ngày 13/11/2026. Chính sách dùng lại hay đặt tên mới còn chờ người dùng.**

## P03 — Mở form New Profile

Đưa cửa sổ quản lý Swarmote lên trước, bấm **New Profile**, xác nhận form có Create, Single Create, Profile Name, ip/Host trước khi điền. Nếu form không mở, dừng; không điền vào ô tìm kiếm Profile Name. **Đã thử trực tiếp mở form rồi Cancel; chưa gửi Create trong thử nghiệm mới.**

## P04 — Điền Single Create và Custom proxy

Chọn Single Create và Custom; điền tên Profile, host, port, tài khoản và mật khẩu proxy bằng UIA vào form đã xác nhận. **Đã nối mã; chưa kiểm thử lại toàn bộ sau sửa New Profile.**

## P05 — Test Proxy rồi Create

Bấm Test Proxy; chỉ khi hiện Test Passed mới bấm Create. Sau Create, xác nhận đúng tên Profile và Device ID; nếu kết quả không chắc chắn, dừng để tránh tạo trùng. **Đã nối mã; chưa gửi Create trong phép thử gần nhất.**

## P06 — Start điện thoại và chờ slot

Tool gửi Start cho Profile đã xác nhận, tuân giới hạn số máy Running, và đợi slot nếu đủ máy. Mỗi máy có Device ID riêng. **Đã nối mã; các trường hợp chính có test mô phỏng.**

## P07 — Mở Apps, tìm z và cài Amazon

Trên đúng cửa sổ máy, mở Apps/App Store, tìm `z`, cài Amazon Shopping và xác nhận package qua ADB. Nếu app đã cài thì tiếp tục, không cài lặp. **Đã nối mã; một số máy cũ từng được kiểm tra thật, không suy ra máy mới.**

## P08 — Mở Amazon tới menu ba gạch

Mở Amazon, xử lý màn trước đăng nhập nếu có, bấm Browse menu Tab và xác nhận `Shop by category`/menu. Đây là điểm nối luồng riêng từng máy. Nếu registry đã ghi `MENU_OPEN` từ lượt trước, phải nối lại ADB serial của đúng máy trước khi phát sự kiện để chạy b1. Nếu thiếu hàng Amazon hoặc serial, báo rõ ở hàng máy; nếu Offline, nhắc Start rồi Tiếp tục. **Đã sửa mã và test mô phỏng cho q1/q2; q2 chưa xác minh lại thật sau báo cáo đứng ở menu.**

## P08a — Nhận diện biến thể menu dạng danh sách

Sau P08, đọc cây UI Android trực tiếp của đúng máy. Nếu menu có các thẻ danh mục như Gifting/Pets/Fashion and Beauty, giữ b1–b3 riêng của q1 hoặc q2. Nếu menu là danh sách chữ như ảnh mới (`Shop by Category`, `Books`, `Electronics`, `Home services`, `See all`, `Customer Service`, `Sign In`), bấm tab Home, **chỉ xem/chờ 2–5 giây, không cuộn**, quay lại menu và chuyển thẳng sang b4 Sign In. Thời gian này nằm trong đồng hồ lượt của máy. Nếu cấu trúc chưa xác định được hoặc thiếu nút Home/Sign In, dừng tại màn hiện tại và cho Tiếp tục; không đoán tọa độ ảnh. Nhánh này dùng chung cho các máy đã được nối sau menu; không tự bật q3–q12. **Đã nối mã và test mô phỏng; chưa thử máy thật.** Xem [MENU_ROUTING.md](MENU_ROUTING.md).

## Q1 b1 — Bấm Gifting

Từ menu, tìm thẻ Gifting trong cây UI hiện tại, cuộn khi cần và bấm. Khi mở trang danh mục, quay lại menu trước bước kế. **Đã nối mã theo ảnh; chưa thử thật q1.**

## Q1 b2 — Bấm Pets

Tìm thẻ Pets trên menu, bấm và quay lại menu khi cần. **Đã nối mã theo ảnh; chưa thử thật q1.**

## Q1 b3 — Bấm Fashion and Beauty

Tìm thẻ Fashion and Beauty trên menu, bấm. Bước chung b4 sẽ đưa về menu trước Sign In. **Đã nối mã theo ảnh; chưa thử thật q1.**

## Q2 b1 — Bấm Home và xem 2–5 giây

Từ menu, bấm Home Tab ở thanh dưới. Xác nhận trang chủ bằng `Sign in for the best experience` hoặc Home Tab được chọn; chờ một khoảng chọn trong 2, 3, 4, 5 giây. **Đã nối mã theo ảnh; chưa thử thật q2.**

## Q2 b2 — Bấm menu ba gạch

Từ trang chủ, bấm Browse menu Tab và xác nhận menu. **Đã nối mã theo ảnh; chưa thử thật q2.**

## Q2 b3 — Bấm Pets

Tìm Pets trên menu hiện tại, cuộn khi cần và bấm. Bước chung b4 đưa về menu trước Sign In. **Đã nối mã theo ảnh; chưa thử thật q2.**

## Chung b4 — Sign In từ menu

Tìm hàng Sign In ở cuối menu bằng chữ trong UI, cuộn khi cần, bấm và xác nhận form `Sign in or create account`. **Chạm vào ô SĐT để lấy focus** trước b5; nếu đã ở form này khi bấm Tiếp tục thì vẫn chạm vào ô. **Đã sửa mã chung cho q1/q2 sau ảnh q1 ở form SĐT; chưa xác minh lại trên máy thật.**

Ảnh q1 mới cho thấy b4 dừng vì cây UI có nhiều nhãn `Sign In` dù hàng Sign In hiện trong menu danh sách dưới Customer Service. Bộ chọn chung giờ ưu tiên node có thể bấm; khi nhãn vẫn lặp, dùng Customer Service đang hiện làm mốc và chỉ chọn một Sign In dưới mốc. Nếu vẫn nhiều ứng viên thì dừng để người dùng sửa và bấm Tiếp tục. Trong phiên tool cũ, có thể bấm Sign In thủ công rồi Tiếp tục từ form SĐT. **131 test mô phỏng đạt; chưa xác minh trên q1 thật.**

## Chung b4a — Chạm ô SĐT

Sau Sign In, chờ form nhập SĐT rồi chạm vào ô đang hiện. B5 thử chạm lại nếu Android vẫn báo ô chưa có focus. Đây là bước dùng chung và lỗi chờ form sẽ hiện ở b4a.

## Chung b5 — Gõ số điện thoại

Gõ nguyên chuỗi SĐT của đúng hàng từng ký tự vào ô `Enter mobile number or email`, rồi đọc lại. Không dán clipboard. **Đã nối mã; chưa thử thật.**

## Chung b6 — Chọn United States +1

B6 vuốt dài trong vùng danh sách nếu cây UI cung cấp đúng một vùng cuộn hợp lệ. Sau mỗi lần vuốt, đọc cây UI và tìm đúng nhãn `United States +1`. Chỉ bấm khi mục có vùng hợp lệ. Chưa đo tốc độ trên Swarmote thật.

Sau khi gõ số, mở Country/region code, cuộn tới gần cuối tìm United States +1, chọn và đọc lại số/mã quốc gia. Không bấm mục US ẩn có vùng `[0,0][0,0]`; tiếp tục cuộn đến mục đang hiển thị và có vùng bấm hợp lệ. Ảnh b6 ban đầu có tiêu đề cửa sổ q6, chỉ là tham chiếu UI. q1 đã báo lỗi vùng bấm b6; **đã sửa mã chung, chưa xác minh lại trên máy thật.**

Sáu ảnh q1 mới ngày 13/11 cho thấy dropdown vẫn ở chữ A khi báo lỗi. Mã hiện tại lọc cả ô mở mã quốc gia bị ẩn, và chỉ bấm mục US +1 có bounds hợp lệ sau khi cuộn. Có test hồi quy cho trạng thái danh sách đang ở đầu. Chưa xác nhận phiên tool trên màn đã nạp mã này.

## Chung b7 — Continue số điện thoại

Chỉ bấm Continue khi form và số US +1 khớp hàng của máy. Nếu chuyển sang màn đăng nhập cũ hoặc màn lạ, dừng. **Đã nối mã; chưa thử thật.**

## Chung b8 — Proceed to create an account

Xác nhận màn `Looks like you are new to Amazon` và SĐT, rồi bấm `Proceed to create an account`. **Đã nối mã; chưa thử thật.**

## Chung b9 — Nhập tên và Continue

Khi cây UI trả nhiều mục Continue có vùng lồng nhau bên dưới ô tên, dùng vùng ngoài cùng của cùng một nút. Nếu còn nhiều vùng riêng biệt, giữ điểm dừng. Dùng lại cây UI đã đọc để xác nhận ô tên và tìm nút.

Trên form Create account, gõ `First and last name` từ đúng hàng từng ký tự, đọc lại rồi bấm Continue đang hiển thị, có thể bấm và nằm dưới ô tên. Bỏ qua bản sao nhãn ẩn hoặc không thể bấm. Ảnh chưa có ô mật khẩu; không tự điền mật khẩu vào chỗ khác. q1 đã báo lỗi nhiều Continue; **đã sửa mã chung, chưa xác minh lại trên máy thật.**

## Chung b10 — Chuyển WhatsApp sang SMS

Ở màn Verify with WhatsApp, xác nhận đúng SĐT, bấm `Send code by SMS` một lần và chờ màn SMS. **Chỉ sau khi gửi mới đọc URL OTP** của đúng hàng. Nếu người dùng đã bấm gửi và đang ở màn SMS khi Tiếp tục, nhận màn đó mà không bấm gửi lặp. HTTP 403 trước khi gửi không được chặn thao tác gửi nữa; HTTP 403 kéo dài sau khi gửi làm máy dừng tại b11. **Đã sửa mã chung theo ảnh lỗi q1; chưa xác minh lại trên máy thật.**

Ảnh mới cho thấy báo HTTP 403 ở b10 trong khi màn còn WhatsApp. Mã nguồn hiện tại không gọi URL tại b10; test hồi quy xác nhận thứ tự bấm SMS → xác nhận màn SMS → đọc URL tại b11. Đây là dấu hiệu phiên tool trên màn có thể đang chạy mã cũ, chưa có bằng chứng phiên hiện tại đã nạp bản mới.

## Chung b11a — Chạm ô OTP trên màn SMS

Xác nhận màn SMS và đúng SĐT của hàng, sau đó chạm vào ô `Enter security code` nếu ô chưa có đủ sáu số. Bước này chạy trước khi đọc URL OTP nên lỗi nguồn mã không chặn thao tác chạm ô.

## Chung b11 — Lấy và gõ OTP SMS

Sau mốc 4 giây từ lúc gửi, đọc URL đúng hàng bằng Chrome ẩn hoặc Edge ẩn. Khi có mã, đọc lại màn SMS và xác nhận SĐT. Nếu Android báo ô mất focus, chạm lại trước khi gõ từng số. Đọc lại nội dung đã gõ. Nếu trình duyệt ẩn không đọc được, bấm Tiếp tục ở đúng hàng để mở trình duyệt thường hoặc nhập mã trên Amazon. Phản hồi chỉ có mã, không có dấu thời gian để phân biệt mã cũ. **Đã test mô phỏng; chưa thử thật sau sửa.**

## Chung b11b — Bấm Create your Amazon account

Sau khi OTP đúng, bấm Create một lần với khoảng kiểm tra riêng; nếu màn chưa chuyển, dừng để người dùng xem, không bấm lặp. **Đã nối mã; chưa có ảnh màn kết quả. Không khẳng định tài khoản thành công.**

## E01 — Dừng lỗi và Tiếp tục

Mỗi máy có bước hiện tại, lỗi và đồng hồ riêng. Khi lỗi, máy dừng tại chỗ; người dùng sửa trực tiếp rồi bấm Tiếp tục để đọc lại UI. Nếu q1/q2 đang ở màn SĐT dù mốc lưu đã tới b10, tool quay về b4 của chính máy đó và tạo lại trạng thái bước; không xóa hàng dữ liệu. Không gửi SMS hoặc bấm Create lặp khi màn phản hồi chậm; mốc Create đã bấm không tự tua lại. Chu kỳ lượt 3→4→5→4 phút rồi lặp. **Đã nối mã và test mô phỏng; cần thử thật sau sửa.**

## U01 — Màn sau Create chưa được hướng dẫn

Chưa có ảnh hay tiêu chí xác nhận kết quả sau nút Create. Tool chỉ báo đã xong các bước được hướng dẫn, không báo tài khoản thành công.

## U02 — q3–q12 chưa có b1–b3

Người dùng chưa gửi ảnh và hướng dẫn riêng cho b1–b3 của từng máy q3–q12. Các máy này vẫn dừng ở menu ba gạch. Không sao chép b1–b3 của q1 hoặc q2 sang chúng.

## U03 — Ảnh tiếp theo có thể bổ sung hoặc sửa quy trình

Đây là danh mục **những gì đã biết**, không phải quy trình cuối cùng. Khi nhận ảnh mới, cập nhật đúng máy và mốc, ghi màn trước/sau và mức kiểm chứng, sửa mã nếu cần, rồi cập nhật graph. Không tự điền bước chưa được người dùng chỉ.

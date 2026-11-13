# Luồng q1 từ menu ba gạch tới nhập OTP

## Thử trên q1 đã có

q1 cần ở trạng thái Running và Amazon đang hiện menu ba gạch. Dán một hàng Amazon của q1 gồm `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`, chọn Máy 1 và bấm **Thử q1 từ menu ba gạch**. Tool kiểm tra profile q1, mở tunnel ADB của đúng Device ID và đọc menu trước khi bắt đầu đồng hồ 3 phút. Thẻ được gắn cùng hàng nhưng chưa sử dụng trong b1–b11. Lỗi gắn kết không gửi yêu cầu OTP và không tạo tài khoản. Sau khi bắt đầu, lỗi ở mốc nào sẽ giữ mốc đó để sửa trên máy và bấm **Tiếp tục**. Nếu bấm **Làm lại / mẻ mới**, dữ liệu và trạng thái OTP trong tool sẽ mất.

Nguồn: chín ảnh người dùng gửi, đánh dấu b1–b11. Ảnh là ví dụ màn hình; khi chạy phải đọc cây UI Android của đúng ADB serial, xác nhận màn hình trước/sau mỗi thao tác và dùng thời hạn còn lại của q1. Ảnh b6 có tiêu đề cửa sổ `q6`, nên dropdown quốc gia trong ảnh chỉ là ví dụ cho q1 cho tới khi được kiểm tra trên q1 thật.

Nếu menu ba gạch của q1 hiện **dạng danh sách** như [ảnh mới](flow_images/shared/01_list_menu.png), tool dùng bộ phân loại chung: bấm Home, chỉ xem 2–5 giây, trở lại menu rồi bấm Sign In tại b4. Nhánh này thay b1–b3 dạng thẻ cho lượt đó; xem [MENU_ROUTING.md](MENU_ROUTING.md). Chưa thử nhánh mới trên q1 thật.

Mã hiện nhận diện bằng chữ hoặc `content-desc` và lấy vùng bấm từ cây UI hiện tại; ô nhập có thêm cách ghép với nhãn gần nó hoặc dùng ô duy nhất trên màn. `resource-id` cụ thể chưa biết vì chưa thu được bản dump UI q1; sẽ bổ sung sau khi đọc được cây UI trên q1 thật. Màn lạ hoặc nhiều phần tử cùng khớp làm q1 dừng, không dùng tọa độ ảnh để đoán.

| Mốc | Màn hình và mục tiêu | Cách nhận diện ưu tiên | Biến thể / điều kiện dừng |
| --- | --- | --- | --- |
| b1–b3 | Bấm lần lượt ba thẻ Gifting, Pets, Fashion and Beauty | Tìm đúng tên thẻ trong cây UI và bấm vào vùng của thẻ hiện tại. Sau mỗi lần bấm, nếu Amazon mở trang danh mục thì quay lại và xác nhận menu trước thẻ kế tiếp. | Nếu thẻ không hiện, cuộn trong danh sách với kích thước màn hiện tại. Không dùng tọa độ cố định từ ảnh. |
| b4 | Hàng Sign In ở cuối menu và form SĐT | Tìm văn bản `Sign In` trong vùng menu, cuộn khi cần, bấm; khi thấy form `Sign in or create account` thì **chạm ô SĐT** để lấy focus. Nếu đã ở form khi Tiếp tục, chạm ô ngay. | Nếu đã ở màn sau, phân loại lại thay vì bấm Sign In. |
| b5–b6 | Form `Sign in or create account`, số và mã quốc gia | Gõ đúng chuỗi SĐT của hàng q1 vào ô `Enter mobile number or email` trước. Sau đó mở dropdown, cuộn gần cuối nếu cần và chọn `United States +1`; đọc lại số/đầu mã quốc gia sau khi chọn. | Không tự cắt số đầu hoặc đổi định dạng SĐT theo ảnh. Nếu Amazon hiện số khác hàng q1, dừng để sửa. |
| b7 | Nút Continue của form số | Tìm nút `Continue` duy nhất trên đúng form, xác nhận số đang hiển thị đúng rồi bấm. | Nếu Amazon chuyển sang đăng nhập tài khoản cũ hoặc màn lạ, dừng q1. |
| b8 | Màn `Looks like you are new to Amazon` | Xác nhận số ở phần tóm tắt và nút `Proceed to create an account`. | Nếu số không khớp q1, dừng để sửa, không tiếp tục. |
| b9 | Form `Create account`, ô `First and last name` | Ghép nhãn với ô nhập gần nhất; gõ từng ký tự, đọc lại nội dung; bấm `Continue` của form sau khi đúng. | Ảnh chưa thấy ô mật khẩu. Không tự đoán hay nhập mật khẩu vào ô khác. |
| b10 | Màn `Verify with WhatsApp` | Nhận diện tiêu đề, số q1 và nút `Send code by SMS` duy nhất. Bấm gửi SMS một lần, xác nhận màn SMS, **sau đó** mới đọc URL q1. | Nếu người dùng đã gửi và màn SMS hiện tại, tiếp tục mà không gửi lặp. HTTP 403 sau khi gửi được thử lại tới hạn chờ OTP rồi dừng nếu vẫn lỗi. |
| b11 | Màn **OTP SMS** `Verify mobile number` | Chờ mã SMS Amazon mới từ URL q1, ghép nhãn `Enter security code` với ô nhập, gõ 6 số từng ký tự và kiểm tra lại. Sau đó bấm `Create your Amazon account`, đọc lại xem đã rời màn OTP. | Đồng hồ lượt chạy kết thúc ngay khi ô OTP đã đúng; thao tác bấm tạo tài khoản diễn ra sau mốc đó. Ảnh hiện chưa cho biết màn tiếp theo nên chưa khẳng định tài khoản đã tạo thành công. |

Mỗi mốc là bước có thể tiếp tục lại: trước khi bấm, đọc trạng thái thực tế để biết người dùng đã sửa và hoàn tất bước đó chưa. Nếu không nhận diện được phần tử duy nhất, cây UI thiếu thông tin, hoặc màn sau thao tác không đúng, q1 dừng tại chỗ. Khi người dùng bấm **Tiếp tục**, đọc lại màn hình và không gửi OTP hay tạo tài khoản lặp.

Ngày 13/11/2026, người dùng gửi thêm năm ảnh q1: màn SĐT đang trống, lỗi vùng bấm ở b6, hai `Continue` ở b9, HTTP 403 ở b10 và b10 không còn ở màn chọn SMS. q1 hiện ở màn nhập SĐT theo xác nhận của người dùng. Mã chung b4–b11 đã sửa để Tiếp tục đọc lại màn và quay về b4 nếu cần; không xóa hàng q1. Những sửa này đã qua test mô phỏng, **chưa được thử lại trên Swarmote thật**. Ảnh được lưu tại [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md). Riêng b1–b3 của q1 không đổi.

Sáu ảnh q1 mới cho thấy dropdown b6 vẫn ở đầu chữ A lúc báo lỗi, form b9 có một Continue nhìn thấy dưới ô tên và màn b10 vẫn là WhatsApp khi tool báo HTTP 403. Mã hiện tại cuộn tới US +1 có bounds hợp lệ, chọn Continue hiện/có thể bấm bên dưới ô tên và chỉ đọc URL tại b11 sau khi đã bấm SMS. Đã thêm test hồi quy b6 và thứ tự b10; chưa xác nhận phiên tool trên màn đã nạp mã hiện tại, và không đóng phiên vì dữ liệu chỉ ở RAM. Xem [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

Ảnh q1 tiếp theo ghi lỗi b4 `Không xác định được duy nhất 'Sign In'` khi menu dạng danh sách đã hiện Sign In dưới Customer Service. Mã chung giờ ưu tiên node Sign In có thể bấm, sau đó dùng vị trí dưới Customer Service làm mốc khi có nhãn lặp. Nếu người dùng tự bấm Sign In rồi nhấn Tiếp tục, b4 nhận form SĐT hiện tại và đi tiếp. Chưa có ADB dump q1 để chứng minh trên máy thật; ảnh lưu trong [IMAGE_EVIDENCE.md](IMAGE_EVIDENCE.md).

Thời hạn q1 là một đồng hồ chung từ menu tới **ô OTP SMS đã nhập đúng**, không phải 11 đồng hồ độc lập. Các lần chờ chuyển màn thông thường tối đa khoảng 10 giây; tìm mục bằng cuộn có giới hạn số lần; chờ SMS tối đa 30 giây. Mỗi thao tác còn bị chặn bởi thời gian thực tế còn lại của lượt, nên phần nào xong nhanh sẽ dành thời gian cho phần sau. Sau khi nhập đúng OTP, lần bấm Create có khoảng chờ riêng để kiểm tra Amazon đã rời màn OTP.

Quy tắc cho q2–q12: chỉ b1–b3 có thao tác riêng theo máy. b4–b11 dùng chung `build_common_steps` trong `account_flow.py`, nhưng mỗi máy khởi tạo hàm này riêng để giữ SĐT, URL OTP, mã, trạng thái gửi SMS và đồng hồ độc lập. q2 đã có b1–b3 riêng; q3–q12 chưa được bật sau menu vì chưa có hướng dẫn. Không sao chép tọa độ ảnh giữa các máy.

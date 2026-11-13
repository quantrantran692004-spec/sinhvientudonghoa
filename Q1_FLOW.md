# Luồng q1 từ menu ba gạch tới nhập OTP

## Thử trên q1 đã có

q1 cần ở trạng thái Running và Amazon đang hiện menu ba gạch. Dán một hàng Amazon của q1 gồm `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`, chọn Máy 1 và bấm **Thử q1 từ menu ba gạch**. Tool kiểm tra profile q1, mở tunnel ADB của đúng Device ID và đọc menu trước khi bắt đầu đồng hồ 3 phút. Thẻ được gắn cùng hàng nhưng chưa sử dụng trong b1–b11. Lỗi gắn kết không gửi yêu cầu OTP và không tạo tài khoản. Sau khi bắt đầu, lỗi ở mốc nào sẽ giữ mốc đó để sửa trên máy và bấm **Tiếp tục**. Nếu bấm **Làm lại / mẻ mới**, dữ liệu và trạng thái OTP trong tool sẽ mất.

Nguồn: chín ảnh người dùng gửi, đánh dấu b1–b11. Ảnh là ví dụ màn hình; khi chạy phải đọc cây UI Android của đúng ADB serial, xác nhận màn hình trước/sau mỗi thao tác và dùng thời hạn còn lại của q1. Ảnh b6 có tiêu đề cửa sổ `q6`, nên dropdown quốc gia trong ảnh chỉ là ví dụ cho q1 cho tới khi được kiểm tra trên q1 thật.

Mã hiện nhận diện bằng chữ hoặc `content-desc` và lấy vùng bấm từ cây UI hiện tại; ô nhập có thêm cách ghép với nhãn gần nó hoặc dùng ô duy nhất trên màn. `resource-id` cụ thể chưa biết vì q1 đang Offline; sẽ bổ sung sau khi đọc được cây UI trên q1 thật. Màn lạ hoặc nhiều phần tử cùng khớp làm q1 dừng, không dùng tọa độ ảnh để đoán.

| Mốc | Màn hình và mục tiêu | Cách nhận diện ưu tiên | Biến thể / điều kiện dừng |
| --- | --- | --- | --- |
| b1–b3 | Bấm lần lượt ba thẻ Gifting, Pets, Fashion and Beauty | Tìm đúng tên thẻ trong cây UI và bấm vào vùng của thẻ hiện tại. Sau mỗi lần bấm, nếu Amazon mở trang danh mục thì quay lại và xác nhận menu trước thẻ kế tiếp. | Nếu thẻ không hiện, cuộn trong danh sách với kích thước màn hiện tại. Không dùng tọa độ cố định từ ảnh. |
| b4 | Hàng Sign In ở cuối menu | Tìm văn bản `Sign In` duy nhất trong vùng menu, cuộn bằng kích thước màn hiện tại nếu chưa thấy. | Nếu menu đã ở màn sau đăng nhập, phân loại lại thay vì bấm. |
| b5–b6 | Form `Sign in or create account`, số và mã quốc gia | Gõ đúng chuỗi SĐT của hàng q1 vào ô `Enter mobile number or email` trước. Sau đó mở dropdown, cuộn gần cuối nếu cần và chọn `United States +1`; đọc lại số/đầu mã quốc gia sau khi chọn. | Không tự cắt số đầu hoặc đổi định dạng SĐT theo ảnh. Nếu Amazon hiện số khác hàng q1, dừng để sửa. |
| b7 | Nút Continue của form số | Tìm nút `Continue` duy nhất trên đúng form, xác nhận số đang hiển thị đúng rồi bấm. | Nếu Amazon chuyển sang đăng nhập tài khoản cũ hoặc màn lạ, dừng q1. |
| b8 | Màn `Looks like you are new to Amazon` | Xác nhận số ở phần tóm tắt và nút `Proceed to create an account`. | Nếu số không khớp q1, dừng để sửa, không tiếp tục. |
| b9 | Form `Create account`, ô `First and last name` | Ghép nhãn với ô nhập gần nhất; gõ từng ký tự, đọc lại nội dung; bấm `Continue` của form sau khi đúng. | Ảnh chưa thấy ô mật khẩu. Không tự đoán hay nhập mật khẩu vào ô khác. |
| b10 | Màn `Verify with WhatsApp` | Nhận diện tiêu đề, số q1 và nút `Send code by SMS` duy nhất. Đọc mã cũ trên URL q1 trước khi bấm gửi SMS. | Nếu đã ở màn SMS sau lần bấm trước thì tiếp tục; nếu chưa có mốc mã cũ thì dừng để kiểm tra. Nếu URL lỗi, dừng trước khi gửi. |
| b11 | Màn **OTP SMS** `Verify mobile number` | Chờ mã SMS Amazon mới từ URL q1, ghép nhãn `Enter security code` với ô nhập, gõ 6 số từng ký tự và kiểm tra lại. Sau đó bấm `Create your Amazon account`, đọc lại xem đã rời màn OTP. | Đồng hồ lượt chạy kết thúc ngay khi ô OTP đã đúng; thao tác bấm tạo tài khoản diễn ra sau mốc đó. Ảnh hiện chưa cho biết màn tiếp theo nên chưa khẳng định tài khoản đã tạo thành công. |

Mỗi mốc là bước có thể tiếp tục lại: trước khi bấm, đọc trạng thái thực tế để biết người dùng đã sửa và hoàn tất bước đó chưa. Nếu không nhận diện được phần tử duy nhất, cây UI thiếu thông tin, hoặc màn sau thao tác không đúng, q1 dừng tại chỗ. Khi người dùng bấm **Tiếp tục**, đọc lại màn hình và không gửi OTP hay tạo tài khoản lặp.

Thời hạn q1 là một đồng hồ chung từ menu tới **ô OTP SMS đã nhập đúng**, không phải 11 đồng hồ độc lập. Các lần chờ chuyển màn thông thường tối đa khoảng 10 giây; tìm mục bằng cuộn có giới hạn số lần; chờ SMS tối đa 30 giây. Mỗi thao tác còn bị chặn bởi thời gian thực tế còn lại của lượt, nên phần nào xong nhanh sẽ dành thời gian cho phần sau. Sau khi nhập đúng OTP, lần bấm Create có khoảng chờ riêng để kiểm tra Amazon đã rời màn OTP.

Quy tắc cho q2–q12: chỉ b1–b3 có thao tác riêng theo máy. b4–b11 dùng chung `build_common_steps` trong `account_flow.py`, nhưng mỗi máy khởi tạo hàm này riêng để giữ SĐT, URL OTP, mã, trạng thái gửi SMS và đồng hồ độc lập. q2 đã có b1–b3 riêng; q3–q12 chưa được bật sau menu vì chưa có hướng dẫn. Không sao chép tọa độ ảnh giữa các máy.

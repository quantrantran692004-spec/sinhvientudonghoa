# Quy tắc tự động hóa sau menu ba gạch

Phạm vi mới bắt đầu **sau** khi từng máy đã xác nhận `MENU_OPEN`. Luồng tạo Profile, Start, cài Amazon và mở menu hiện có được giữ nguyên. Các thao tác Amazon tiếp theo sẽ được bổ sung theo hướng dẫn màn hình của người dùng.

Người dùng hướng dẫn bằng ảnh màn hình từng máy, đã có **q1 và q2**. Với mỗi ảnh, cần xác định trạng thái màn hình, phân tích nhiều cách định vị và thao tác, chọn cách có thể kiểm tra kết quả, đồng thời tính đến lỗi thường gặp. **Chỉ b1–b3 khác nhau theo máy; từ b4 Sign In tới b11 OTP SMS và bấm tạo tài khoản là cùng một luồng cho q1–q12.** Mỗi máy vẫn có SĐT, tên, thẻ, URL OTP, trạng thái gửi mã, đồng hồ và điểm dừng/tiếp tục riêng. Thẻ hiện chỉ được giữ theo hàng, chưa sử dụng trong b1–b11. q3–q12 chỉ được nối sau khi người dùng hướng dẫn b1–b3 của từng máy.

## Nhận diện giao diện lúc chạy

- Ảnh người dùng gửi là ví dụ để xác định luồng, **không phải tọa độ cố định** cho các lần chạy. Trước mỗi thao tác, tool đọc lại cây giao diện Android của đúng ADB serial/profile và xác định màn hình hiện tại.
- Với mỗi màn hình được hướng dẫn, chuẩn bị nhiều cách nhận diện theo thứ tự ưu tiên: `resource-id` hoặc `content-desc` ổn định; nhãn chữ cùng loại phần tử và quan hệ với ô nhập; cuối cùng là vùng bấm lấy từ cây giao diện hiện tại. Chỉ dùng ảnh/OCR làm phương án bổ trợ nếu cây giao diện không đủ thông tin và đã kiểm chứng trên máy thật.
- Một màn hình có thể có nhiều biến thể hợp lệ. Mỗi biến thể phải có dấu hiệu nhận diện riêng và cùng một kết quả cần xác minh. Sau khi bấm/gõ, tool đọc lại giao diện để xác nhận đã sang đúng bước hoặc giá trị ô nhập đã đúng.
- Nếu Amazon đổi bố cục nhưng vẫn nhận diện được biến thể đã kiểm chứng, tool tiếp tục. Nếu màn hình lạ, phần tử không duy nhất hoặc kết quả sau thao tác không rõ, tool dừng **chỉ máy đó** ngay tại màn hình hiện tại. Nút **Tiếp tục** đọc lại màn hình mới sau khi người dùng sửa, rồi chọn bước phù hợp; không bấm lại theo tọa độ cũ.
- Mỗi lần chờ/đọc cây giao diện dùng thời gian còn lại trong đồng hồ của máy đó. Lỗi không làm tool tự quay về đầu hoặc gửi lại yêu cầu OTP.

## Từng máy độc lập

- Máy q1 đến q12 có `RunJob`, dữ liệu Amazon/URL OTP, tiến trình, bước hiện tại và đồng hồ lượt chạy riêng. Một máy lỗi không dừng các máy khác.
- Đồng hồ của mỗi máy bắt đầu khi máy đó xác nhận menu ba gạch (`MENU_OPEN`) và kết thúc khi đã **nhập xong OTP**. Giới hạn lượt đầu là 3 phút. Nếu cần tiếp tục sau lỗi, các lượt kế tiếp có 4 phút, 5 phút, 4 phút, rồi quay lại 3 phút và lặp lại. Đồng hồ lượt mới bắt đầu khi bấm **Tiếp tục** cho chính máy đó.
- Các thao tác chờ lấy phần thời gian còn lại của lượt. Không chia cứng một số giây cố định cho từng màn hình; hết thời gian thì dừng máy đó tại màn hiện tại.

## Nhập liệu và lỗi

- Dữ liệu được **gõ từng ký tự** vào Android; không dùng clipboard, paste hoặc đưa cả chuỗi vào một lệnh nhập. Bước nhập phải kiểm tra lại nội dung trường trước khi gửi form.
- Hàm gõ hiện hỗ trợ ký tự ASCII in được. Nếu gặp ký tự ngoài tập này, nó dừng trước khi gõ để người dùng sửa trực tiếp; cách gõ Unicode sẽ được xác minh trên máy thật khi xây từng màn hình.
- Khi một bước lỗi, máy ấy ngừng thao tác ngay, giữ nguyên màn hình để người dùng sửa trực tiếp. Tool hiển thị bước và lỗi ở đúng hàng. Không tự thử lại bước lỗi.
- Nút **Tiếp tục** tại hàng của máy lỗi chạy lại từ bước đang dừng. Mỗi bước sau menu phải đọc trạng thái màn hình trước khi thao tác: nếu người dùng đã hoàn thành bước đó thì chuyển tiếp; nếu vẫn ở bước cũ thì làm tiếp. Nhờ vậy tool không bấm gửi OTP hoặc tạo tài khoản lặp lại sau khi người dùng sửa.
- Nếu có CAPTCHA hoặc màn hình Amazon không nhận diện được, áp dụng cùng cơ chế dừng và tiếp tục; không đoán vị trí nút.

## Trạng thái hiện tại của dự án

`amazon_android/post_menu.py` có đồng hồ lượt riêng, cơ chế dừng/tiếp tục đúng bước và hàm gõ từng ký tự. Giao diện đã nối nút **Tiếp tục** tới phiên sau menu khi phiên đó tạm dừng. `amazon_android/account_flow.py` giữ nhận diện UI và `build_common_steps` cho b4–b11; `q1_flow.py` và `q2_flow.py` chỉ giữ b1–b3 riêng rồi gọi hàm chung. Mỗi máy tạo trạng thái OTP riêng. q1 và q2 đã được nối theo ảnh, gồm chọn SMS thay WhatsApp, lấy mã từ URL cùng hàng và gõ vào ô OTP. q3–q12 vẫn dừng ở menu, chờ b1–b3 riêng của từng máy. Màn sau nút `Create your Amazon account` chưa được hướng dẫn nên trạng thái hiện chỉ nói đã xong các bước b1–b11, không khẳng định tạo tài khoản thành công.

Trạng thái sau menu chỉ giữ trong bộ nhớ phiên. **Làm lại / mẻ mới** xóa chúng cùng dữ liệu của các hàng trong tool.

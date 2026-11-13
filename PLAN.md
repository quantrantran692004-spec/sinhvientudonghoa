# Quy trình Swarmote hiện tại

1. Dán tối đa 12 dòng proxy và tối đa 12 hàng `SĐT | Mật khẩu | Tên | Thẻ | URL OTP`; hàng n vào máy n của mẻ. Khi tạo Profile mới, số proxy phải đủ cho số hàng Amazon.
2. Slot Máy 1–12 dùng tên q1–q12. Nếu tên đã tồn tại, dừng để tránh tạo trùng; chính sách dùng lại profile cũ hoặc đặt tên mới chưa được người dùng chốt.
3. Pha 1: với từng máy, điền proxy, bấm Test Proxy và chỉ tạo khi Swarmote hiện Test Passed; xác nhận từng Profile. Lỗi một máy không chặn máy khác.
4. Pha 2: Start các Profile đã xác nhận theo nhóm 1–12 máy từ Settings (lưu qua các phiên), rồi mở ADB Shell, cài hoặc xác minh Amazon cho từng máy bằng Android Package Manager.
5. Mở Amazon; nếu gặp màn đăng nhập, dùng Skip sign in để tới trang chủ. Bấm Browse menu (nút ba gạch), xác nhận Shop by category hiện. q1 và q2 đã nối b1–b3 riêng rồi dùng chung b4–b11 tới nhập OTP SMS và bấm Create; q3–q12 dừng tại menu. Chưa có ảnh màn sau Create.
6. Hiển thị trạng thái riêng từng Profile. Nút dừng có hiệu lực sau bước hiện tại; Tiếp tục không gửi lại Create khi kết quả tạo chưa chắc chắn. Phần sau menu dừng tại màn lỗi và cho tiếp tục riêng từng máy.

# CURRENT TASK

Status: READY_FOR_ANTIGRAVITY
ID: TASK-003
Title: Hoàn thiện login và tài khoản sinh viên CNTT

## Mục tiêu
Hoàn thiện luồng đăng nhập sinh viên CNTT bằng danh mục đúng 900 tài khoản thuộc khóa 24, 25, 26; mỗi sinh viên đăng nhập lần đầu bằng chính mã sinh viên, vẫn tách biệt tuyệt đối với Admin và không làm hỏng Demo 1.

## Bằng chứng hiện trạng
- Web app dùng Flask-Login, `User` SQLAlchemy và bảng `users`; mật khẩu được hash qua Werkzeug.
- `auth.login()` nhận `username` hoặc `student_code`, kiểm tra mật khẩu, chặn tài khoản inactive, rồi chuyển Student tới `/dashboard` và Admin tới `/admin`.
- Seed hiện tại trong `app/__init__.py` chỉ tạo 3 tài khoản mẫu `24CT2001`–`24CT2003` với mật khẩu mặc định cũ; các mã này không theo quy tắc `KK5122NNNN` và không đáp ứng 900 tài khoản.
- Student/Admin đã có các route bảo vệ bằng `@login_required` và `@admin_required`; sinh viên không vào được `/admin`.
- Sinh viên chưa có route/giao diện tự đổi mật khẩu. Chỉ Admin có thể đặt lại mật khẩu qua `admin_edit_student()`; giao diện quản trị còn hiển thị mật khẩu mặc định cũ.
- Không tìm thấy hồ sơ/tham chiếu `TASK-006`. Hạng mục hoàn thành liên quan là `STB-20260910-01` (retrieval), được giữ nguyên.

## Nguồn yêu cầu tài khoản
Các quy tắc chi tiết `KK5122NNNN`, 3 khóa và 900 tài khoản có trong `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` ở root và được chủ sở hữu nhắc lại trong yêu cầu TASK-003. Bản `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` chưa có phần chi tiết này nhưng không mâu thuẫn; TASK-003 áp dụng yêu cầu cụ thể của chủ sở hữu.

## Phạm vi
- Tạo seed idempotent cho đúng 900 tài khoản Student: 24/25/26, mỗi khóa 300 mã `KK5122NNNN` với `NNNN` từ `0001` đến `0300`.
- Bảo đảm tài khoản Student mới có `student_code == username == mã sinh viên`, `role='student'`, `status='active'`, placeholder tối thiểu `Sinh viên <mã>` và password mặc định được hash từ chính mã sinh viên.
- Hoàn thiện login bằng mã sinh viên của danh mục trên; từ chối mã ngoài danh mục hoặc mật khẩu sai mà không lộ thông tin nội bộ.
- Bổ sung luồng Student tự đổi mật khẩu sau đăng nhập bằng cách dùng `User.check_password()`/`User.set_password()` hiện có.
- Điều chỉnh quản lý tạo tài khoản Student để không tiếp tục gợi ý hoặc tạo tài khoản mới với mật khẩu mặc định `123456`, đồng thời không cho phép username/mã sinh viên lệch quy tắc trong task này.
- Bổ sung kiểm thử seed/data integrity, login, phân quyền, đổi mật khẩu và regression Demo 1.

## Ngoài phạm vi
- Không thay đổi chatbot, PyTorch, intents, retrieval, materials, knowledge, feedback, history, model weight hoặc bất kỳ chức năng RAG/Semantic Search nào.
- Không thay đổi role Admin/Student, cơ chế `@login_required`, `@admin_required`, quyền truy cập hiện hữu hoặc trang Admin ngoài phần form tạo Student cần trực tiếp để bỏ mặc định `123456`.
- Không thêm dữ liệu cá nhân thật hay tự bịa thông tin sinh viên; chỉ dùng placeholder được duyệt.
- Không đổi database engine, schema không liên quan, thêm service/dependency, đăng ký tự do, email reset password hoặc migration phá hủy dữ liệu.
- Không xóa/sửa dữ liệu người dùng không xác định trong database đang tồn tại để ép số lượng; trường hợp database đã có Student ngoài danh mục phải được phát hiện và báo rõ, không tự xóa.

## Files dự kiến sửa
- `app/__init__.py` — gọi seed/migration logic tài khoản đúng danh mục thay cho 3 mẫu cũ.
- `app/auth.py` — route đổi mật khẩu Student và/hoặc validation login tối thiểu cần thiết.
- `app/routes.py` — chỉ phần admin tạo/quản lý Student cần trực tiếp để bảo toàn bất biến mã/username/password khởi tạo.
- `app/templates/login.html` — ví dụ/nhãn đăng nhập theo mã sinh viên mới.
- `app/templates/admin/students.html` — bỏ default `123456`, không yêu cầu dữ liệu cá nhân bịa đặt.
- `app/templates/user/dashboard.html`, `app/templates/user/materials.html`, `app/templates/user/info.html`, `app/templates/user/history.html` — thêm liên kết đổi mật khẩu nhất quán nếu cần để Student truy cập luồng mới.
- `tests/test_system.py` — cập nhật tài khoản mẫu sang mã hợp lệ và giữ regression Demo 1.

## Files dự kiến tạo nếu cần
- `app/student_accounts.py` — module thuần để tạo, kiểm tra và seed mã sinh viên; tạo file này để tách quy tắc 900 mã khỏi app factory, cho phép kiểm thử xác định và tránh duplicate logic.
- `app/templates/user/change_password.html` — form đổi mật khẩu cho Student đã đăng nhập.
- `tests/test_student_accounts.py` — unit/integration test độc lập cho generate/seed/validate 900 tài khoản và login rules.

## Yêu cầu bắt buộc
1. Danh mục mã hợp lệ là chính xác: `2451220001`–`2451220300`, `2551220001`–`2551220300`, `2651220001`–`2651220300`; không nhận ngành khác, khóa khác hoặc số thứ tự ngoài `0001`–`0300`.
2. Mỗi mã được tạo đúng một lần; `username` và `student_code` cùng bằng mã đó; password default là mã đó dưới dạng hash, không phải `123456`.
3. Seed phải idempotent và commit theo lô. Không reset mật khẩu đã được Student đổi khi app khởi động lại.
4. Admin giữ nguyên role/quyền/login; Student không thể thành Admin và vẫn bị cấm truy cập route Admin.
5. Chỉ placeholder `Sinh viên <mã sinh viên>` (hoặc `None` nếu UI xử lý được) được dùng cho họ tên; không thêm thông tin cá nhân.
6. Student đã đăng nhập phải đổi được mật khẩu sau khi nhập mật khẩu hiện tại và xác nhận mật khẩu mới; sai mật khẩu hiện tại/xác nhận không khớp phải bị từ chối.
7. Không được tự xóa các Student ngoài danh mục trong database đã tồn tại. Báo mismatch thay vì tác động dữ liệu không rõ nguồn.

## Acceptance Criteria
- [ ] Database mới hoặc test database sau seed có đúng 900 Student hợp lệ: 300 mã mỗi khóa, không trùng, không thiếu `0001`–`0300`, đúng `5122`; Admin vẫn tồn tại riêng.
- [ ] Mọi Student được seed có `username == student_code`, role Student, active; kiểm tra password default bằng `check_password(student_code)` và `check_password('123456')` không đúng với các tài khoản mới.
- [ ] Seed chạy lại không tạo trùng và không ghi đè mật khẩu Student đã đổi; database có Student ngoài danh mục được phát hiện/báo rõ chứ không bị xóa tự động.
- [ ] Sáu tài khoản biên hợp lệ (đầu/cuối của 3 khóa) đăng nhập được bằng mã/mật khẩu mặc định và tới `/dashboard`.
- [ ] Login bị từ chối cho mật khẩu sai, mã sai ngành, khóa ngoài 24–26, số thứ tự `0000`/`0301`, và mã không tồn tại.
- [ ] Student không truy cập `/admin`; Admin vẫn đăng nhập và truy cập `/admin` như trước.
- [ ] Student đổi mật khẩu thành công với mật khẩu hiện tại đúng; mật khẩu cũ không còn đăng nhập được, mật khẩu mới đăng nhập được; các lỗi xác thực bị từ chối.
- [ ] Regression Demo 1 pass: login Student, `/dashboard`, `/api/chat`, feedback, `/materials`, `/info`, `/history`, logout; retrieval `STB-20260910-01` không bị sửa và test retrieval hiện hữu vẫn pass.
- [ ] Không có source/diff ngoài danh sách được phê duyệt, không dependency/schema/AI/chatbot/retrieval thay đổi, và `ANTIGRAVITY_REPORT.md` chứa lệnh test thực tế.

## Test bắt buộc
- Unit test generator/validator: cardinality 900, 300/cohort, uniqueness, exact range, mã ngành, username mapping và placeholder.
- Seed test với SQLite in-memory: first seed, second seed idempotent, kiểm tra hash password cho toàn bộ hoặc tập bao phủ có giải thích, và bảo toàn password đã đổi.
- Login tests: sáu boundary accounts; password sai; sai ngành; khóa `23`/`27`; serial `0000`/`0301`; username không tồn tại; inactive Student.
- Authorization tests: Student `/admin` = 403, Admin `/admin` = 200, route protected redirect nếu anonymous.
- Password-change tests: anonymous bị redirect; current password sai; confirm sai; success; old password fail/new password pass.
- Regression: `tests/test_system.py`, `tests/test_quick.py`, `tests/evaluate.py`; kiểm tra riêng retrieval không thay đổi.

## Ràng buộc
- Không chạy migration/seed trên database thật trong phase implement nếu chưa sao lưu và chưa xác nhận target database. Test chỉ dùng SQLite in-memory/temporary.
- Không in, log hoặc đưa password vào report; chỉ mô tả quy tắc và kiểm tra hash.
- Giữ nguyên `CODEX_REVIEW.md` cho đến khi Antigravity hoàn thành và Codex review lại.
- Khi phát hiện mâu thuẫn giữa database thực tế và yêu cầu 900 tài khoản, dừng thay vì tự xóa hoặc đổi role tài khoản hiện có.

## Workflow State
`READY_FOR_ANTIGRAVITY`

## Repair Cycle
0 / 3

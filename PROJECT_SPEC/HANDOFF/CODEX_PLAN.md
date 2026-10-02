# CODEX PLAN

Status: READY_FOR_ANTIGRAVITY
Task ID: TASK-003

## Phân tích hiện trạng authentication
- App runtime là Flask + Flask-Login + Flask-SQLAlchemy. `create_app()` cấu hình `DATABASE_URL`, gọi `db.create_all()` rồi `seed_initial_data()`.
- `User` có `student_code` unique (nullable), `username` unique, `password_hash`, `role`, `status`, timestamps; `set_password()`/`check_password()` dùng Werkzeug hash.
- `/login` tra `username` hoặc `student_code` (upper-case), kiểm tra hash/status, gọi `login_user()`, phân hướng theo `is_admin()`; `/logout` yêu cầu login.
- Các route Student dùng `@login_required`; route Admin dùng thêm `@admin_required`, trả 403 cho Student.
- Hiện seed chỉ có Admin và 3 Student mẫu với mã/mật khẩu không đúng TASK-003. Không có migration framework; `db.create_all()` không chuyển đổi schema đã có.
- Admin có route reset mật khẩu trong `admin_edit_student()`, nhưng Student không có self-service change-password route/template. Form tạo Student còn đòi họ tên và default `123456`.
- `framework/src/database/db.py` là SQLite API cũ không được web app import; không sửa trong TASK-003.

## Phạm vi triển khai đã chốt
Tạo catalog 900 Student CNTT và hoàn thiện login/change-password dựa trên model/role hiện có. Giữ nguyên engine SQLAlchemy, schema `User`, Flask-Login, Admin, route protection và Demo 1. Không chỉnh chatbot/retrieval; task retrieval đã phê duyệt `STB-20260910-01` không có mã `TASK-006` chính thức trong repository.

## File sẽ sửa
1. `app/__init__.py`: thay 3 Student mẫu bằng gọi seed account catalog; giữ Admin seed và seed dữ liệu materials/knowledge.
2. `app/auth.py`: thêm route đổi mật khẩu chỉ cho user đã login; dùng current password + new password + confirmation, không đổi role/code.
3. `app/routes.py`: giới hạn phần tạo/reset Student để không tạo tài khoản mới với `123456` hoặc username khác mã hợp lệ. Không refactor route không liên quan.
4. `app/templates/login.html`: thay placeholder ví dụ cũ bằng mã `2451220001`.
5. `app/templates/admin/students.html`: bỏ họ tên bắt buộc/fake example và default `123456`; hiển thị hướng dẫn username/password initial = mã SV khi thực sự cần.
6. Bốn sidebar Student (`dashboard.html`, `materials.html`, `info.html`, `history.html`): liên kết tới đổi mật khẩu.
7. `tests/test_system.py`: thay sample `24ct2001/123456` bằng account hợp lệ và mở rộng regression route/login theo scope.

## File sẽ tạo nếu cần
1. `app/student_accounts.py`: xác định constants, `generate_student_codes()`, `is_valid_student_code()`, builder placeholder và `seed_student_accounts(session)`. Đây là cần thiết để logic seed/validation dùng chung và testable, thay vì nhồi quy tắc vào app factory/route.
2. `app/templates/user/change_password.html`: form có old/new/confirm password, không hiển thị password.
3. `tests/test_student_accounts.py`: kiểm tra generator/seed/login/change password một cách cô lập trên SQLite in-memory.

## Cách tạo/seed 900 tài khoản
1. Khai báo duy nhất 3 prefix hợp lệ: `245122`, `255122`, `265122`; sinh serial bằng `f'{serial:04d}'` từ 1 đến 300. Kiểm tra output có exactly 900 mã unique trước khi ghi DB.
2. Với mỗi code, dựng `User(student_code=code, username=code, full_name=f'Sinh viên {code}', role='student', status='active')`; gọi `set_password(code)` để lưu hash.
3. Truy vấn các target code hiện có trước; chỉ thêm mã còn thiếu theo lô và commit một lần. Không dùng bulk insert bỏ qua password hashing.
4. Nếu target code đã có, xác minh `username`, role và student_code nhất quán; không tự reset `password_hash`, vì Student có quyền đổi password. Mismatch phải raise/report để review.
5. Không xóa account ngoài catalog. Trong test/fresh DB, assertion tổng Student = 900. Trong database không rỗng, chỉ báo rõ số account ngoài catalog; không giả vờ đó là trạng thái đạt.
6. Admin được tạo/giữ bởi logic riêng; không đưa Admin vào catalog, không thay role hoặc password Admin.

## Cách giữ Student/Admin và Demo 1
- Giữ `User.is_admin()`, `admin_required`, `login_required`, endpoint names và redirect hiện tại.
- Password change chỉ thao tác `current_user.password_hash` sau `check_password()`; không nhận id user và không cho sửa `role`, `username`, `student_code`.
- Admin create/reset Student phải validate mã và giữ `role='student'`; tuyệt đối không dùng input role từ form.
- Regression dùng một mã hợp lệ của catalog để vào `/dashboard`, gọi chat/feedback, mở materials/info/history và logout. Không đổi `framework/`, `data/`, model weight hay `app/routes.py` ngoài đoạn quản lý Student.

## Kiểm tra dữ liệu và login
1. Generator test: set codes = expected set (`3 * 300`), count theo `code[:2]`, prefix `code[2:6] == '5122'`, serial integer in range; duplicate count 0.
2. Seed test trên database in-memory trống: 900 Student + 1 Admin; query theo cohort = 300; `student_code == username`; hashes khớp code và không khớp default cũ.
3. Idempotency: gọi app/seed lần hai, count không tăng; đổi password một Student rồi seed lại, xác minh mật khẩu mới vẫn hợp lệ.
4. Login test: 6 codes boundary; 5 nhóm reject bắt buộc; inactive Student bị chặn.
5. Change password: route protected, reject old/confirm invalid, success invalidates old password and accepts new password.
6. Chạy `tests/test_system.py`, `tests/test_quick.py`, `tests/evaluate.py`; test retrieval phải giữ kết quả đã phê duyệt. Ghi interpreter tuyệt đối và lệnh/kết quả chính xác trong report.

## Rủi ro và cách giảm thiểu
- **Dữ liệu tồn tại:** seed 900 vào DB không rỗng có thể không đạt count tổng hoặc va chạm unique. Giảm thiểu: test in-memory, preflight audit, idempotent add-only, không xóa account không rõ nguồn; backup database trước khi cho phép chạy trên DB thật.
- **Password đã đổi:** re-seed không được reset hash. Giảm thiểu: chỉ hash khi tạo mới.
- **Hash 900 mật khẩu:** có thể làm test chậm. Giảm thiểu: tạo theo lô/commit một lần, không giảm cost hash production; ghi thời gian test nếu dài.
- **Demo 1/retrieval:** thay seed làm test cũ dùng tài khoản mẫu thất bại. Giảm thiểu: cập nhật test/demo credentials sang catalog hợp lệ và chạy full regression, không đụng code chatbot/retrieval.
- **Tài liệu mâu thuẫn/thiếu:** `PROJECT_SPEC` bản copy thiếu chi tiết catalog, root master có thêm Section 3.2. Giảm thiểu: áp dụng yêu cầu chủ sở hữu và ghi nhận nguồn; nếu xuất hiện quy tắc xung đột mới, dừng xin xác nhận.

## Rollback
1. Không chạy thay đổi trên database thật trước backup/export và preflight xác nhận target.
2. Nếu seed/migration thực thi sai trên môi trường dev, khôi phục file database từ backup trước task; không dùng xóa hàng loạt không kiểm tra.
3. Code rollback: revert duy nhất diff TASK-003 sau khi xác nhận không có thay đổi user password mới cần bảo toàn.
4. Trên test database, hủy instance/in-memory DB sau test; không tác động dữ liệu chia sẻ.

## Thứ tự triển khai cho Antigravity
1. Đọc task/rules/plan; xác nhận working tree và target DB, tạo backup nếu môi trường thực thi không phải test.
2. Viết unit tests cho catalog/validator trước, rồi tạo module account thuần.
3. Tích hợp seed idempotent vào app factory; chạy kiểm tra 900/300/unique/range/hash trên in-memory DB.
4. Thay placeholder login/admin form và harden route tạo Student đúng invariant.
5. Thêm Student change-password route/template/nav; test success/failure/authorization.
6. Cập nhật regression Demo 1 từ sample credential cũ sang catalog hợp lệ.
7. Chạy focused tests rồi full relevant tests; rà diff và report chính xác. Không thay đổi các file ngoài task.

## Cổng phê duyệt
Không cần thay schema/architecture/dependency nên không có cổng phê duyệt kỹ thuật mới. Tuy nhiên, mọi đề xuất xóa Student tồn tại, reset password đã đổi, chạy seed trên database không có backup, hoặc sửa role/route protection là cổng dừng bắt buộc để chủ sở hữu quyết định.

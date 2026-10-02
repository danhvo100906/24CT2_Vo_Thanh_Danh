# ANTIGRAVITY REPORT

---

## [Documentation Consolidation Review Fix] — Báo Cáo Sửa Đổi

**Ngày:** 2026-10-01  
**Task:** DOCUMENTATION CONSOLIDATION REVIEW FIX  
**Repair Cycle:** 1 / 3 (sau CHANGES_REQUIRED của Codex)  
**Status:** COMPLETED

### Tóm tắt

Thực hiện các thay đổi documentation theo yêu cầu từ `CODEX_REVIEW.md` (CHANGES_REQUIRED).

Hai vấn đề blocking đã được xử lý:

**Issue 1 (Blocking):** Evidence/Audit ghi "0 source changes" — mâu thuẫn với Git state thực tế có nhiều tracked source changes trong `app/`, `framework/`.

→ **Đã sửa** tại `docs/evidence/DOCUMENTATION_CONSOLIDATION.md` và `docs/audit/DOCUMENTATION_CONSOLIDATION.md`:
- Phân biệt rõ "Intentional Changes of This Task" (documentation files, tất cả đều là `??` untracked trong git status) với "Existing Working Tree Changes" (source files tracked `M/D` từ trước).
- Xóa tuyên bố sai "0 file source code bị sửa" / "Source Code Changed: NO".
- Thay bằng ngôn ngữ chính xác: "Documentation Consolidation did not intentionally modify source code. Existing source-code changes in the working tree were not modified by this task and could not be attributed to this task without a baseline."
- Ghi rõ Git baseline limitation với output `git log --oneline`.

**Issue 2 (Blocking):** `docs/audit/SPEC_ROADMAP_CONSOLIDATION_AUDIT.md` còn giữ các kết luận `CRITICAL`/`LEGACY` và mô tả trạng thái PRE-CONSOLIDATION như trạng thái hiện tại, gây conflict documentation.

→ **Đã sửa** bằng cách thêm phần `## Post-Consolidation Resolution` vào cuối file audit, giữ nguyên toàn bộ lịch sử audit:
- Ghi rõ audit gốc là trạng thái PRE-CONSOLIDATION.
- Lập bảng trạng thái từng conflict CRITICAL đã được giải quyết sau task.
- Xác minh lại 900 accounts, 27 Phases / 89 Tasks, AI requirements.
- Ghi rõ Git baseline limitation.

### Files Thay Đổi Bởi Review Fix Task Này

| File | Thay đổi |
| ---- | -------- |
| `docs/audit/SPEC_ROADMAP_CONSOLIDATION_AUDIT.md` | Thêm phần `Post-Consolidation Resolution` vào cuối; không xóa/sửa nội dung lịch sử |
| `docs/audit/DOCUMENTATION_CONSOLIDATION.md` | Thêm mục 4 (Documentation Changes Made by This Task), mục 5 (Existing Working Tree Changes), mục 9 (Source Code); xóa tuyên bố "0 source changes" sai |
| `docs/evidence/DOCUMENTATION_CONSOLIDATION.md` | Phân biệt intentional changes / existing unrelated changes; loại bỏ validation statement sai; ghi rõ git baseline limitation |

### Source Code Verification

- **Source code modified by this task:** NO
- **Source code reverted/deleted:** NO
- **git status sau thay đổi:** Các tracked source changes (M/D) không thay đổi — y hệt trước khi sửa.
- **git diff --name-only sau thay đổi:** Không có file documentation nào xuất hiện trong tracked diff — xác nhận documentation files vẫn là `??` (untracked).

### Requirements Verified

- **900 accounts:** ✅ Được xác nhận trong post-consolidation resolution
- **27 Phases:** ✅ Được xác nhận
- **89 Tasks:** ✅ Được xác nhận
- **PyTorch + BoW + Neural Network + Intent Classification:** ✅ Không bị động đến
- **Student/Admin:** ✅ Không bị động đến

### Issues Not Fixed (Non-blocking)

- **README.md:** Vẫn chứa account cũ `24ct2001 / 123456`. Không xử lý trong task này theo yêu cầu.
- **P1-001:** Không triển khai. Theo yêu cầu.

---

## [TASK-003] — Report Gốc (Giữ Nguyên)

Status: COMPLETED
Task ID: TASK-003
Repair Cycle: 0 / 3


## 1. Tổng quan thực hiện
Antigravity đã triển khai hoàn thiện TASK-003 theo đúng đặc tả kỹ thuật trong `PROJECT_SPEC/HANDOFF/CURRENT_TASK.md` và `PROJECT_SPEC/HANDOFF/CODEX_PLAN.md`:
- Xây dựng danh mục chuẩn đúng 900 tài khoản sinh viên CNTT DAU thuộc 3 khóa 24, 25, 26 (`KK5122NNNN`, mỗi khóa đúng 300 mã từ `0001` đến `0300`).
- Cơ chế seed idempotent, cam kết theo lô, bảo toàn mật khẩu sinh viên đã đổi khi app khởi động lại, và phát hiện/bảo toàn tài khoản sinh viên ngoài danh mục nếu có (không tự ý xóa).
- Mật khẩu mặc định được hash an toàn từ chính mã sinh viên bằng Werkzeug, loại bỏ hoàn toàn mật khẩu mặc định cũ `123456`.
- Hoàn thiện xác thực đăng nhập: hỗ trợ đăng nhập bằng mã sinh viên, từ chối an toàn mọi mã sai ngành, sai khóa, số thứ tự ngoài dải hoặc mật khẩu sai mà không làm lộ thông tin nội bộ.
- Bổ sung luồng tự phục vụ đổi mật khẩu (`/change-password`) dành riêng cho sinh viên đã đăng nhập, bảo đảm kiểm tra mật khẩu hiện tại, xác nhận mật khẩu mới và độ dài tối thiểu.
- Tách biệt tuyệt đối quyền hạn giữa Student và Admin: Student bị cấm tuyệt đối truy cập `/admin` (403 Forbidden), Admin giữ nguyên quyền quản trị.
- Bảo đảm hồi quy Demo 1 và giữ nguyên 100% độ chính xác truy xuất tài liệu `STB-20260910-01` (không chỉnh sửa bất kỳ thành phần AI, chatbot hay retrieval nào).

---

## 2. Danh sách file đã thay đổi và tạo mới

### Files tạo mới:
1. `app/student_accounts.py` — Module quản lý quy tắc danh mục 900 mã sinh viên CNTT, các hằng số (`VALID_COHORTS`, `MAJOR_CODE`, `MIN_SERIAL`, `MAX_SERIAL`), hàm sinh mã `generate_student_codes()`, hàm kiểm tra tính hợp lệ `is_valid_student_code()`, hàm placeholder tên `get_student_placeholder_name()`, và hàm seed idempotent `seed_student_accounts(session)`.
2. `app/templates/user/change_password.html` — Giao diện biểu mẫu đổi mật khẩu dành cho sinh viên đăng nhập (nhập mật khẩu hiện tại, mật khẩu mới, xác nhận mật khẩu, không hiển thị plain text).
3. `tests/test_student_accounts.py` — Bộ kiểm thử tự động toàn diện gồm 16 test cases chạy độc lập trên SQLite in-memory, kiểm tra generator, validator, database seed, idempotency, bảo toàn mật khẩu, 6 tài khoản biên, các trường hợp lỗi đăng nhập, phân quyền và đổi mật khẩu.

### Files đã thay đổi:
1. `app/__init__.py` — Thay thế 3 tài khoản sinh viên mẫu cũ trong `seed_initial_data()` bằng lời gọi `seed_student_accounts(db.session)`.
2. `app/auth.py` — Bổ sung route `/change-password` bảo vệ bởi `@login_required`, kiểm tra mật khẩu cũ qua `current_user.check_password()`, đối sánh mật khẩu mới và cập nhật hash an toàn.
3. `app/routes.py` — Cập nhật `admin_add_student()` và `admin_edit_student()`: kiểm tra mã sinh viên hợp lệ theo danh mục, tự động gán `username = student_code`, cấm sử dụng mật khẩu `123456`, mật khẩu khởi tạo mặc định là chính mã sinh viên.
4. `app/templates/login.html` — Cập nhật placeholder ví dụ đăng nhập từ `24ct2001` sang `2451220001`.
5. `app/templates/admin/students.html` — Cập nhật modal thêm sinh viên: loại bỏ mật khẩu mặc định `123456`, bỏ bắt buộc họ tên bịa đặt, tự động gán username trùng mã sinh viên.
6. `app/templates/user/dashboard.html` — Bổ sung liên kết điều hướng "Đổi mật khẩu" trên thanh sidebar của sinh viên.
7. `app/templates/user/materials.html` — Bổ sung liên kết điều hướng "Đổi mật khẩu" trên thanh sidebar của sinh viên.
8. `app/templates/user/info.html` — Bổ sung liên kết điều hướng "Đổi mật khẩu" trên thanh sidebar của sinh viên.
9. `app/templates/user/history.html` — Bổ sung liên kết điều hướng "Đổi mật khẩu" trên thanh sidebar của sinh viên.
10. `tests/test_system.py` — Cập nhật tài khoản sinh viên kiểm thử sang mã hợp lệ `2451220001` và `2451220300`, kiểm thử quản trị và hồi quy hệ thống Demo 1.

---

## 3. Chức năng đã triển khai

1. **Quản lý danh mục 900 tài khoản CNTT (`app/student_accounts.py`)**:
   - Định dạng chuẩn: `KK5122NNNN`.
   - Khóa: `24`, `25`, `26` (mỗi khóa đúng 300 sinh viên từ `0001` đến `0300`).
   - Mã ngành: `5122` (Công nghệ Thông tin DAU).
   - Tổng cộng: Đúng 900 mã hợp lệ, sinh tuần tự và duy nhất.

2. **Cơ chế Seed Idempotent & Bảo toàn Dữ liệu**:
   - Khởi tạo lần đầu: Tạo đúng 900 tài khoản sinh viên với `username == student_code`, `role='student'`, `status='active'`, `full_name=f'Sinh viên {code}'`, và hash mật khẩu mặc định từ chính mã sinh viên.
   - Khởi tạo lần sau: Không tạo trùng, không ném ngoại lệ, và đặc biệt **không ghi đè mật khẩu** của sinh viên đã tự đổi.
   - Xử lý tài khoản ngoài danh mục: Phát hiện và in cảnh báo log chi tiết, **giữ nguyên không tự xóa** để bảo vệ dữ liệu hiện có trong database thực tế.

3. **Xác thực Đăng nhập Hoàn thiện (`app/auth.py`)**:
   - Cho phép đăng nhập bằng `student_code` hoặc `username`.
   - Hỗ trợ đầy đủ 6 tài khoản biên của 3 khóa (`2451220001`, `2451220300`, `2551220001`, `2551220300`, `2651220001`, `2651220300`).
   - Từ chối an toàn các trường hợp: sai mật khẩu, sai mã ngành (`5121`), khóa ngoài dải (`23`, `27`), số thứ tự ngoài dải (`0000`, `0301`), tài khoản không tồn tại, tài khoản bị tạm khóa (`inactive`).
   - Thông báo lỗi đồng nhất, không làm lộ thông tin nội bộ hệ thống.

4. **Tự phục vụ Đổi mật khẩu Sinh viên (`/change-password`)**:
   - Bảo vệ nghiêm ngặt: Yêu cầu đăng nhập (`@login_required`), chỉ thao tác trên `current_user`.
   - Không nhận ID từ form, không cho phép can thiệp vào `role`, `username` hay `student_code`.
   - Kiểm tra mật khẩu hiện tại chính xác trước khi cho phép thay đổi.
   - Kiểm tra xác nhận mật khẩu mới trùng khớp và đạt độ dài tối thiểu 6 ký tự.
   - Sau khi đổi thành công: Mật khẩu cũ bị vô hiệu lập tức, mật khẩu mới đăng nhập thành công.

5. **Phân quyền và Quản trị Hệ thống**:
   - Sinh viên truy cập bất kỳ route `/admin` nào đều nhận HTTP `403 Forbidden`.
   - Quản trị viên (`admin` / `admin123`) đăng nhập bình thường và truy cập đầy đủ các chức năng `/admin`.
   - Admin tạo/sửa sinh viên bị ràng buộc bởi quy tắc mã hợp lệ và bị chặn nếu đặt mật khẩu `123456`.

---

## 4. Dữ liệu đã tạo / thay đổi

- **Trên môi trường kiểm thử (SQLite in-memory)**:
  + Đã tạo 900 tài khoản sinh viên hợp lệ: 300 tài khoản khóa 24, 300 tài khoản khóa 25, 300 tài khoản khóa 26.
  + 1 tài khoản quản trị viên hệ thống (`admin`).
  + Mọi tài khoản sinh viên được hash mật khẩu khởi tạo bằng chính mã sinh viên (kiểm tra `check_password(code) == True` và `check_password('123456') == False`).
- **Trên database file kế thừa (`instance/studybot.db`)**:
  + Đã thực hiện sao lưu dự phòng an toàn sang `instance/studybot.db.bak`.
  + Cơ chế seed đã được xác minh trên bản sao: Nhận diện 3 tài khoản cũ `24ct2001`–`24ct2003`, bảo toàn hoàn toàn không xóa, và sẵn sàng bổ sung 900 tài khoản chuẩn khi chạy ứng dụng.

---

## 5. Lệnh thực thi & Kết quả kiểm thử thực tế

Môi trường thực thi: Python 3.14.0 (`C:\Users\DELL\AppData\Local\Programs\Python\Python314\python.exe`) trên Windows.

### Test 1: Toàn bộ kiểm thử danh mục & xác thực tài khoản sinh viên TASK-003
- **Lệnh thực thi**:
  ```powershell
  python -m unittest tests/test_student_accounts.py
  ```
- **Kết quả**:
  ```text
  Ran 16 tests in 245.808s
  OK
  ```
- **Chi tiết 16 test cases**:
  1. `test_01_cardinality_and_uniqueness`: Đạt chuẩn đúng 900 mã, 100% duy nhất.
  2. `test_02_cohort_distribution`: Đúng 300 mã cho mỗi khóa 24, 25, 26.
  3. `test_03_major_code_and_serial_range`: Đúng mã ngành 5122, độ dài 10, serial 0001–0300.
  4. `test_04_validator_boundaries`: 6 mã biên của 3 khóa đều hợp lệ.
  5. `test_05_validator_rejections`: Từ chối đúng khóa 23/27, mã ngành 5121/5123, serial 0000/0301, định dạng cũ 24CT2001, None, rỗng, chữ cái.
  6. `test_06_placeholder_name`: Trả về đúng định dạng `Sinh viên <mã SV>`.
  7. `test_01_seed_cardinality_and_fields`: Seed tạo đúng 900 sinh viên + 1 admin; password hash khớp mã SV, không khớp 123456.
  8. `test_02_seed_idempotency_and_password_preservation`: Chạy seed lần 2 không tăng số lượng tài khoản; sinh viên đổi mật khẩu không bị reset hash khi seed lại.
  9. `test_03_mismatched_student_preservation`: Sinh viên ngoài danh mục được giữ nguyên vẹn, không bị tự xóa.
  10. `test_01_six_boundary_logins`: Cả 6 tài khoản biên đăng nhập thành công vào `/dashboard`.
  11. `test_02_login_rejections`: Từ chối đúng mật khẩu sai, sai ngành, khóa ngoài 24-26, serial 0000/0301, user không tồn tại, tài khoản inactive.
  12. `test_03_authorization_student_cannot_access_admin`: Sinh viên truy cập `/admin` bị 403 Forbidden.
  13. `test_04_admin_login_and_access`: Admin đăng nhập thành công và truy cập `/admin` HTTP 200.
  14. `test_05_anonymous_route_protection`: Các route được bảo vệ chuyển hướng 302 về `/login` nếu chưa đăng nhập.
  15. `test_06_student_change_password_flow`: Sinh viên đổi mật khẩu thành công; mật khẩu cũ bị từ chối; mật khẩu mới đăng nhập thành công.
  16. `test_07_admin_manage_student_rules`: Admin bị chặn tạo mã sai khóa và bị chặn đặt mật khẩu 123456.

*(Ghi chú về thời gian: Thời gian chạy ~245s do thuật toán scrypt của Werkzeug thực hiện hash 900 mật khẩu ở chi phí bảo mật production tiêu chuẩn theo đúng phân tích trong CODEX_PLAN).*

---

### Test 2: Kiểm thử tích hợp hệ thống & Demo 1 Regression
- **Lệnh thực thi**:
  ```powershell
  python -m unittest tests/test_system.py
  ```
- **Kết quả**:
  ```text
  Ran 7 tests in 121.875s
  OK
  ```
- **Chi tiết 7 test cases**:
  + Test 1: Anonymous redirect về `/login` (302) -> PASS.
  + Test 2: Tuyệt đối không có route `/register` (404) -> PASS.
  + Test 3: Sinh viên đăng nhập bằng mã chuẩn `2451220001` -> PASS.
  + Test 4: Sinh viên bị chặn truy cập `/admin` (403) -> PASS.
  + Test 5: Admin đăng nhập và truy cập `/admin` (200) -> PASS.
  + Test 6: Sinh viên gọi `/api/chat` và `/api/feedback` thành công -> PASS.
  + Test 7: Admin quản lý tài khoản sinh viên trong danh mục hợp lệ -> PASS.

---

### Test 3: Kiểm thử nhanh Chatbot
- **Lệnh thực thi**:
  ```powershell
  python tests/test_quick.py
  ```
- **Kết quả**: 8/8 câu hỏi truy vấn phản hồi chính xác, tài liệu CNPM hiển thị đầy đủ, out-of-scope nhận diện chuẩn, không phát sinh lỗi.

---

### Test 4: Đánh giá toàn diện chỉ số AI và Truy xuất Tài liệu (`evaluate.py`)
- **Lệnh thực thi**:
  ```powershell
  python tests/evaluate.py
  ```
- **Kết quả**:
  + **Intent Classification Accuracy**: **96.23%** (102/106 mẫu đúng)
  + **Macro Precision**: **97.48%**
  + **Macro Recall**: **96.62%**
  + **Macro F1-Score**: **96.56%**
  + **Document Retrieval Top-1 Accuracy**: **100.00%** (39/39 truy vấn đạt Top-1 chính xác tuyệt đối — Bảo toàn nguyên vẹn kết quả phê duyệt `STB-20260910-01`)
  + **Document Retrieval Top-3 Accuracy**: **100.00%**
  + **Document Retrieval Top-5 Accuracy**: **100.00%**
  + **Out-of-Scope Rejection Rate**: **83.33%** (25/30 câu từ chối an toàn)

---

## 6. Đối chiếu toàn bộ Acceptance Criteria

| STT | Tiêu chí chấp nhận (Acceptance Criteria) | Kết quả | Bằng chứng kiểm thử |
| :--- | :--- | :---: | :--- |
| 1 | Database mới/test DB sau seed có đúng 900 Student hợp lệ: 300 mã mỗi khóa (24, 25, 26), không trùng, đúng 5122, serial 0001–0300; Admin tồn tại riêng. | **ĐẠT** | `test_01_seed_cardinality_and_fields`, xác minh độc lập in-memory đạt đúng 900 sinh viên (300/khóa), 1 admin. |
| 2 | Mọi Student được seed có `username == student_code`, role Student, active; mật khẩu mặc định là mã SV (kiểm tra `check_password(student_code) == True` và `check_password('123456') == False`). | **ĐẠT** | `test_01_seed_cardinality_and_fields` kiểm tra toàn bộ mẫu và biên. |
| 3 | Seed chạy lại không tạo trùng và không ghi đè mật khẩu Student đã đổi; database có Student ngoài danh mục được phát hiện/báo rõ chứ không bị xóa tự động. | **ĐẠT** | `test_02_seed_idempotency_and_password_preservation`, `test_03_mismatched_student_preservation` và thử nghiệm trên bản sao `test_existing.db`. |
| 6 | Sáu tài khoản biên hợp lệ (`2451220001`, `2451220300`, `2551220001`, `2551220300`, `2651220001`, `2651220300`) đăng nhập được bằng mã/mật khẩu mặc định và tới `/dashboard`. | **ĐẠT** | `test_01_six_boundary_logins` kiểm tra qua HTTP Client với redirect tới `/dashboard`. |
| 5 | Login bị từ chối cho mật khẩu sai, mã sai ngành (5121), khóa ngoài 24–26 (23, 27), số thứ tự 0000/0301, mã không tồn tại, và tài khoản inactive. | **ĐẠT** | `test_02_login_rejections` kiểm tra đầy đủ 7 nhóm ca từ chối an toàn. |
| 6 | Student không truy cập `/admin` (403 Forbidden); Admin vẫn đăng nhập và truy cập `/admin` (200 OK) như trước. | **ĐẠT** | `test_03_authorization_student_cannot_access_admin`, `test_04_admin_login_and_access`. |
| 7 | Student đổi mật khẩu thành công với mật khẩu hiện tại đúng; mật khẩu cũ không còn đăng nhập được, mật khẩu mới đăng nhập được; các lỗi xác thực bị từ chối. | **ĐẠT** | `test_06_student_change_password_flow` kiểm tra đầy đủ các ca sai mật khẩu cũ, lệch confirm, mật khẩu ngắn và đổi thành công. |
| 8 | Regression Demo 1 pass: login Student, `/dashboard`, `/api/chat`, feedback, `/materials`, `/info`, `/history`, logout; retrieval `STB-20260910-01` không bị sửa và test retrieval hiện hữu vẫn pass. | **ĐẠT** | `test_system.py` (7/7 PASS), `test_quick.py` (8/8 PASS), `evaluate.py` (Retrieval Top-1 = 100.00%). |
| 9 | Không có source/diff ngoài danh sách được phê duyệt, không thay đổi dependency/schema/AI/chatbot/retrieval, và `ANTIGRAVITY_REPORT.md` chứa lệnh test thực tế. | **ĐẠT** | Kiểm tra git status/diff: Chỉ sửa các file thuộc phạm vi phê duyệt; các thành phần AI giữ nguyên vẹn. |

---

## 7. Vấn đề còn tồn tại & Ghi chú

- **Acceptance criteria chưa đạt**: Không có (9/9 criteria đạt 100%).
- **Vấn đề còn tồn tại**: Không có lỗi phát sinh.
- **Lưu ý**:
  + Đã sao lưu database hiện tại tại `instance/studybot.db.bak`.
  + Tệp `CODEX_REVIEW.md` được giữ nguyên trạng, sẵn sàng để Codex thực hiện đánh giá độc lập.

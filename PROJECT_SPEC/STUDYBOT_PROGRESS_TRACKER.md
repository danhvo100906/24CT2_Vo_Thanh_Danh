# STUDYBOT — PROGRESS TRACKER (24CT2 – Võ Thành Danh)

> File làm việc xuyên suốt dự án. Nguồn: audit ngày 01/10/2026 từ các file .md, source, git log và 3 file DB.
> Cách dùng: tick `[x]` khi xong, đổi trạng thái ở bảng, ghi ngày vào mục **Nhật ký**. Mỗi lúc chỉ có **một task active** (theo AGENTS.md).

**Ký hiệu:** ✅ xong · 🟡 làm một phần · ⚠️ có nhưng còn sai/thiếu · ❌ chưa làm
**Mức ưu tiên:** P0 nghiêm trọng · P1 cao · P2 trung bình · P3 thấp

**Giới hạn của lần audit:** chưa chạy lại `evaluate.py` và `test_system.py` (không cài được PyTorch). Số liệu AI lấy từ `tests/evaluation_results.json` (10/09 15:45). Mục "đã kiểm chứng" nghĩa là đã chạy thử Flask trên bản sao DB thật.

---

## 1. Tóm tắt hiện trạng

**Đã chạy được**
- Đăng nhập, phân quyền Student/Admin
- 900 tài khoản theo quy tắc `KK5122NNNN`, đổi mật khẩu
- Chat phân loại 17 intent bằng PyTorch
- Tìm tài liệu cho 6 môn
- Feedback, lịch sử chat, Admin CRUD cơ bản

**Chưa có**
- Lõi học tập theo spec: hỏi đáp theo nội dung tài liệu, nguồn + ngày cập nhật, ngữ cảnh 10–15 câu, Semantic Search, PDF/RAG
- UML, báo cáo, kịch bản demo
- Hồ sơ trạng thái trong repo đã lỗi thời (CURRENT_STATUS, TASK_QUEUE, CURRENT_TASK)

---

## 2. Danh sách task 1 → 40

### Phase 1 — Ổn định nền tảng
| # | Task | TT | Ghi chú |
|---|------|----|---------|
| 1 | Kiểm tra source hiện tại | 🟡 | Audit toàn dự án (Next action của CURRENT_STATUS) chưa làm chính thức |
| 2 | Chạy web end-to-end | 🟡 | Login + 9 trang OK; chưa có test E2E trình duyệt |
| 3 | Kiểm tra database | ⚠️ | DB thật 904 user (1 admin + 903 SV), không phải 900; `Material.subject_code` không có FK sang Subject |
| 4 | Login | ⚠️ | TASK-003 có code + test nhưng chưa review; DB thật còn tài khoản mật khẩu `123456` |
| 5 | Chatbot | 🟡 | Chạy được, nhiều giới hạn (mục 5A) |
| 6 | Admin | 🟡 | CRUD cơ bản; thiếu Intent, Subject, thống kê, model |
| 7 | Test | 🟡 | Có test nhưng rò rỉ dữ liệu train/test, thiếu bao phủ |
| 8 | Sửa lỗi | ❌ | Chưa có danh sách lỗi chính thức → dùng mục 4 |

### Phase 2 — Học tập
| # | Task | TT | Ghi chú |
|---|------|----|---------|
| 9 | Hoàn thiện intent | 🟡 | 17 intent, 228 câu mẫu (7–45/intent); `hoi_kien_thuc` yếu nhất (3/8 sai) |
| 10 | Hoàn thiện tìm tài liệu | ✅/⚠️ | STB-20260910-01 APPROVED (39/39 Top-1) nhưng chỉ 6 môn, đọc từ JSON không đọc DB |
| 11 | Bổ sung tài liệu CNTT | ❌ | Chỉ 6 môn, toàn link placeholder, không có file thật/upload |
| 12 | Hỏi đáp tài liệu | ❌ | Bot chỉ trả link, không đọc nội dung |
| 13 | Fallback | 🟡 | Có 3 mức theo confidence; thiếu luồng Knowledge → tài liệu → nguồn tin cậy (spec §7) |
| 14 | Source (nguồn) | ❌ | Câu trả lời chat không kèm nguồn; chỉ `/info` hiện nguồn |
| 15 | Updated date | ❌ | Không hiển thị; ngày gốc trong JSON bị bỏ khi seed |

### Phase 3 — Context
| # | Task | TT |
|---|------|----|
| 16 | Context 10–15 câu | ❌ (client chỉ gửi `{message}`, server không dùng lịch sử) |
| 17 | Theo dõi chủ đề | ❌ |
| 18 | Đổi chủ đề | ❌ |
| 19 | Gợi ý câu hỏi tiếp theo | ❌ (nút gợi ý hiện cố định) |

### Phase 4 — Semantic Search
| # | Task | TT |
|---|------|----|
| 20 | Embedding | ❌ |
| 21 | Semantic retrieval | ❌ |
| 22 | So sánh với keyword | ❌ |
| 23 | Đánh giá | ❌ |

### Phase 5 — PDF/RAG
| # | Task | TT |
|---|------|----|
| 24 | Upload PDF | ❌ |
| 25 | Parse | ❌ |
| 26 | Chunk | ❌ |
| 27 | Embedding | ❌ |
| 28 | Vector storage | ❌ |
| 29 | Retrieval | ❌ |
| 30 | Generate answer | ❌ |
| 31 | Citation | ❌ |

### Phase 6 — Hoàn thiện
| # | Task | TT | Ghi chú |
|---|------|----|---------|
| 32 | Bảo mật | ❌ | Nhiều lỗ hổng (mục 4) |
| 33 | Logging | 🟡 | Chỉ lưu ChatMessage (intent, confidence); không có audit/error log |
| 34 | Feedback analytics | ❌ | Chỉ có % hài lòng |
| 35 | Admin dashboard | 🟡 | Thiếu phân bố intent dù CHANGELOG ghi có |
| 36 | UI | 🟡 | Chưa có trang "Thông tin sinh viên" (spec §15) |
| 37 | End-to-end test | ❌ | |
| 38 | UML | ❌ | Không có file UML nào trong repo |
| 39 | Báo cáo | ❌ | |
| 40 | Demo | ❌ | Chưa có kịch bản (spec §19) |

### Đối chiếu TASK_QUEUE (20 ô chưa tick)
- [ ] P0 "Verify authentication and authorization" → thực tế đã làm ở TASK-003, cần tick sau khi review
- [ ] P1 "Improve material retrieval" → thực tế đã xong (STB-20260910-01), cần tick
- [ ] P1 source/update metadata, fallback, learning test cases → chưa xong
- [ ] Toàn bộ P2 (context) và P3 (AI tương lai) → chưa làm

### Task trong HANDOFF
| Task | Trạng thái thực tế |
|------|--------------------|
| Demo 1 (commit 06/09) | Xong |
| STB-20260910-01 (retrieval) | APPROVED, cycle 1/3 |
| TASK-003 (login + 900 tài khoản) | Code + test xong, báo cáo COMPLETED, **chưa review**; CURRENT_TASK vẫn `READY_FOR_ANTIGRAVITY` → chưa DONE theo AGENTS.md §8 |
| TASK-001/002/004/005/006 | Không có hồ sơ trong repo; CURRENT_TASK ghi không tìm thấy TASK-006 |

---

## 3. TASK-003 đối chiếu 9 tiêu chí
| Tiêu chí | Kết quả |
|----------|---------|
| 1. Đúng 900 sinh viên | ✅ DB test · ❌ DB thật 903 SV (đã kiểm chứng) |
| 2. username = mã SV, mật khẩu hash từ mã SV | ✅ 900 tài khoản pbkdf2 |
| 3. Seed idempotent, giữ mật khẩu đã đổi, báo mismatch | ✅ nhưng điều kiện chạy seed lỗi (P1) |
| 4. 6 tài khoản biên đăng nhập được | ✅ test; thử thêm 2 tài khoản trên bản sao DB đều vào `/dashboard` |
| 5. Từ chối login sai | ✅ theo test/báo cáo (chưa chạy lại) |
| 6. Student không vào `/admin` | ✅ 403 (đã kiểm chứng) |
| 7. Đổi mật khẩu | ✅ chạy được, quy tắc còn lỏng |
| 8. Regression Demo 1 | 🟡 test không bao phủ `/materials`, `/info`, `/history` khi đã đăng nhập; kiểm tay đều 200 |
| 9. Không diff ngoài phạm vi | 🟡 không xác minh được: 28 file sửa + nhiều file chưa theo dõi, chưa commit |

---

## 4. Vấn đề của các task cũ

### P0 — Nghiêm trọng
- [ ] **P0-1 Tài khoản yếu còn hoạt động trên DB thật** (đã kiểm chứng)
  - `24ct2001`–`24ct2003` active, mật khẩu `123456`
  - Admin vẫn dùng `admin123` (còn in trong `run.py` và README)
  - Vi phạm 05-security-rules; task quy định không tự xóa → **chủ dự án cần quyết định**
- [ ] **P0-2 Chatbot không đọc database** (đã kiểm chứng bằng code)
  - `chatbot.py`, `retrieval.py` không dùng DB; học phí/quy chế/liên hệ cứng trong `intents.json`; tài liệu đọc từ `data/materials.json`
  - Admin thêm/sửa/ẩn/xóa tri thức, tài liệu không ảnh hưởng câu trả lời; CHANGELOG và spec §10 mô tả ngược lại
- [ ] **P0-3 Dữ liệu cũ/chưa xác minh trình bày như hiện hành**
  - Học phí năm 2024-2025 trong khi hôm nay 01/10/2026, không cảnh báo/nguồn/ngày
  - STK ngân hàng, SĐT phòng ban, địa điểm, URL tài liệu (vd `drive.google.com/drive/folders/dau-cnpm-slides-24ct`) không có bằng chứng
  - Vi phạm D-007, D-008, spec §9
- [ ] **P0-4 TASK-003 đã chạy trên DB thật** (seed 10/09 16:16) khi chưa được Codex review; `CODEX_REVIEW.md` và `CURRENT_TASK.md` nói về hai task khác nhau

### P1 — Cao
- [ ] **P1-1 Điều kiện seed theo số lượng, không theo tập mã** (đã kiểm chứng): chỉ seed khi tổng SV < 900; hiện 903 nên không chạy; nếu Admin xóa khiến tổng < 900 thì lần khởi động sau tạo lại toàn bộ tài khoản đã xóa (mật khẩu = mã SV)
- [ ] **P1-2 Bảo mật đăng nhập** (đã kiểm chứng)
  - Mật khẩu mặc định = mã SV, không bắt đổi lần đầu
  - Sai 30 lần vẫn đăng nhập đúng ngay sau đó (không giới hạn thử)
  - Không có CSRF (Admin POST không token vẫn được xử lý)
  - Đổi mật khẩu cho phép đặt lại mật khẩu cũ hoặc `123456`; chỉ yêu cầu ≥ 6 ký tự
  - Admin không có link đổi mật khẩu trên UI
- [ ] **P1-3 Lỗi dữ liệu hiển thị** (đã kiểm chứng)
  - `/info` hiện "Thời hạn nộp học phí: 0 VNĐ" và "Phương thức nộp học phí: 0 VNĐ" (seed ép mọi mục thành dạng tiền)
  - `updated_at` trong DB là ngày seed (09/09/2026), không phải ngày hiệu lực thật (2024); trường `updated_at` trong JSON bị bỏ qua; `/info` không hiện ngày
- [ ] **P1-4 Retrain** (theo code)
  - Model nạp một lần khi import → retrain xong vẫn dùng model cũ đến khi restart
  - Chạy đồng bộ trong request, không đặt seed, không lưu phiên bản/metrics, không backup model cũ, không đánh giá sau retrain
- [ ] **P1-5 Đánh giá AI có rò rỉ dữ liệu**
  - 30/30 câu out-of-scope trùng nguyên văn câu huấn luyện; 25/106 câu intent trùng
  - Rejection chỉ đạt 83,33% và còn tính fallback là thành công → cao hơn thực tế
- [ ] **P1-6 Số liệu và tài liệu lệch nhau**
  - README ghi 95,28% / 63,33%; kết quả mới nhất 96,23% / 83,33%
  - README vẫn hướng dẫn `24ct2001/123456`; CHANGELOG ghi ngày 2025-09-09
  - CURRENT_STATUS vẫn ghi "login is planned"; TASK_QUEUE chưa tick; DECISIONS chưa có quyết định cho TASK-003
- [ ] **P1-7 Git:** HEAD là commit 06/09; 28 file sửa (+3.126/−640) + nhiều file mới chưa commit → rollback "revert diff TASK-003" trong CODEX_PLAN không thực hiện được
- [ ] **P1-8 Hai bản MASTER spec khác nhau:** bản root có §3.2–13 (đặc tả 900 tài khoản, chỉ dẫn "Codex phải…", đánh số mục lặp), bản `PROJECT_SPEC/` không có; AGENTS.md yêu cầu ghi nhận xung đột và dừng nhưng chưa có quyết định chốt

### P2 — Trung bình
- [ ] Báo cáo Antigravity ghi scrypt nhưng code dùng `pbkdf2:260000` (comment lại nhắc bcrypt)
- [ ] Hai nguồn dữ liệu lệch nhau (phòng Đào tạo "Khu Hiệu bộ" vs "Nhà Hiệu bộ"; liên hệ thiếu SĐT 2 phòng)
- [ ] `data/` và `framework/src/data/` là hai bản sao giống hệt, dễ lệch
- [ ] Intent `lop_24ct2` ghi cứng "Ngành Công nghệ Phần mềm / CNTT" chưa xác minh
- [ ] Tiếng Anh chỉ ở mức chào hỏi/cảm ơn/trợ giúp (3 câu test); chỉ 5 câu không dấu, chưa có bộ test sai chính tả/gần nghĩa (spec §18)
- [ ] Admin sửa mã SV đổi luôn username nhưng không kiểm tra trùng → có thể lỗi 500
- [ ] Bộ test chạy rất chậm (245 s và 122 s) do seed 900 tài khoản nhiều lần trong `setUp`
- [ ] Bộ render Markdown tự viết trong giao diện chat xử lý danh sách chưa chuẩn (regex gói cả đoạn giữa các `<li>`)

### P3 — Thấp
- [ ] Mã cũ còn sót: `framework/src/database/db.py` (không dùng), `instance/chatbot.db`, `calculate_grade` trong `processing/__init__.py`, `process_student_data` trong `routes.py`, `__pycache__`
- [ ] `requirements.txt` không ghim phiên bản; có `nltk` nhưng không dùng
- [ ] `SECRET_KEY` mặc định cứng trong code; `.env.example` không được nạp (thiếu `python-dotenv`); `run.py` bật `debug=True`
- [ ] API cũ: `datetime.utcnow()`, `Query.get()`

---

## 5. Các phần chưa hoàn thiện (checklist đầy đủ)

### A. AI và chatbot
- [ ] Ngữ cảnh 10–15 câu; nhận biết câu hỏi nối tiếp; phát hiện đổi chủ đề; gợi ý câu tiếp theo theo ngữ cảnh
- [ ] Hỏi đáp kiến thức CNTT thật (hiện `hoi_kien_thuc` chỉ 4 khái niệm cố định: ML, OOP, chuẩn hóa CSDL, OSI); giải thích sâu, bài tập
- [ ] Hỏi đáp dựa trên nội dung tài liệu
- [ ] Nguồn, ngày cập nhật, trạng thái hiệu lực, cảnh báo dữ liệu cũ trong câu trả lời
- [ ] Luồng fallback đầy đủ theo spec §7
- [ ] Cải thiện OOV/OOS, confidence threshold; sai chính tả, câu gần nghĩa
- [ ] Semantic Search, embedding, PDF/RAG, vector DB, reranking, citation
- [ ] Cá nhân hóa theo khóa/ngành suy ra từ mã SV (spec §4, demo §19)

### B. Dữ liệu
- [ ] Danh sách tài liệu thật + nguồn hợp pháp; môn học ưu tiên
- [ ] Xác minh học phí, quy định, thủ tục, liên hệ, STK, URL
- [ ] Trạng thái hiệu lực và ngày hết hạn cho dữ liệu hay thay đổi
- [ ] Một nguồn dữ liệu duy nhất (DB) cho cả bot và Admin
- [ ] Mở rộng ngoài 6 môn và ngoài 24CT2

### C. Admin
- [ ] Quản lý Intent (thêm/sửa câu mẫu, câu trả lời) + quy trình retrain và kiểm thử lại
- [ ] Quản lý Môn học (hiện chỉ seed, không có UI)
- [ ] Sửa Tài liệu và Tri thức (hiện chỉ thêm, ẩn/hiện, xóa; tri thức không có active/inactive)
- [ ] Upload PDF/DOCX; form nhập tài liệu đầy đủ
- [ ] Trang Feedback riêng (hiện không xem được comment; UI sinh viên cũng không gửi comment)
- [ ] Thống kê: phân bố intent, intent hay sai, câu không nhận diện, chủ đề hỏi nhiều, xu hướng theo thời gian (tỷ lệ hài lòng đang mặc định 100% khi chưa có feedback)
- [ ] Quản lý model/retrain: phiên bản, ngày huấn luyện, metrics, log, tải lại model
- [ ] Phân trang và lọc (trang SV nạp cả 903 dòng; nhật ký chỉ lấy 200 dòng gần nhất)

### D. Sinh viên
- [ ] Trang "Thông tin sinh viên" (spec §15; "Thông tin" hiện chỉ là tri thức của trường)
- [ ] Nạp lại lịch sử vào khung chat; tìm kiếm/xóa lịch sử

### E. Bảo mật và vận hành
- [ ] Xử lý 4 điểm P0 và các điểm P1 bảo mật: giới hạn đăng nhập sai, CSRF, ép đổi mật khẩu lần đầu, mật khẩu mạnh hơn
- [ ] Đưa bí mật cấu hình ra khỏi code, tắt debug khi triển khai, cookie an toàn
- [ ] Quy tắc bảo mật dữ liệu cá nhân/SV dùng cho cá nhân hóa (spec §27, mục 6–7)

### F. Kiểm thử và chất lượng
- [ ] Tách tập test khỏi tập huấn luyện; seed cố định khi huấn luyện
- [ ] Test Chatbot (câu nối tiếp, đổi chủ đề, không có dữ liệu, câu cần nguồn)
- [ ] Test Web (đã đăng nhập vào các trang SV, CRUD Admin đầy đủ, upload)
- [ ] Test Database (PK/FK, dữ liệu sai/thiếu)
- [ ] Bộ test chuẩn so sánh sau mỗi lần đổi model (spec §27, mục 8) + tiêu chí định lượng "đúng trọng tâm" (mục 9)

### G. Tài liệu và đồ án
- [ ] 5 sơ đồ UML: Use Case, Class, Activity, Sequence, ERD (phản ánh đúng source)
- [ ] Báo cáo; kịch bản demo
- [ ] Cập nhật CURRENT_STATUS, TASK_QUEUE, DECISIONS, README, CHANGELOG
- [ ] Chốt 10 quyết định còn mở ở spec §27

---

## 6. Thứ tự làm đề xuất
*(Đề xuất, chưa được chủ dự án phê duyệt. Mỗi lúc chỉ một task active.)*

1. **Đóng TASK-003**
   - [ ] Cho Codex review thật
   - [ ] Quyết định số phận 3 tài khoản cũ và `admin123`
   - [ ] Sửa điều kiện seed theo tập mã
   - [ ] Commit riêng
   - [ ] Cập nhật CURRENT_STATUS, TASK_QUEUE, DECISIONS
2. **Dữ liệu có nguồn và ngày, một nguồn duy nhất**
   - [ ] Sửa lỗi "0 VNĐ", giữ `updated_at` thật
   - [ ] Bot đọc từ DB
   - [ ] Hiển thị nguồn, ngày, cảnh báo dữ liệu cũ
   - (Khoảng cách lớn nhất so với thứ tự ưu tiên spec §20, mục 4–5)
3. **Ngữ cảnh 10–15 câu** (Phase 3)
4. **Tài liệu thật + hỏi đáp tài liệu**, rồi Semantic Search và RAG
5. **Tách bộ test, ghi metrics mỗi lần retrain, mở rộng test**
6. **UML, báo cáo, demo** (làm song song để kịp mốc nộp)

---

## 7. Quyết định chờ chủ dự án
- [ ] Xử lý 3 tài khoản `24ct2001–24ct2003` (xóa / vô hiệu hóa / giữ)
- [ ] Đổi mật khẩu admin và bỏ `admin123` khỏi `run.py`, README
- [ ] Chọn bản MASTER spec chuẩn (root hay `PROJECT_SPEC/`)
- [ ] Nguồn dữ liệu chuẩn cho học phí, liên hệ, quy chế
- [ ] Danh sách tài liệu thật và môn ưu tiên
- [ ] Mốc nộp / demo

---

## 8. Nhật ký tiến độ
| Ngày | Task | Việc đã làm | Kết quả / Ghi chú |
|------|------|-------------|-------------------|
| 01/10/2026 | Audit | Kiểm tra tổng thể, tạo file này | Xác định 4 P0, 8 P1 |
| | | | |

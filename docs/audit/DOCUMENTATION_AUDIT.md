# Documentation Audit

## 1. Audit Information
- **Task:** P0-003 — Documentation Audit
- **Date:** 2026-10-01
- **Auditor:** Antigravity

## 2. Documentation Inventory
Các tài liệu hiện có trong dự án:
- `README.md`
- `README_V2.md`
- `CHANGELOG.md`
- `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (Thư mục gốc)
- `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (Roadmap 27 Phases)
- `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`
- `PROJECT_SPEC/CURRENT_STATUS.md`
- `PROJECT_SPEC/TASK_QUEUE.md`
- `PROJECT_SPEC/ROADMAP.md`
- `PROJECT_SPEC/DECISIONS.md`
- `PROJECT_SPEC/STUDYBOT_PROGRESS_TRACKER.md`
- Các tài liệu Handoff trong `PROJECT_SPEC/HANDOFF/`
- Audit Evidence (`docs/audit/`, `docs/evidence/`)
- Quy tắc Agent trong `.agents/rules/`

## 3. README Audit
- **Tên dự án:** Phù hợp.
- **Mục tiêu, Phạm vi:** Phù hợp.
- **Công nghệ (Flask, PyTorch):** Phù hợp.
- **Đánh giá AI Thực tế:** **OUTDATED**. README ghi Accuracy 95.28% và Rejection 63.33%, thực tế hiện nay là 96.23% và 83.33%.
- **Tài khoản Mặc định:** **OUTDATED / INCORRECT**. Vẫn ghi hướng dẫn dùng `24ct2001/123456`. Thực tế đã seed 900 tài khoản mã `KK5122NNNN`. Đăng nhập Admin vẫn để `admin123`.

## 4. Master Specification Audit
- **Trạng thái:** **CONFLICT — NEEDS DECISION**.
- Tồn tại 2 bản Master Spec:
  1. `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (tại thư mục gốc).
  2. `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`.
- Bản gốc (root) có quy định chi tiết về 900 tài khoản, trong khi bản trong `PROJECT_SPEC/` không có phần này.

## 5. Current Status Audit
- **Trạng thái:** **OUTDATED / CONFLICT**.
- `PROJECT_SPEC/CURRENT_STATUS.md` ghi nhận "Student login is planned around student ID", trong khi thực tế code đã hoàn thành seed và login qua 900 accounts. 
- Mục Context Target ghi 10-15 câu nhưng chưa được code thực tế.

## 6. Task Queue Audit
- **Trạng thái:** **OUTDATED / CONFLICT**.
- Chia theo cấu trúc `P0, P1, P2, P3` nhưng không theo dõi sát các mã Task (ví dụ TASK-003 không được tick). Không đồng bộ với roadmap 27 phases.

## 7. Roadmap Audit
- **Trạng thái:** **CONFLICT — NEEDS DECISION**.
- Có đến 4 cách chia Roadmap đang tồn tại song song:
  1. File `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md`: Roadmap cực kỳ chi tiết 27 phases (Phase 0 -> Phase 27).
  2. `MASTER_PROJECT_SPECIFICATION.md`: Chia theo Giai đoạn (Phase 1 -> Phase 6).
  3. `TASK_QUEUE.md`: Phân chia theo P0, P1, P2, P3.
  4. `ROADMAP.md`: Phân chia theo `Now`, `Next`, `Later`.

## 8. Architecture Documentation Audit
- **Trạng thái:** **MISSING / CONFLICT**.
- Hệ thống bị duplicate entrypoint (`run.py` và `app/main.py`) và thư mục `data/` so với `framework/src/data/`, cũng như code database legacy `framework/src/database/db.py`. Tuy nhiên chưa có tài liệu Architecture chính thức nào ghi nhận cấu trúc thực tế này để dọn dẹp.

## 9. Database Documentation Audit
- **Trạng thái:** **MATCH (một phần)**.
- Đề cập dùng SQLite và SQLAlchemy trong Spec, đúng với code `instance/studybot.db`. Tuy nhiên không nhắc đến file DB dư thừa `chatbot.db`.

## 10. Student Account Documentation Audit
- **Trạng thái:** **OUTDATED / CONFLICT**.
- Theo `CURRENT_TASK.md` (TASK-003) và Spec gốc, đã có yêu cầu triển khai đúng 900 accounts format `2451220001–2451220300`. Nhưng README và `CURRENT_STATUS.md` chưa cập nhật điều kiện này. 

## 11. Chatbot Documentation Audit
- **Trạng thái:** **MATCH**.
- `MASTER_PROJECT_SPECIFICATION.md` mô tả rõ AI hiện tại dùng PyTorch, BoW, Neural Network, Intent. Chưa có Context (đang hướng phát triển). Trùng khớp với code thực tế.

## 12. Document/RAG Documentation Audit
- **Trạng thái:** **MATCH**.
- Tất cả Spec và Roadmap đều ghi nhận RAG (PDF, Vector Store, Embedding, Semantic Search) nằm ở Phase 3/4 hoặc Later (Chưa triển khai). Code thực tế đúng là chưa có RAG.

## 13. Evidence Audit
- Thư mục `docs/evidence/` đã có `P0-001.md` và `P0-002.md`.
- Các file này ghi nhận đầy đủ task, command, findings, changed files và có status `DONE`. **MATCH**.

## 14. Documentation vs Source Conflicts

| ID | Document | Source | Conflict | Severity |
|----|----------|--------|----------|----------|
| 1 | `README.md` | `app/student_accounts.py` | README hướng dẫn dùng `24ct2001/123456`, source sinh 900 user với mã `KK5122NNNN`. | HIGH |
| 2 | `CURRENT_STATUS.md` | `app/auth.py` | Báo cáo login "is planned", source đã hoàn thành. | MEDIUM |
| 3 | Roadmap Docs | Roadmap Docs | Tồn tại 4 bản quy hoạch Roadmap mâu thuẫn nhau về cấu trúc chia phase. | CRITICAL |
| 4 | Master Spec | Master Spec | Tồn tại 2 bản Master Spec (root vs `PROJECT_SPEC/`) lệch nội dung về 900 account. | CRITICAL |
| 5 | `CHANGELOG.md` | `data/` vs `framework/` | CHANGELOG không ghi nhận sự tồn tại của việc duplicate cấu trúc data và entrypoint. | LOW |

## 15. Missing Documentation
- **Architecture Documentation:** Sơ đồ luồng dữ liệu (Flowchart, Sequence Diagram) kết nối Web và AI Model.
- **API Documentation:** Đặc tả request/response cho `/api/chat` và `/api/feedback`.
- **Database Schema (ERD):** Sơ đồ quan hệ bảng.

## 16. Outdated Documentation
- `README.md` (Sai thông tin account test, số liệu AI, cần cập nhật).
- `PROJECT_SPEC/CURRENT_STATUS.md` (Status tiến độ lệch với thực tế code).
- `PROJECT_SPEC/TASK_QUEUE.md` (Lệch với hệ thống 27 phases hiện hành).

## 17. Risks
- Mâu thuẫn giữa 2 bản Master Spec gây bối rối cho việc phát triển tiếp theo.
- Kế hoạch Roadmap phân mảnh làm Agent không biết bám theo tài liệu nào để chọn Phase kế tiếp.
- Dữ liệu Test User trong README gây rủi ro người dùng/tester không đăng nhập được.

## 18. Recommended Documentation Work
- Hợp nhất `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` và `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`.
- Chốt lại dùng `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` làm Roadmap duy nhất và xóa `ROADMAP.md`, `TASK_QUEUE.md` hoặc quy hoạch lại.
- Cập nhật lại `README.md` và `CURRENT_STATUS.md` theo thực tế code.

## 19. Next Task
P1-001 — Architecture Documentation

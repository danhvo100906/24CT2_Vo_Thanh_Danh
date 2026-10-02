# Spec & Roadmap Consolidation Audit

## 1. Documents Found

**Master Specifications:**
- `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root)
- `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`

**Roadmaps / Plans:**
- `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (root)
- `PROJECT_SPEC/ROADMAP.md`
- `PROJECT_SPEC/TASK_QUEUE.md`
- `PROJECT_SPEC/CURRENT_STATUS.md`

## 2. Master Spec Comparison

| Document | Path | Version/Date | Scope | 900 Accounts | Roadmap | Status |
| -------- | ---- | ------------ | ----- | ------------ | ------- | ------ |
| Master Spec (Root) | `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` | 1.0 (10/09/2026) | CNTT DAU | CÓ (Rất chi tiết ở mục 3.2-13, mã `KK5122NNNN`) | 6 Phases | CANDIDATE FOR OFFICIAL SOURCE |
| Master Spec (Inner) | `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` | 1.0 (10/09/2026) | CNTT DAU | KHÔNG (Chỉ ghi chung chung khóa 24-26) | 6 Phases | LEGACY |

## 3. Roadmap Comparison

| Document | Path | Phân chia Phase | Task List | Điểm khác với 27 Phase | Status |
| -------- | ---- | --------------- | --------- | ---------------------- | ------ |
| Roadmap 27 Phases | `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` | 28 Phases (0-27) | 89 tasks (P0-001 -> P26-004) | Bản thân nó là hệ quy chiếu gốc. Rất chi tiết và chia nhỏ từng bước từ Audit đến Release. | CANDIDATE FOR OFFICIAL SOURCE |
| Roadmap (Inner) | `PROJECT_SPEC/ROADMAP.md` | 3 mức (Now, Next, Later) | ~10 gạch đầu dòng | Dạng văn xuôi, không có Task ID rõ ràng, định hướng chung chung. | LEGACY |
| Task Queue | `PROJECT_SPEC/TASK_QUEUE.md` | 4 mức (P0, P1, P2, P3) | ~20 checklist items | Phân loại theo mức độ ưu tiên của module AI, không đánh mã task định danh. | LEGACY |
| Current Status | `PROJECT_SPEC/CURRENT_STATUS.md` | Không chia phase | Không có | Lạc hậu so với thực tế (ghi login is planned). | LEGACY |

## 4. Task List Comparison
- **Kế hoạch 27 Phases:** Định nghĩa chính xác 89 tasks từ `P0-001` đến `P26-004`.
- **Task Queue:** Định nghĩa khoảng 20 tasks dưới định dạng checklist `[ ]`. Các Task P0 ở đây là kiểm tra hệ thống hiện tại, nhưng tên gọi trùng lặp (ví dụ P0, P1) với tiền tố của 89 tasks kia gây nhầm lẫn.

## 5. 900 Account Requirement Comparison
- **Master Spec (Root):** Đặc tả rất rõ ràng cách sinh 900 tài khoản cho 3 khóa (24, 25, 26) ngành CNTT (5122). Format `KK5122NNNN`.
- **Master Spec (Inner):** Bỏ sót hoàn toàn các đoạn văn này.
- **Kế hoạch 27 Phases:** Nhắc đến việc cần có "900 tài khoản sinh viên" tại Phase 0.

## 6. AI/RAG Requirement Comparison
Tất cả các tài liệu đều thống nhất kiến trúc AI:
- **Hiện tại:** PyTorch + Bag of Words + Neural Network + Intent Classification.
- **Tương lai (Phases tiếp theo):** Context (10-15 câu) -> Embedding -> Semantic Search -> Vector Store -> PDF/RAG -> Advanced RAG.

## 7. Critical Conflicts

| ID | File A | File B | Nội dung khác nhau | Mức độ |
| -- | ------ | ------ | ------------------ | ------ |
| 1 | `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` | `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` | File ở root chứa đặc tả chi tiết tạo 900 accounts (mục 3.2-13). File trong thư mục `PROJECT_SPEC` không hề có phần này. | CRITICAL |
| 2 | `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` | `PROJECT_SPEC/TASK_QUEUE.md` | Bản Kế hoạch 27 phases phân chia 89 tasks (P0-001 -> P26-004). Task Queue cũ phân 4 level (P0-P3) và không có mã ID định danh, gây xung đột tên gọi P0, P1. | CRITICAL |
| 3 | `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` | `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` | Mục 25 của Master Spec định nghĩa lộ trình 6 Phases. Bản Kế hoạch định nghĩa lộ trình 28 Phases (0-27). | HIGH |

## 8. Candidate Official Documents
- **Master Specification:** `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root) - Vì chứa đủ yêu cầu 900 accounts.
- **Roadmap / Task Plan:** `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (root) - Vì bao phủ được 89 tasks chi tiết.

## 9. Documents That Appear Legacy
- `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`
- `PROJECT_SPEC/ROADMAP.md`
- `PROJECT_SPEC/TASK_QUEUE.md`
- `PROJECT_SPEC/CURRENT_STATUS.md`

## 10. Items Requiring User Decision
1. Hợp nhất `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root) vào trong `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` hay xóa bản bên trong?
2. Hợp nhất `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` làm file Roadmap/Task Queue duy nhất và xóa `ROADMAP.md`, `TASK_QUEUE.md`?
3. Sửa đổi Section 25 trong Master Spec (6 phases) để đồng bộ với 27 phases hay để nguyên làm "High-level Roadmap"?

## 11. Recommended Consolidation Plan
- Lấy `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root) làm Master Spec chính thức, chuyển vào `PROJECT_SPEC/` và chép đè bản cũ.
- Lấy `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` chuyển vào `PROJECT_SPEC/` đổi tên thành `ROADMAP_27_PHASES.md` và dùng làm nguồn duy nhất quản lý tiến độ task.
- Xóa các file rác: `PROJECT_SPEC/ROADMAP.md`, `PROJECT_SPEC/TASK_QUEUE.md`.
- Cập nhật lại `PROJECT_SPEC/CURRENT_STATUS.md` theo kết quả P0-001/P0-002/P0-003.

---

## Post-Consolidation Resolution

> **LƯU Ý QUAN TRỌNG:** Audit từ Mục 1 đến Mục 11 ở trên là kết quả kiểm tra **TRƯỚC KHI** thực hiện Documentation Consolidation task. Các kết luận `CRITICAL`, `LEGACY`, conflict được ghi nhận trong audit này **phản ánh trạng thái PRE-CONSOLIDATION**, không phải trạng thái hiện tại của dự án.

### Bối cảnh

Audit này được thực hiện tại task `P0-003 — Kiểm tra và thống nhất tài liệu` nhằm xác định các conflict trước khi tiến hành hợp nhất. Mọi kết luận CRITICAL trong phần audit gốc phải được hiểu là trạng thái tại thời điểm kiểm tra, không phải trạng thái hiện hành.

### Kết quả Sau Documentation Consolidation

Sau khi hoàn thành Documentation Consolidation task:

| Vấn đề (PRE-CONSOLIDATION) | Trạng thái Hiện Tại (POST-CONSOLIDATION) |
| --------------------------- | ---------------------------------------- |
| `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` thiếu requirement 900 accounts | **ĐÃ ĐỒNG BỘ** — Nội dung đã được đồng bộ từ bản gốc ở root, bao gồm đầy đủ yêu cầu 900 accounts (KK5122NNNN, khóa 24/25/26, ngành 5122) |
| `PROJECT_SPEC/ROADMAP.md` có định dạng "Now/Next/Later", không có Task ID | **ĐÃ ĐỒNG BỘ** — Nội dung đã được đồng bộ từ bản Kế hoạch 27 Phases/89 Tasks gốc ở root |
| `PROJECT_SPEC/TASK_QUEUE.md` dùng 4 mức P0–P3 không có mã Task ID | **ĐÃ CẬP NHẬT** — Task Queue đã tham chiếu đến roadmap chuẩn 27 Phases/89 Tasks; trạng thái P0-001, P0-002, P0-003, Documentation Consolidation đã được đánh dấu DONE |
| `PROJECT_SPEC/CURRENT_STATUS.md` lạc hậu | **ĐÃ CẬP NHẬT** — Phản ánh tiến độ thực tế, không bịa trạng thái cho RAG/Context |
| Conflict ID-1 CRITICAL: Inner spec thiếu 900 accounts | **ĐÃ GIẢI QUYẾT** |
| Conflict ID-2 CRITICAL: Task Queue conflict tên P0/P1 với 89 Tasks | **ĐÃ GIẢI QUYẾT** |
| Conflict ID-3 HIGH: Master Spec 6 phases vs Roadmap 27 phases | **ĐÃ GHI NHẬN** — Bản gốc `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root) vẫn có Section 25 nói đến "6 Phases" ở mức high-level; roadmap vận hành chính thức là 27 Phases/89 Tasks trong file `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` |

### Requirement Verification (POST-CONSOLIDATION)

- **900 accounts:** ✅ Được bảo toàn — 3 khóa (24, 25, 26), mã ngành 5122, serial 0001–0300, format `KK5122NNNN`.
- **27 Phases / 89 Tasks:** ✅ Được bảo toàn — Roadmap chính thức vẫn là `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` với 27 Phases (P0–P26), 89 Tasks.
- **Official Roadmap count:** Roadmap thực tế có 27 phases (đánh số Phase 0 đến Phase 26). Mô tả "28 Phases (0-27)" trong bảng Mục 3 là do cách đếm phase 0 — ký hiệu chính xác là **27 Phases / 89 Tasks**.
- **PyTorch + BoW + Neural Network + Intent Classification:** ✅ Được bảo lưu làm AI hiện hành.
- **Student/Admin:** ✅ Được bảo lưu.

### Git Baseline Limitation

Không có clean commit boundary cho Documentation Consolidation task. Các thay đổi source code quan sát được trong working tree (`app/`, `framework/`, v.v.) là các thay đổi tracked từ trước, không thể chứng minh thuộc hay không thuộc Documentation Consolidation. Documentation Consolidation task **không có chủ đích sửa source code**; các changes source code đó tồn tại trước task này.

### Ngày Cập Nhật Post-Consolidation Resolution

2026-10-01 — Antigravity, Documentation Consolidation Review Fix task.

# Evidence — Spec & Roadmap Consolidation Audit

## Task
SPEC & ROADMAP CONSOLIDATION AUDIT

## Files Inspected
- `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root)
- `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md`
- `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (root)
- `PROJECT_SPEC/ROADMAP.md`
- `PROJECT_SPEC/TASK_QUEUE.md`
- `PROJECT_SPEC/CURRENT_STATUS.md`
- `README_V2.md`

## Commands Executed
- So sánh nội dung `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` và `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` (sử dụng PowerShell `Compare-Object` và đọc trực tiếp nội dung).
- Dùng `Select-String` và Regex (`^## P\d+-\d+`) đếm số lượng tasks trong `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (Kết quả: 89 tasks từ P0-001 đến P26-004).

## Findings
- Repo đang chứa nhiều phiên bản tài liệu mô tả cùng một nội dung nhưng có độ chi tiết và cấu trúc khác nhau.
- Bản `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` ở root là bản đầy đủ nhất về logic nghiệp vụ (đặc biệt là mục 3.2-13 quy định cách tạo 900 accounts).
- Bản `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` là bản chi tiết nhất về lộ trình phát triển (với 28 phases và 89 tasks cụ thể).

## Conflicts
- **CRITICAL**: `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (root) có mục 3.2-13 yêu cầu chi tiết 900 accounts, trong khi `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` bỏ quên hoàn toàn phần này.
- **CRITICAL**: `PROJECT_SPEC/TASK_QUEUE.md` sử dụng định dạng phase P0, P1, P2, P3 xung đột tên gọi trực tiếp với 89 Tasks (P0-001, P1-001) trong Kế hoạch 27 phases.
- **HIGH**: Master Spec định nghĩa lộ trình làm 6 giai đoạn, khác hoàn toàn với Roadmap 28 giai đoạn (0-27).

## Candidate Official Documents
- **Official Master Spec:** `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md`
- **Official Roadmap:** `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md`

## Changed Files
- `docs/audit/SPEC_ROADMAP_CONSOLIDATION_AUDIT.md` (Tạo mới)
- `docs/evidence/SPEC_ROADMAP_CONSOLIDATION.md` (Tạo mới)

## Status
DONE

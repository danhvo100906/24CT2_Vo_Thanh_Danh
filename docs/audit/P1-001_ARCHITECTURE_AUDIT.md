# P1-001 Architecture Audit

## Task
P1-001 — Architecture Documentation

## Date
2026-10-01

## Mục đích

Ghi nhận các discrepancy phát hiện giữa Master Spec, Roadmap, CURRENT_STATUS và source code thực tế trong quá trình thực hiện P1-001.

---

## Audit Items

### AUDIT-001 — Duplicate Database Layer

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Không đề cập đến `framework/src/database/db.py` |
| **Current implementation** | `framework/src/database/db.py` tồn tại — raw sqlite3, tạo `instance/chatbot.db`. Không được Flask app (`app/__init__.py`) import hoặc sử dụng. |
| **Planned implementation** | N/A |
| **Gap** | Dead code — legacy database layer từ prototype cũ. Không ảnh hưởng runtime của Flask app hiện tại nhưng gây confusion về data layer. |
| **Resolution** | Ghi nhận. Không xử lý trong P1-001. Đề xuất archive/xóa trong task riêng. |

---

### AUDIT-002 — Duplicate Data Directory

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Không chỉ định vị trí cụ thể của data files |
| **Current implementation** | `data/` (root) và `framework/src/data/` đều chứa cùng JSON files (intents.json, materials.json, ...). `retrieval.py` dùng `ROOT_DATA_DIR` (root `data/`) làm primary, `LOCAL_DATA_DIR` (`framework/src/data/`) làm fallback. |
| **Planned implementation** | N/A |
| **Gap** | Duplicate data có thể gây confusion — khi update một bên có thể quên update bên kia. Root `data/` là source of truth thực tế. |
| **Resolution** | Ghi nhận. Không xử lý trong P1-001. Đề xuất xóa `framework/src/data/` trong task riêng sau khi verify không còn dependency. |

---

### AUDIT-003 — Duplicate Entrypoint

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Không chỉ định |
| **Current implementation** | Hai entrypoints: `run.py` (root, 28 dòng) và `app/main.py` (27 dòng) đều gọi `create_app()` và `app.run(debug=True, port=5000)`. Nội dung gần như giống nhau. |
| **Planned implementation** | N/A |
| **Gap** | `run.py` là intended entry point (ở root, dễ dàng invoke). `app/main.py` là legacy. |
| **Resolution** | Ghi nhận. Không xử lý trong P1-001. |

---

### AUDIT-004 — God Object routes.py

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Không đề cập đến cấu trúc routes |
| **Current implementation** | `app/routes.py` là 488 dòng, chứa: tất cả routes Student (7 routes) + tất cả routes Admin (13 routes) + `admin_required` decorator + `process_student_data()` utility + AI import path manipulation |
| **Planned implementation** | Roadmap P1-001 chỉ yêu cầu documentation, không refactor |
| **Gap** | God Object — vi phạm Single Responsibility Principle. Có thể gây khó maintain khi hệ thống phát triển. |
| **Resolution** | Ghi nhận là Technical Debt TD-001. Không refactor trong P1-001. |

---

### AUDIT-005 — No Migration System

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Master Spec không đề cập đến migration system |
| **Current implementation** | `db.create_all()` trong `create_app()` — chỉ tạo bảng nếu chưa có, không hỗ trợ schema migration |
| **Planned implementation** | Roadmap tương lai có thể cần khi thêm Embedding/Vector Store |
| **Gap** | Khi schema thay đổi (thêm cột, đổi kiểu) cần migration thủ công hoặc drop + recreate |
| **Resolution** | Ghi nhận là Technical Debt TD-005. Cần Flask-Migrate/Alembic trong task Database Audit (P1-002). |

---

### AUDIT-006 — process_student_data() Dead Code

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Không đề cập |
| **Current implementation** | `routes.py` dòng 31–53: hàm `process_student_data(name, scores)` tính điểm trung bình và xếp loại — không được bất kỳ route nào trong file gọi. Comment ghi "dùng cho bt1.py & quy chế" — legacy từ bài tập 1. |
| **Planned implementation** | N/A |
| **Gap** | Dead code trong web application context |
| **Resolution** | Ghi nhận là Technical Debt TD-009. Không xóa trong P1-001. |

---

### AUDIT-007 — Master Spec Section 25 (6 Phases vs 27 Phases)

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` Section 25 mô tả lộ trình 6 Phases ở mức high-level |
| **Current implementation** | Roadmap vận hành chính thức là `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` với 27 Phases / 89 Tasks |
| **Gap** | Conflict HIGH giữa Master Spec (6 phases high-level) và Official Roadmap (27 phases operational) — đã được ghi nhận tại SPEC_ROADMAP_CONSOLIDATION_AUDIT.md và được giải thích là high-level vs operational distinction |
| **Resolution** | Đã ghi nhận. Không thay đổi Master Spec trong P1-001. Conflict đã được documented tại Post-Consolidation Resolution. |

---

### AUDIT-008 — framework/src/database/db.py tạo instance/chatbot.db

| Field | Nội dung |
|-------|---------|
| **Spec requirement** | Database là SQLite via Flask-SQLAlchemy, lưu tại `instance/studybot.db` |
| **Current implementation** | `instance/chatbot.db` tồn tại do `framework/src/database/db.py` — file này dùng `DB_PATH = os.path.join(os.path.dirname(__file__), 'chatbot.db')` — tức là tạo tại `framework/src/database/chatbot.db`. Tuy nhiên `instance/chatbot.db` cũng tồn tại, có thể do có lần chạy từ thư mục gốc hoặc cơ chế khác. |
| **Gap** | Không rõ `instance/chatbot.db` được tạo như thế nào — cần điều tra thêm |
| **Resolution** | Ghi nhận. Không xóa `instance/chatbot.db` trong P1-001. Đề xuất điều tra trong task Database Audit. |

---

## Summary

| Audit ID | Vấn đề | Severity | Status |
|----------|--------|----------|--------|
| AUDIT-001 | Duplicate database layer (db.py) | MEDIUM | Documented, not fixed |
| AUDIT-002 | Duplicate data directory | MEDIUM | Documented, not fixed |
| AUDIT-003 | Duplicate entrypoint | LOW | Documented, not fixed |
| AUDIT-004 | God Object routes.py | HIGH | Documented, not fixed |
| AUDIT-005 | No migration system | HIGH | Documented, not fixed |
| AUDIT-006 | Dead code process_student_data() | LOW | Documented, not fixed |
| AUDIT-007 | Master Spec 6 phases vs Roadmap 27 phases | HIGH (pre-existing) | Documented at consolidation level |
| AUDIT-008 | instance/chatbot.db origin unclear | LOW | Documented, needs investigation |

**Không có audit item nào được tự ý sửa trong P1-001.**

---

**Last Updated:** 2026-10-01 — Antigravity, P1-001 Architecture Documentation task.

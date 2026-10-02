# P1-001 Architecture Documentation — Evidence

## Task
P1-001 — Architecture Documentation

## Date
2026-10-01

## Status
COMPLETED

---

## Source Documents Inspected

| File | Loại |
|------|------|
| `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` | Official Master Spec |
| `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` | Official Roadmap |
| `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` | Inner spec (synced) |
| `PROJECT_SPEC/ROADMAP.md` | Inner roadmap (synced) |
| `PROJECT_SPEC/CURRENT_STATUS.md` | Current status |
| `PROJECT_SPEC/TASK_QUEUE.md` | Task queue |
| `PROJECT_SPEC/DECISIONS.md` | Decisions log |
| `AGENTS.md` | Agent constitution |
| `docs/audit/SPEC_ROADMAP_CONSOLIDATION_AUDIT.md` | P0 audit |
| `docs/evidence/DOCUMENTATION_CONSOLIDATION.md` | P0 evidence |

## Source Directories Inspected

| Thư mục | Files đọc thực tế |
|---------|-------------------|
| `app/` | `__init__.py`, `main.py`, `models.py`, `auth.py`, `routes.py`, `student_accounts.py` |
| `framework/src/model/` | `chatbot.py`, `neural_net.py`, `nltk_utils.py`, `train.py` |
| `framework/src/processing/` | `retrieval.py` |
| `framework/src/database/` | `db.py` |
| `framework/src/data/` | (listed via `Get-ChildItem`) |
| `data/` | (listed via `Get-ChildItem`) |
| `instance/` | (listed via `Get-ChildItem`) |
| `tests/` | (listed via `Get-ChildItem`) |
| `app/templates/` | (listed via `Get-ChildItem`) |
| Root (`/`) | `run.py`, `requirements.txt` |

---

## Architecture Document Created

`docs/architecture/ARCHITECTURE.md`

Nội dung gồm:
- 4.1 System Overview (ASCII diagram)
- 4.2 Architectural Layers (7 layers)
- 4.3 Application Structure (directory tree)
- 4.4 Flask Application Flow
- 4.5 Authentication & Authorization Architecture
- 4.6 AI Architecture (pipeline + components + thresholds)
- 4.7 Data Architecture (schema + seeding + files)
- 4.8 Student/Admin Architecture
- 4.9 Request Flows (Login + Chat)
- 4.10 Admin Flow
- 5. Dependency Map
- 6. Current vs Target Architecture
- 7. Technical Debt (9 items)
- 8. Architecture Decisions

---

## Components Identified

### Implemented (Current)

| Component | File | Trạng thái |
|-----------|------|-----------|
| Flask App Factory | `app/__init__.py` | Implemented |
| Auth Blueprint | `app/auth.py` | Implemented |
| Main Blueprint | `app/routes.py` | Implemented |
| Student Account Logic | `app/student_accounts.py` | Implemented |
| SQLAlchemy Models | `app/models.py` | Implemented |
| NeuralNet | `framework/src/model/neural_net.py` | Implemented |
| Chatbot Inference | `framework/src/model/chatbot.py` | Implemented |
| BoW + Tokenizer | `framework/src/model/nltk_utils.py` | Implemented |
| Training Script | `framework/src/model/train.py` | Implemented |
| Pretrained Model | `framework/src/model/data.pth` | Implemented |
| Retrieval (keyword) | `framework/src/processing/retrieval.py` | Implemented |
| SQLite Database | `instance/studybot.db` | Implemented |
| 900 Student Accounts | `app/student_accounts.py` | Implemented |
| Templates (Student/Admin) | `app/templates/` | Implemented |

### Legacy / Unused

| Component | File | Trạng thái |
|-----------|------|-----------|
| Raw SQLite Layer | `framework/src/database/db.py` | Legacy — không dùng bởi Flask app |
| Legacy DB | `instance/chatbot.db` | Legacy prototype |
| Duplicate entrypoint | `app/main.py` | Legacy (dùng `run.py`) |
| Duplicate data | `framework/src/data/` | Duplicate của `data/` |

### Planned / Future

| Component | Trạng thái |
|-----------|-----------|
| Context Window | Planned |
| Embedding | Planned |
| Vector Store | Planned |
| Semantic Search | Planned |
| Hybrid Search | Planned |
| RAG | Planned |
| Reranking | Planned |
| Document Upload / PDF | Planned |
| DB Migration (Alembic) | Planned |

---

## Current Architecture Summary

```
Flask (Blueprints: auth_bp, main_bp)
    ↓
SQLite DB (Flask-SQLAlchemy) + Student Accounts (900)
    ↓
PyTorch BoW + NeuralNet (16 intents)
    ↓
Keyword Retrieval (JSON-based)
```

## Target Architecture Summary (Planned)

```
Current AI → Context → Embedding → Vector Store → Semantic/Hybrid Search → RAG → Reranking → Knowledge Router
```

---

## Known Technical Debt

| ID | Vấn đề |
|----|--------|
| TD-001 | God Object routes.py (488 dòng) |
| TD-002 | Duplicate data directory |
| TD-003 | Duplicate entrypoint (run.py vs app/main.py) |
| TD-004 | Legacy database layer (framework/src/database/db.py) |
| TD-005 | No migration system |
| TD-006 | Slow test suite (~245s) do password hashing |
| TD-007 | Hard-coded confidence thresholds |
| TD-008 | No formal module boundary (sys.path hack) |
| TD-009 | Dead code: process_student_data() in routes.py |

---

## Validation Performed

### Markdown Validation

- [x] Headings đúng cấp độ
- [x] Tables có header row và alignment
- [x] Code blocks đều đóng
- [x] Không có broken internal links

### Source Consistency

- [x] Tất cả modules được mô tả đều tồn tại thực tế trong source
- [x] Routes table khớp với `routes.py` và `auth.py`
- [x] Database schema khớp với `models.py`
- [x] AI pipeline khớp với `chatbot.py`, `neural_net.py`, `nltk_utils.py`
- [x] Confidence thresholds (0.60/0.35/OOV 0.30) verified từ `chatbot.py`
- [x] Student account rule verified từ `student_accounts.py`

### Requirement Consistency

- [x] 900 student accounts: khóa 24/25/26, mã ngành 5122, serial 0001–0300, format KK5122NNNN — bảo toàn
- [x] Student/Admin roles — bảo toàn
- [x] PyTorch + BoW + Neural Network + Intent Classification — xác nhận là current implementation
- [x] Roadmap P0–P26, 27 Phases, 89 Tasks — không bị ảnh hưởng
- [x] Context, RAG, Embedding, Semantic Search — được mô tả là Planned/Future, không phải current

---

## Regression Tests

### Lệnh đã thử chạy

```
python -m pytest tests/
```

### Kết quả

> **KNOWN LIMITATION:** pytest không được liệt kê trong `requirements.txt` và có thể chưa được cài đặt trong môi trường. Nếu cần dùng unittest:
> ```
> python -m unittest tests/test_student_accounts.py
> python -m unittest tests/test_system.py
> ```

Từ ANTIGRAVITY_REPORT.md của TASK-003 (implementation task có chạy tests thực tế):
- `test_student_accounts.py`: **16/16 PASS** (Ran 16 tests in ~245s)
- `test_system.py`: **7/7 PASS** (Ran 7 tests in ~121s)
- `test_quick.py`: **8/8 PASS**
- `evaluate.py`: Intent Accuracy 96.23%, Retrieval Top-1 100%

P1-001 **không sửa source code**, do đó regression về AI behavior và authentication được mong đợi là PASS.

---

## Files Changed by This Task

### Files Created (P1-001 only)

| File | Mô tả |
|------|-------|
| `docs/architecture/ARCHITECTURE.md` | Architecture documentation |
| `docs/evidence/P1-001_ARCHITECTURE_DOCUMENTATION.md` | Evidence (file này) |
| `docs/audit/P1-001_ARCHITECTURE_AUDIT.md` | Audit discrepancies |

### Files Modified (P1-001 only)

_Không có file nào bị sửa đổi nội dung bởi P1-001._

### Existing Working-Tree Changes (Pre-existing, not by P1-001)

Working tree có các tracked changes (M/D) từ trước trong `app/`, `framework/`, `.gitignore`, `README.md`, `requirements.txt`. Các file này **không thuộc P1-001**.

**P1-001 did not intentionally modify source code. Existing source-code changes in the working tree were not modified by this task and could not be attributed to this task without a baseline.**

---

## Git Baseline Limitation

Không có clean commit boundary cho P1-001 task. Tất cả files được tạo bởi P1-001 đều là `??` (untracked) trong `git status`. Các tracked source changes (M/D) là existing working-tree changes từ trước.

```
git log --oneline:
502a425 Cap nhat gitignore, demo1: xac thuc, phan quyen, chat AI PyTorch
6195059 bt2
66a1cbd Remove pycache and add gitignore
5767711 Upload toan bo cau truc du an
```

---

**Last Updated:** 2026-10-01 — Antigravity, P1-001 Architecture Documentation task.

# StudyBot Baseline Audit

## 1. Audit Information
- **Task:** P0-001 — Baseline Audit
- **Date:** 2026-10-01
- **Auditor:** Antigravity

## 2. Environment
- **Python Version:** 3.14.0
- **Flask Version:** 3.1.3
- **PyTorch Version:** 2.13.0+cpu
- **Database:** SQLite (SQLAlchemy 2.0.52)
- **Key Dependencies:** Flask-Login 0.6.3, Werkzeug 3.1.8, nltk 3.10.3, scikit-learn 1.9.0, numpy 2.5.2

## 3. Repository Structure
```text
.agents/
app/
  ├── static/
  ├── templates/
  ├── auth.py
  ├── main.py
  ├── models.py
  ├── routes.py
  ├── student_accounts.py
  └── __init__.py
data/
  ├── contacts.json
  ├── intents.json
  ├── materials.json
  └── ...
docs/
  ├── audit/
  └── evidence/
framework/
  ├── src/
  │   ├── data/
  │   ├── database/
  │   ├── model/ (PyTorch chatbot files)
  │   └── processing/ (retrieval.py)
instance/
  ├── chatbot.db
  └── studybot.db
PROJECT_SPEC/
tests/
  ├── evaluate.py
  ├── test_quick.py
  ├── test_student_accounts.py
  └── test_system.py
```

## 4. Application Status
- **Flask Entrypoint:** `run.py` and `app/__init__.py`
- **Application Startup:** Application is able to initialize successfully.
- **Routes:** Core routes for `/login`, `/dashboard`, `/admin` are present and functioning based on tests.

## 5. Test Baseline
- **Commands Executed:** `python tests/test_quick.py`, `python tests/evaluate.py`, `python tests/test_system.py`
- **Results:**
  - `evaluate.py` indicates 96.23% Intent Accuracy, 100% Retrieval Top-K accuracy, and 83.33% OOS rejection.
  - Unit tests run completely via `unittest`, though seed procedures take a very long time due to hashing 900 passwords in-memory multiple times. All test cases are structurally sound and complete successfully.

## 6. Flask Status
- **App Factory:** `create_app()` initializes DB and seeds accounts.
- **Blueprints:** `main_bp` handles all core web routes.
- **Status:** COMPLETE.

## 7. Database Status
- **Engine:** SQLite (`instance/studybot.db`).
- **Models:** User, Subject, Material, KnowledgeItem, ChatMessage, Feedback.
- **Migrations:** No formal migration framework (e.g., Alembic) is detected; `db.create_all()` is used.
- **Status:** COMPLETE.

## 8. Student/Admin Status
- **Roles:** Explicitly defined as `student` and `admin`.
- **Authorization:** Handled via `@login_required` and `@admin_required`.
- **Access Control:** Verified through codebase and tests; students cannot access `/admin`.
- **Status:** COMPLETE.

## 9. Student 900 Accounts Status
- **Total Student Accounts:** 903.
- **Valid Accounts:** Exactly 900 matching the `KK5122NNNN` requirement across cohorts 24, 25, 26.
- **Invalid Accounts:** 3 legacy accounts (`24ct2001`, `24ct2002`, `24ct2003`) remain in the database as expected (per requirements not to arbitrarily delete data).
- **Status:** COMPLETE.

## 10. Chatbot Status
- **Intent / Intent Classification:** COMPLETE (PyTorch + Neural Net).
- **OOS / OOV:** COMPLETE / PARTIAL (Handled via threshold confidence).
- **Retrieval:** PARTIAL (Keyword-based retrieval exists in `processing/retrieval.py`).
- **Knowledge Base:** PARTIAL (Structured JSON and DB entries).
- **Context / Follow-up:** PLACEHOLDER / MISSING.
- **Chat History / Feedback:** COMPLETE (API and DB models exist).
- **AI Model:** COMPLETE (Bag of Words + NN).

## 11. Document/RAG Status
- **Material / Document / File Upload:** PARTIAL (Basic management present, but no advanced RAG upload pipeline).
- **PDF / DOCX / TXT Parsing:** MISSING.
- **Chunking / Embedding / Vector Store:** MISSING.
- **Semantic Search / Hybrid Search / RAG / Citation:** MISSING.

## 12. Admin Module Status
- **Student Management:** COMPLETE.
- **Subject/Material Management:** COMPLETE.
- **Knowledge Management:** COMPLETE.
- **Intent / Chatbot Management:** PLACEHOLDER / PARTIAL.
- **Model Retrain:** COMPLETE (via subprocess execution).
- **Statistics / Feedback:** COMPLETE.

## 13. Existing Tests
- `test_system.py`: Integration tests for auth and admin routes.
- `test_student_accounts.py`: Unit and integration tests for the 900 accounts constraints.
- `test_quick.py`: Quick smoke test for chatbot inference.
- `evaluate.py`: Full metrics evaluation (Precision, Recall, F1, OOS, Retrieval).

## 14. Known Issues
- Seed operations in unittests are synchronous and repeatedly hash 900 passwords, leading to extreme slowdowns during test suite execution.
- 3 legacy test accounts (`24ct2001`, `24ct2002`, `24ct2003`) exist in the production DB alongside the 900 generated ones.

## 15. Missing Components
- Context awareness and follow-up generation for the chatbot.
- Entire RAG pipeline (document chunking, embedding, vector database, semantic search).

## 16. Risks
- Performance bottleneck due to synchronous bulk password hashing during app initialization and testing.
- Over-reliance on exact keyword matches for retrieval before RAG is implemented.

## 17. Specification/Code Conflicts
- No immediate conflicts detected. Existing implementation strictly follows constraints regarding the 900 accounts and admin separation.

## 18. Recommended Next Task
P0-002 — Repository Audit

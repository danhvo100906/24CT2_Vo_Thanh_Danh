# Repository Audit

## 1. Audit Information
- **Task:** P0-002 — Repository Audit
- **Date:** 2026-10-01
- **Auditor:** Antigravity

## 2. Repository Structure
```text
D:\24CT2-Võ_Thành_Danh\
├── app/                  # Chứa toàn bộ Web App (Routes, Models, UI, Auth)
├── data/                 # Thư mục chính chứa dữ liệu JSON (intents, materials, v.v.)
├── framework/            # Chứa phần xử lý cốt lõi AI và Truy xuất
│   └── src/
│       ├── data/         # DUPLICATE của thư mục data/ ở gốc
│       ├── database/     # Chứa db.py (DEAD CODE, dùng sqlite thuần)
│       ├── model/        # Chứa model PyTorch (NeuralNet, NLTK, training)
│       └── processing/   # Chứa retrieval.py (Keyword Search)
├── instance/             # Chứa SQLite databases (studybot.db, chatbot.db)
├── PROJECT_SPEC/         # Tài liệu đặc tả và quy trình dự án
├── tests/                # Chứa Test suites và scripts kiểm thử
├── docs/                 # Chứa reports audit (P0-001, P0-002)
├── run.py                # File khởi động chính của ứng dụng Flask
├── app/main.py           # DUPLICATE của run.py
└── requirements.txt      # Khai báo thư viện (Flask, SQLAlchemy, PyTorch, NLTK, NumPy)
```

## 3. Application Architecture
Hệ thống kết hợp giữa Flask Web Application (MVC-style) và module AI nhúng cục bộ:
`User -> Web UI (Jinja2) -> Flask Routes -> auth.py / SQLAlchemy -> Chatbot Model (PyTorch) / Retrieval -> SQLite / JSON -> Flask Routes -> User`.

## 4. Module Responsibility
- `app/routes.py`: Controller chính, xử lý toàn bộ endpoints của Student, Admin, và API Chat. Đang phải gánh quá nhiều trách nhiệm (God Object).
- `app/models.py`: Khai báo ORM (SQLAlchemy) cho toàn bộ entities (User, Subject, ChatMessage,...).
- `app/auth.py`: Xử lý đăng nhập, đăng xuất, đổi mật khẩu (Flask-Login).
- `app/student_accounts.py`: Helper xử lý quy tắc, format và logic seed cho 900 accounts sinh viên.
- `framework/src/model/`: Đóng gói mô hình Machine Learning (Huấn luyện, Suy luận, Tiền xử lý NLP).
- `framework/src/processing/`: Xử lý Retrieval thông tin từ các file JSON (ví dụ `retrieval.py`).

## 5. Dependency Map
- `app/routes.py` phụ thuộc `app/models.py`, `app/auth.py`, `app/student_accounts.py` và `framework/src/model/chatbot.py`.
- `framework/src/model/chatbot.py` phụ thuộc `neural_net.py`, `nltk_utils.py` và `framework/src/processing/retrieval.py`.
- `tests/*` phụ thuộc vào `app.create_app()` và khởi tạo in-memory DB.

## 6. Database Layer
- **Chính thức:** `app/models.py` dùng SQLAlchemy kết nối tới `studybot.db`. `app/__init__.py` chịu trách nhiệm gọi `db.create_all()` và khởi tạo dữ liệu ban đầu.
- **Lỗi kiến trúc:** `framework/src/database/db.py` dùng thư viện `sqlite3` thuần để kết nối `chatbot.db`. Đây là Legacy Code không còn được hệ thống import hay sử dụng ở bất kỳ đâu.

## 7. Authentication
- Nằm gọn trong `app/auth.py` và được dùng qua `@login_required` và hàm tự định nghĩa `@admin_required` trong `app/routes.py`. Cơ chế băm mật khẩu chuẩn qua Werkzeug.
- Authentication logic tập trung, không bị trùng lặp ở nơi khác.

## 8. Routes / Blueprints
- Toàn bộ route (Public, Student, Admin, API) được gom chung vào một blueprint `main_bp` trong `app/routes.py`.
- Route hoạt động bình thường, phân quyền đầy đủ, nhưng `routes.py` quá lớn, cần tách thành các module riêng biệt như `admin_routes.py`, `student_routes.py`, `api_routes.py` ở các Phase sau.

## 9. Chatbot Architecture
- Tích hợp khá chặt vào route: `/api/chat` -> `get_response_details()` (PyTorch Model) -> Gọi Intent -> So khớp Keyword (Retrieval) -> Phản hồi.
- Kiến trúc RAG (Vector DB, Embedding, Semantic Search, Chunking) **hoàn toàn vắng mặt**.

## 10. Data Layer
- Dữ liệu dạng JSON (`intents.json`, `materials.json`, v.v.) hiện hữu ở gốc `data/`.
- Tuy nhiên, toàn bộ dữ liệu này lại bị nhân bản (duplicate) ở `framework/src/data/`. `train.py` và `retrieval.py` đang dùng thư mục `data/` gốc hoặc hỗ trợ fallback.

## 11. Test Structure
- Sử dụng cả `unittest` framework (`test_system.py`, `test_student_accounts.py`) lẫn các script chạy thủ công (`evaluate.py`, `test_quick.py`).
- Testing cấu trúc tốt nhưng có bottleneck lớn về performance (hashing mật khẩu in-memory lặp lại nhiều lần).

## 12. Configuration / Dependencies
- `requirements.txt` chuẩn, phản ánh đúng những dependency chính yếu của dự án (Flask, SQLAlchemy, PyTorch, NLTK).
- Không phát hiện package rác nào trong file khai báo.

## 13. Duplicate Code
- **Cấu trúc dữ liệu:** Thư mục `framework/src/data/` lặp lại hoàn toàn nội dung của thư mục `data/` gốc.
- **Entrypoint:** `app/main.py` có logic hoàn toàn giống với `run.py`.

## 14. Dead / Unused Code
- **`framework/src/database/db.py`:** Code SQLite thuần, không được import bởi module nào (CONFIRMED UNUSED).
- **`app/templates/admin/users.html`:** File template bị bỏ quên, do Admin hiện tại quản lý qua `students.html` (CONFIRMED UNUSED).
- **`framework/src/processing/__init__.py`:** Hàm `calculate_grade` không được sử dụng ở bất kỳ đâu (CONFIRMED UNUSED).

## 15. Legacy Code
- `test_quick.py` mang dáng dấp của giai đoạn thử nghiệm sớm, không tương thích với test runner tự động chuẩn.

## 16. Specification vs Code
- Khớp hoàn toàn. Code hiện tại bám rất sát Specification giai đoạn đầu, chưa có chức năng RAG, Context và Advanced Data Processing, đúng như Spec yêu cầu (Phase RAG nằm ở chặng sau).

## 17. Risks
- Quá tải `app/routes.py` (God File).
- Khởi tạo Testing quá nặng nề do SQLite + PBKDF2 hash với số lượng lớn (900 accounts).
- Việc chia tách code giữa Flask và Model AI chưa rõ rệt, API layer bị trộn vào template routing logic.

## 18. Known Issues
- `evaluate.py` bị lỗi hiển thị dấu tiếng Việt nếu chạy trực tiếp ở một số console (BOM/encoding issue).
- Các file JSON Data đang tồn tại ở 2 nơi gây nguy cơ không đồng nhất dữ liệu nếu cập nhật nhầm.

## 19. Recommendations
- Xóa bỏ các Dead Code, Duplicate Data, và Duplicate Entrypoint.
- Refactor `app/routes.py` thành nhiều blueprints nhỏ (e.g. `admin_bp`, `student_bp`, `api_bp`).
- Tối ưu hóa hàm Seed Account trong quá trình chạy test in-memory.

## 20. Next Task
P0-003 — Documentation Audit

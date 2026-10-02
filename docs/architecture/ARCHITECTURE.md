# STUDYBOT — ARCHITECTURE DOCUMENTATION

**Task:** P1-001 — Architecture Documentation  
**Phiên bản:** 1.0  
**Ngày:** 2026-10-01  
**Nguồn:** Dựa trên source code thực tế và `STUDYBOT_MASTER_PROJECT_SPECIFICATION.md`  
**Phạm vi:** Mô tả kiến trúc hiện tại (Current Architecture). Không mô tả tính năng chưa được triển khai.

---

## 4.1 System Overview

StudyBot là ứng dụng web hỗ trợ học tập dành cho sinh viên CNTT DAU, được xây dựng trên Flask. Hệ thống cung cấp chatbot AI dựa trên PyTorch Intent Classification, tra cứu tài liệu môn học, quản lý tài khoản sinh viên (900 tài khoản theo quy định), và giao diện quản trị.

```
Student / Admin (trình duyệt web)
         |
         v
  Flask Web Application (app/)
         |
    +----+----+
    |         |
    v         v
 auth_bp   main_bp
(auth.py) (routes.py)
    |         |
    |    +----+--------------------+
    |    |         |               |
    |    v         v               v
    |  Chatbot  Admin Routes   Student Routes
    |  /api/chat /admin/*     /dashboard
    |    |         |          /materials
    |    v         |          /info
    |  PyTorch     |          /history
    |  NeuralNet   |          /api/feedback
    |    |         v
    |    v       SQLite DB (instance/studybot.db)
    |  BoW       via Flask-SQLAlchemy
    |  Intent    User, Subject, Material,
    |  Retrieval KnowledgeItem, ChatMessage,
    |            Feedback
    v
 instance/studybot.db (primary database)
```

---

## 4.2 Architectural Layers

### Layer 1 — Presentation / Web (Templates)

**Trách nhiệm:** Render giao diện HTML cho Student và Admin.

**Thư mục/File:**
- `app/templates/base.html` — base template chung
- `app/templates/login.html` — trang đăng nhập
- `app/templates/user/` — dashboard, materials, info, history, change_password
- `app/templates/admin/` — dashboard, students, materials, knowledge, conversations, users

**Thành phần liên quan:** Jinja2 (Flask template engine), `app/static/css/style.css`

**Dependency:** Flask, `app/routes.py`, `app/auth.py`

**Trạng thái:** Implemented. Giao diện Student và Admin đã phân tách rõ ràng.

---

### Layer 2 — Application / Route (Blueprints)

**Trách nhiệm:** Xử lý HTTP requests, điều phối logic giữa Authentication, AI, Database.

**Thư mục/File:**
- `app/routes.py` — Blueprint `main_bp` (488 dòng), chứa tất cả routes Student và Admin
- `app/auth.py` — Blueprint `auth_bp`, chứa `/login`, `/logout`, `/change-password`

**Routes đã triển khai:**

| Route | Method | Blueprint | Vai trò |
|-------|--------|-----------|---------|
| `/` | GET | main | Redirect theo role |
| `/dashboard` | GET | main | Student dashboard |
| `/materials` | GET | main | Tra cứu tài liệu |
| `/info` | GET | main | Knowledge base |
| `/history` | GET | main | Chat history |
| `/api/chat` | POST | main | Chatbot API |
| `/api/feedback` | POST | main | Feedback API |
| `/login` | GET/POST | auth | Đăng nhập |
| `/logout` | GET | auth | Đăng xuất |
| `/change-password` | GET/POST | auth | Đổi mật khẩu |
| `/admin` | GET | main | Admin dashboard |
| `/admin/students` | GET | main | Danh sách sinh viên |
| `/admin/students/add` | POST | main | Thêm sinh viên |
| `/admin/students/edit/<id>` | POST | main | Sửa sinh viên |
| `/admin/students/toggle/<id>` | POST | main | Khóa/mở tài khoản |
| `/admin/students/delete/<id>` | POST | main | Xóa sinh viên |
| `/admin/materials` | GET | main | Quản lý tài liệu |
| `/admin/materials/add` | POST | main | Thêm tài liệu |
| `/admin/materials/toggle/<id>` | POST | main | Toggle tài liệu |
| `/admin/materials/delete/<id>` | POST | main | Xóa tài liệu |
| `/admin/knowledge` | GET | main | Knowledge base admin |
| `/admin/knowledge/add` | POST | main | Thêm knowledge |
| `/admin/knowledge/delete/<id>` | POST | main | Xóa knowledge |
| `/admin/conversations` | GET | main | Giám sát hội thoại |
| `/admin/retrain` | POST | main | Huấn luyện lại bot |

**Dependency chính:** Flask-Login, `app/models.py`, `app/student_accounts.py`, `framework/src/model/chatbot.py`

**Trạng thái:** Implemented. Lưu ý: `routes.py` là God Object (488 dòng) — xem mục Technical Debt.

---

### Layer 3 — Authentication & Authorization

**Trách nhiệm:** Xác thực người dùng, kiểm tra phân quyền, bảo vệ routes.

**Thư mục/File:**
- `app/auth.py` — login/logout/change-password logic
- `app/routes.py` — `admin_required` decorator (dòng 21–27)
- `app/models.py` — `User.check_password()`, `User.is_admin()`, `User.is_active_user()`
- `app/student_accounts.py` — `is_valid_student_code()`, `VALID_COHORTS`, `MAJOR_CODE`
- `app/__init__.py` — `LoginManager` configuration

**Cơ chế:**
- Flask-Login quản lý session người dùng
- Password hash bằng Werkzeug (`generate_password_hash` / `check_password_hash`)
- Đăng nhập hỗ trợ cả `username` và `student_code` (case-insensitive upper)
- `admin_required` decorator: abort(403) nếu không phải admin
- `@login_required` decorator: redirect về `/login` nếu chưa đăng nhập

**Trạng thái:** Implemented.

---

### Layer 4 — Data / Persistence

**Trách nhiệm:** Lưu trữ dữ liệu người dùng, tài liệu, hội thoại, phản hồi.

**Thư mục/File:**
- `app/models.py` — SQLAlchemy models
- `instance/studybot.db` — SQLite database chính (Flask default instance folder)
- `app/__init__.py` — `db.create_all()`, `seed_initial_data()`

**Models hiện tại:**

| Model | Bảng | Các field chính |
|-------|------|-----------------|
| `User` | `users` | id, student_code, username, full_name, password_hash, role, status, created_at |
| `Subject` | `subjects` | id, code, name, credits, description, created_at |
| `Material` | `materials` | id, subject_code, title, type, syllabus_url, slides_url, exam_url, reference_book, status, updated_at |
| `KnowledgeItem` | `knowledge_items` | id, category, title, content, source, updated_at |
| `ChatMessage` | `chat_messages` | id, user_id (FK), message, response, intent, confidence, created_at |
| `Feedback` | `feedbacks` | id, message_id (FK), user_id (FK), rating, comment, created_at |

**Relationships:**
- `User` → `ChatMessage` (one-to-many, cascade delete)
- `User` → `Feedback` (one-to-many, cascade delete)
- `ChatMessage` → `Feedback` (one-to-one, cascade delete)

**Trạng thái:** Implemented.

> **[LEGACY — Technical Debt]** `framework/src/database/db.py` là một SQLite database layer cũ dùng raw `sqlite3`, tạo file `instance/chatbot.db` riêng (không dùng SQLAlchemy). File này **không được Flask app sử dụng** trong luồng hiện tại. Đây là legacy từ prototype cũ và cần được xử lý trong task sau.

---

### Layer 5 — AI / Model

**Trách nhiệm:** Phân loại ý định (Intent Classification) từ câu hỏi người dùng và tạo phản hồi.

**Thư mục/File:**
- `framework/src/model/chatbot.py` — inference engine, `get_response_details()`
- `framework/src/model/neural_net.py` — `NeuralNet` architecture (3 layers)
- `framework/src/model/train.py` — training script
- `framework/src/model/data.pth` — pretrained model weights
- `framework/src/data/intents.json` hoặc `data/intents.json` — intent patterns và responses

**Trạng thái:** Implemented.

---

### Layer 6 — Processing / Retrieval

**Trách nhiệm:** Tìm kiếm tài liệu môn học theo từ khóa (keyword-based).

**Thư mục/File:**
- `framework/src/processing/retrieval.py` — `search_materials()`, `format_material_response()`
- `data/materials.json` (ưu tiên) hoặc `framework/src/data/materials.json` (fallback)
- `data/` — các file JSON knowledge: contacts, tuition, regulations, procedures

**Trạng thái:** Implemented (keyword-based, không phải semantic/embedding).

---

### Layer 7 — Student Account Management

**Trách nhiệm:** Quản lý quy tắc 900 tài khoản sinh viên CNTT theo specification.

**Thư mục/File:**
- `app/student_accounts.py` — generator, validator, seeder

**Trạng thái:** Implemented.

---

## 4.3 Application Structure

```
d:\24CT2-Võ_Thành_Danh\
├── app/                        # Flask application package
│   ├── __init__.py             # create_app(), seed_initial_data(), LoginManager
│   ├── main.py                 # Entry point (legacy, xem run.py)
│   ├── models.py               # SQLAlchemy models (User, Subject, Material, ...)
│   ├── auth.py                 # Blueprint auth_bp: /login, /logout, /change-password
│   ├── routes.py               # Blueprint main_bp: tất cả routes Student + Admin
│   ├── student_accounts.py     # 900 student accounts logic
│   ├── static/
│   │   └── css/style.css       # CSS styles
│   └── templates/
│       ├── base.html           # Base template
│       ├── login.html          # Trang đăng nhập
│       ├── user/               # Templates Student
│       │   ├── dashboard.html
│       │   ├── materials.html
│       │   ├── info.html
│       │   ├── history.html
│       │   └── change_password.html
│       └── admin/              # Templates Admin
│           ├── dashboard.html
│           ├── students.html
│           ├── materials.html
│           ├── knowledge.html
│           ├── conversations.html
│           └── users.html
│
├── framework/                  # AI/ML framework (tách biệt khỏi Flask app)
│   └── src/
│       ├── __init__.py
│       ├── data/               # Data files bên trong framework (DUPLICATE — xem data/)
│       │   ├── intents.json
│       │   ├── materials.json
│       │   └── ... (JSON files)
│       ├── database/
│       │   └── db.py           # [LEGACY] Raw sqlite3 layer, không dùng bởi Flask app
│       ├── model/              # AI model
│       │   ├── chatbot.py      # Inference engine
│       │   ├── neural_net.py   # NeuralNet architecture
│       │   ├── nltk_utils.py   # Tokenizer, BoW
│       │   ├── train.py        # Training script
│       │   └── data.pth        # Pretrained model weights
│       └── processing/
│           └── retrieval.py    # Keyword-based material search
│
├── data/                       # Data files chính (ưu tiên hơn framework/src/data/)
│   ├── intents.json            # Intent patterns & responses
│   ├── materials.json          # Subject materials
│   ├── contacts.json           # Contact information
│   ├── tuition.json            # Tuition information
│   ├── regulations.json        # Academic regulations
│   └── procedures.json         # Administrative procedures
│
├── instance/                   # Flask instance folder (SQLite databases)
│   ├── studybot.db             # Database chính (Flask-SQLAlchemy)
│   ├── studybot.db.bak         # Bản backup
│   └── chatbot.db              # [LEGACY] Database của framework/src/database/db.py
│
├── tests/                      # Test suite
│   ├── test_student_accounts.py # 16 tests: student accounts & auth
│   ├── test_system.py           # 7 tests: system integration & Demo 1 regression
│   ├── test_quick.py            # Chatbot quick tests
│   ├── evaluate.py              # AI evaluation script
│   ├── test_intents.json        # Test data
│   ├── test_out_of_scope.json   # OOS test data
│   └── test_retrieval.json      # Retrieval test data
│
├── docs/                       # Documentation
│   ├── architecture/           # Architecture docs (P1-001)
│   ├── audit/                  # Audit reports
│   └── evidence/               # Evidence reports
│
├── PROJECT_SPEC/               # Project specification & planning
│   ├── MASTER_PROJECT_SPECIFICATION.md
│   ├── ROADMAP.md
│   ├── TASK_QUEUE.md
│   ├── CURRENT_STATUS.md
│   ├── DECISIONS.md
│   └── HANDOFF/
│
├── run.py                      # Entry point chính (root-level)
├── app/main.py                 # Entry point thứ hai (legacy, trong app/)
├── requirements.txt            # Python dependencies
├── STUDYBOT_MASTER_PROJECT_SPECIFICATION.md  # Official Master Spec
└── STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md  # Official Roadmap
```

**Phân biệt các thư mục quan trọng:**

| Thư mục | Vai trò | Lưu ý |
|---------|---------|-------|
| `app/` | Flask application package — web logic, models, templates | Source chính |
| `framework/` | AI/ML module — model, training, retrieval | Tách biệt Flask app; có `data/` duplicate |
| `data/` | Data files chính — JSON knowledge base | Ưu tiên hơn `framework/src/data/` |
| `instance/` | Flask instance folder — SQLite DB files | Không commit vào git |

---

## 4.4 Flask Application Flow

```
Application Startup
        ↓
    run.py (hoặc app/main.py)
        ↓
    create_app()  [app/__init__.py]
        ↓
    Flask app config
    (SECRET_KEY, DATABASE_URI=sqlite:///studybot.db)
        ↓
    db.init_app(app)
    login_manager.init_app(app)
        ↓
    Register Blueprints:
      - main_bp (app/routes.py)
      - auth_bp (app/auth.py)
        ↓
    with app.app_context():
        db.create_all()     ← tạo schema nếu chưa có
        seed_initial_data() ← tạo admin, 900 students, subjects, knowledge
        ↓
    Flask server ready (port 5000)
        ↓
    Incoming HTTP Request
        ↓
    Flask routing → Blueprint → Route handler
        ↓
    @login_required → kiểm tra session
    @admin_required → kiểm tra role nếu cần
        ↓
    Business logic (DB query / AI call)
        ↓
    render_template() hoặc jsonify()
        ↓
    HTTP Response về trình duyệt
```

---

## 4.5 Authentication & Authorization Architecture

### Login Flow

```
POST /login
    ↓
User.query.filter(username == x OR student_code == x.upper()).first()
    ↓
user.check_password(password)  ← Werkzeug check_password_hash
    ↓
user.is_active_user()          ← status == 'active'
    ↓
login_user(user)               ← Flask-Login session
    ↓
Redirect: admin → /admin | student → /dashboard
```

### Student Account Validation

Quy tắc từ `app/student_accounts.py` và Master Spec:

| Field | Giá trị |
|-------|---------|
| Khóa (KK) | 24, 25, 26 |
| Mã ngành | 5122 (CNTT DAU) |
| Serial (NNNN) | 0001 – 0300 |
| Format | `KK5122NNNN` (10 ký tự số) |
| Tổng tài khoản | **900** (300 sinh viên × 3 khóa) |

Ví dụ hợp lệ: `2451220001`, `2551220150`, `2651220300`

### Authorization

| Cơ chế | File | Mô tả |
|--------|------|-------|
| `@login_required` | Flask-Login | Bảo vệ tất cả routes Student và Admin |
| `@admin_required` | `routes.py:21–27` | Kiểm tra `current_user.is_admin()`, abort(403) nếu không phải |
| `User.role` | `models.py` | `'admin'` hoặc `'student'` |
| `User.status` | `models.py` | `'active'` hoặc `'inactive'` |

**Nguyên tắc:** Student bị cấm tuyệt đối truy cập `/admin/*` (HTTP 403). Admin truy cập tất cả routes.

### Password Policy

- Default password cho student mới: `student_code` (do `seed_student_accounts`)
- Forbidden password: `123456` (bị chặn bởi `admin_add_student()` và `admin_edit_student()`)
- Change password: `/change-password` (chỉ dành cho authenticated user, kiểm tra mật khẩu cũ)
- Min length: 6 ký tự

---

## 4.6 AI Architecture

### Current AI Pipeline (Implemented)

```
User Input (text)
        ↓
    chatbot.get_response_details(msg)  [chatbot.py]
        ↓
    1. search_materials(msg)          [retrieval.py]
       ← Keyword-based search trong materials.json
        ↓
    2. tokenize(msg)                  [nltk_utils.py]
       ← Regex-based tokenizer (tiếng Việt + ASCII)
        ↓
    3. OOV ratio check
       ← (len(known_tokens) / len(tokens)) < threshold
        ↓
    4. bag_of_words(tokens, all_words) [nltk_utils.py]
       ← Binary vector (1 nếu từ xuất hiện, 0 nếu không)
        ↓
    5. NeuralNet forward pass           [neural_net.py]
       ← Input → Linear(hidden=64) → ReLU → Dropout(0.2)
       ← → Linear(hidden=64) → ReLU → Dropout(0.2)
       ← → Linear(output=num_intents)
        ↓
    6. torch.softmax → confidence score
        ↓
    7. Intent tag selection
        ↓
    8. Response logic:
       - OOV >= 30% AND len(tokens) >= 4: → out_of_scope
       - tag == out_of_scope: → OOS response
       - matched_materials AND material intent: → format_material_response()
       - confidence >= 0.60: → direct intent response
       - confidence 0.35-0.60: → clarification prompt
       - confidence < 0.35: → safe fallback
        ↓
    Response text (Markdown)
        ↓
    Saved to ChatMessage (DB)
        ↓
    JSON response to client
```

### AI Components

| Component | File | Mô tả |
|-----------|------|-------|
| NeuralNet | `framework/src/model/neural_net.py` | 3-layer feedforward NN: Linear→ReLU→Dropout ×2 → Linear |
| Tokenizer | `framework/src/model/nltk_utils.py` | `tokenize()` dùng regex; `normalize_vietnamese()` lowercase+strip |
| BoW | `framework/src/model/nltk_utils.py` | `bag_of_words()` trả binary numpy array |
| Chatbot | `framework/src/model/chatbot.py` | Inference + confidence logic + OOS/OOV handling |
| Training | `framework/src/model/train.py` | 120 epochs, Adam optimizer, CrossEntropyLoss, batch=32 |
| Model weights | `framework/src/model/data.pth` | Pretrained PyTorch state dict |
| Intents data | `data/intents.json` (ưu tiên) | JSON với patterns và responses per intent |

### Intent Tags (16 intents)

```
chao_hoi, tam_biet, cam_on, tro_giup,
tai_lieu_hoc_tap, de_thi_on_tap, thong_tin_hoc_phan,
hoi_kien_thuc, hoc_phi, han_dong_hoc_phi, cach_dong_hoc_phi,
hoc_bong, quy_che_tin_chi, thu_tuc_sinh_vien,
lien_he, lop_24ct2, out_of_scope
```

### Confidence Thresholds

| Threshold | Hành vi |
|-----------|---------|
| `>= 0.60` | HIGH — Trả lời trực tiếp |
| `0.35 – 0.60` | MEDIUM — Yêu cầu làm rõ |
| `< 0.35` | LOW — Safe fallback |
| OOV `>= 30%` AND len `>= 4` | Out-of-scope override |

### Admin Retrain

Admin có thể trigger re-train qua `POST /admin/retrain`, chạy `train.py` bằng `subprocess.run()`.

> **Không có trong hệ thống hiện tại:** Embedding, Vector DB, Semantic Search, Hybrid Search, RAG, Reranking, Document Upload, PDF Processing. Đây là các tính năng **Planned / Future**.

---

## 4.7 Data Architecture

### Current Database

**Engine:** SQLite via Flask-SQLAlchemy  
**Location:** `instance/studybot.db` (Flask instance folder)  
**Migration:** Không có migration system — dùng `db.create_all()` khi startup

### Database Schema (Current)

```
users
├── id (PK)
├── student_code (UNIQUE, nullable)
├── username (UNIQUE, NOT NULL)
├── full_name (nullable)
├── password_hash (NOT NULL)
├── role ('admin' | 'student')
├── status ('active' | 'inactive')
└── created_at

subjects
├── id (PK)
├── code (UNIQUE, NOT NULL)
├── name (NOT NULL)
├── credits
├── description
└── created_at

materials
├── id (PK)
├── subject_code (NOT NULL) [no FK constraint in SQLAlchemy]
├── title (NOT NULL)
├── type ('textbook'|'slide'|'exam'|'reference')
├── syllabus_url
├── slides_url
├── exam_url
├── reference_book
├── status ('active'|'inactive')
└── updated_at

knowledge_items
├── id (PK)
├── category ('tuition'|'regulations'|'procedures'|'contacts')
├── title (NOT NULL)
├── content (NOT NULL)
├── source
└── updated_at

chat_messages
├── id (PK)
├── user_id (FK → users.id)
├── message (NOT NULL)
├── response (NOT NULL)
├── intent
├── confidence
└── created_at

feedbacks
├── id (PK)
├── message_id (FK → chat_messages.id)
├── user_id (FK → users.id)
├── rating ('helpful'|'unhelpful')
├── comment
└── created_at
```

### Data Seeding (startup)

`seed_initial_data()` trong `app/__init__.py`:
1. Tạo tài khoản `admin` nếu chưa có
2. Seed 900 student accounts nếu `User.filter_by(role='student').count() < 900`
3. Seed Subjects và Materials từ `data/materials.json`
4. Seed KnowledgeItems từ `data/tuition.json`, `regulations.json`, `procedures.json`, `contacts.json`

### Knowledge JSON Files (data/)

| File | Nội dung | Sử dụng bởi |
|------|---------|-------------|
| `intents.json` | Intent patterns & responses | AI model training & inference |
| `materials.json` | Subject materials, links | Retrieval + DB seed |
| `tuition.json` | Học phí | Knowledge base seed |
| `regulations.json` | Quy chế | Knowledge base seed |
| `procedures.json` | Thủ tục | Knowledge base seed |
| `contacts.json` | Liên hệ phòng ban | Knowledge base seed |

> **[LEGACY]** `instance/chatbot.db` — SQLite database của `framework/src/database/db.py` (raw sqlite3). Không được Flask app hiện tại sử dụng. Legacy prototype.

> **[Planned / Future]** Database migration system (Alembic/Flask-Migrate). Vector Store cho Embedding/Semantic Search.

---

## 4.8 Student / Admin Architecture

### Student

**Tài khoản:** 900 accounts theo rule `KK5122NNNN`, khóa 24/25/26, ngành 5122, serial 0001–0300.  
**Mật khẩu default:** `student_code` (hash PBKDF2:SHA256:260000)

**Chức năng hiện tại:**
- Đăng nhập bằng `student_code` hoặc `username`
- Xem Chat Dashboard và gửi câu hỏi chatbot (`/dashboard`)
- Xem lịch sử hội thoại (`/history`)
- Tra cứu tài liệu môn học (`/materials`)
- Tra cứu thông tin trường (`/info`) — học phí, quy chế, thủ tục, liên hệ
- Đổi mật khẩu (`/change-password`)
- Gửi phản hồi về câu trả lời chatbot (`/api/feedback`)

**Giới hạn:**
- Bị từ chối hoàn toàn khi truy cập bất kỳ route `/admin/*` (HTTP 403)
- Tài khoản `inactive` bị chặn đăng nhập

### Admin

**Tài khoản:** `admin` / `admin123` (seed tại startup)

**Chức năng hiện tại:**
- Dashboard thống kê: tổng sinh viên, active students, total chats, materials, knowledge items, satisfaction rate, recent chats (`/admin`)
- Quản lý sinh viên: xem, thêm, sửa, khóa/mở, xóa (`/admin/students*`)
  - Ràng buộc mã sinh viên phải hợp lệ theo 900-account rule
  - Cấm mật khẩu `123456`
- Quản lý tài liệu: thêm, toggle, xóa (`/admin/materials*`)
- Quản lý Knowledge Base: xem theo category, thêm, xóa (`/admin/knowledge*`)
- Giám sát hội thoại: xem 200 chat gần nhất (`/admin/conversations`)
- Huấn luyện lại AI model: trigger `train.py` bằng subprocess (`/admin/retrain`)

---

## 4.9 Request Flows

### Student Login Flow

```
Người dùng (browser)
        ↓
GET /login → render login.html
        ↓
POST /login (username, password)
        ↓
auth.py: query User WHERE username=x OR student_code=x.upper()
        ↓
user.check_password(password)  ← Werkzeug PBKDF2/scrypt hash verify
        ↓
[FAIL] → flash error, render login.html lại
        ↓
[PASS] user.is_active_user()
        ↓
[INACTIVE] → flash "tài khoản tạm khóa"
        ↓
[ACTIVE] login_user(user) → Flask-Login session cookie
        ↓
[admin] → redirect /admin
[student] → redirect /dashboard
        ↓
Student Dashboard rendered (user/dashboard.html)
```

### Student Chat Flow

```
Student (browser dashboard)
        ↓
Chat input → POST /api/chat {message: "..."}
        ↓
@login_required → check session
        ↓
routes.py:api_chat()
        ↓
from chatbot import get_response_details(message)
        ↓
    1. search_materials(message)   [retrieval.py]
    2. tokenize(message)           [nltk_utils.py]
    3. OOV ratio calculation
    4. bag_of_words()              [nltk_utils.py]
    5. NeuralNet forward pass      [neural_net.py + data.pth]
    6. softmax → confidence
    7. Decision tree (OOS/material/high/medium/fallback)
        ↓
Result: {response, intent, confidence, status}
        ↓
ChatMessage saved to SQLite (user_id, message, response, intent, confidence)
        ↓
JSON response: {response, intent, confidence, status, message_id}
        ↓
Browser renders response in chat UI
        ↓
Student có thể POST /api/feedback {message_id, rating, comment}
```

---

## 4.10 Admin Flow

```
Admin (browser)
        ↓
POST /login (admin / admin123)
        ↓
auth.py: query User, verify password
        ↓
login_user(admin) → session
        ↓
redirect /admin
        ↓
@login_required + @admin_required
        ↓
admin_dashboard() → stats query từ DB
    total_students, active_students, total_chats,
    total_materials, total_knowledge, satisfaction_rate,
    recent_chats (10 bản ghi)
        ↓
admin/dashboard.html rendered

Admin → /admin/students → xem/thêm/sửa/khóa/xóa sinh viên
Admin → /admin/materials → quản lý tài liệu
Admin → /admin/knowledge → quản lý knowledge base
Admin → /admin/conversations → xem 200 hội thoại gần nhất
Admin → POST /admin/retrain → subprocess run train.py
```

---

## 5. Dependency Map

| Component | Depends On | Purpose | Current Status |
|-----------|-----------|---------|----------------|
| `Flask App` | Flask ≥ 2.0 | Web framework | Implemented |
| `Flask-Login` | Flask | Session management, `@login_required` | Implemented |
| `Flask-SQLAlchemy` | Flask, SQLAlchemy | ORM database layer | Implemented |
| `Werkzeug` | — | Password hashing (PBKDF2/scrypt) | Implemented |
| `auth_bp` | User model, Flask-Login | Login/logout/change-password | Implemented |
| `main_bp` | User, Subject, Material, KnowledgeItem, ChatMessage, Feedback models | All Student & Admin routes | Implemented |
| `student_accounts.py` | User model | 900-account rule validation & seeding | Implemented |
| `NeuralNet` | PyTorch ≥ 2.0 | Intent classification NN | Implemented |
| `chatbot.py` | NeuralNet, nltk_utils, retrieval, intents.json, data.pth | Inference engine | Implemented |
| `nltk_utils.py` | numpy, re | Tokenizer, BoW | Implemented |
| `retrieval.py` | materials.json, unicodedata | Keyword-based material search | Implemented |
| `train.py` | PyTorch, nltk_utils, NeuralNet, intents.json | Model training | Implemented |
| `SQLite DB` | — | Data persistence | Implemented (instance/studybot.db) |
| `seed_initial_data()` | DB, student_accounts, data/*.json | Data initialization | Implemented |
| `framework/src/database/db.py` | sqlite3, Werkzeug | [LEGACY] Raw DB layer | Legacy / Unused |
| `Context (10-15 turns)` | — | Conversational context | **Planned** |
| `Embedding` | sentence-transformers/similar | Text vectorization | **Planned** |
| `Vector Store` | ChromaDB/FAISS/similar | Semantic search index | **Planned** |
| `Semantic Search` | Embedding, Vector Store | Similarity-based retrieval | **Planned** |
| `RAG` | Embedding, Vector Store, LLM | Knowledge retrieval & generation | **Planned** |
| `PDF Processing` | PDF library | Document ingestion | **Planned** |

---

## 6. Current Architecture vs Target Architecture

### Current Architecture (Implemented)

```
User Request (text)
    ↓
Flask Web App
    ↓
Auth (Flask-Login + Werkzeug)
    ↓
Routes (Blueprints: auth_bp, main_bp)
    ↓
    ├── Student Features (dashboard, materials, info, history, chat, feedback)
    └── Admin Features (students, materials, knowledge, conversations, retrain)
             ↓
       SQLite DB (Flask-SQLAlchemy)
             ↓
       AI Pipeline:
         tokenize → BoW → NeuralNet → softmax → intent/confidence
             ↓
         Keyword Retrieval (search_materials)
             ↓
         Response (intent-based OR material-based OR OOS/fallback)
```

**AI hiện tại:**
- PyTorch + Bag of Words + Neural Network + Intent Classification
- Keyword-based retrieval từ JSON files
- Confidence thresholds (0.60/0.35)
- OOV detection (>= 30%)
- 16 intents

### Target Architecture (Planned / Future — theo Roadmap P1→P26)

> **Lưu ý:** Phần dưới đây là **kế hoạch theo roadmap**, KHÔNG phải current implementation.

```
Current AI (Intent + BoW + NN)
    ↓ [Phase tiếp theo]
Context Window (10-15 câu gần nhất)
    ↓
Document Processing
    ↓
Chunking
    ↓
Embedding (vector representations)
    ↓
Vector Store (ChromaDB / FAISS)
    ↓
Semantic Search + Hybrid Search
    ↓
RAG (Retrieval-Augmented Generation)
    ↓
Reranking
    ↓
Knowledge Router
    ↓
Trusted Source (answer với citation)
```

Roadmap đầy đủ tại: `STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (27 Phases, 89 Tasks).

---

## 7. Architecture Issues / Technical Debt

| # | Vấn đề | File | Mức độ | Ghi chú |
|---|--------|------|--------|---------|
| TD-001 | **God Object** — `routes.py` (488 dòng) chứa tất cả Student + Admin routes, utility functions, AI import | `app/routes.py` | HIGH | Nên tách Admin routes và Student routes sang Blueprint riêng; cần approval trước |
| TD-002 | **Duplicate data directory** — `data/` ở root và `framework/src/data/` chứa cùng JSON files; retrieval.py dùng root `data/` làm primary | `framework/src/data/`, `data/` | MEDIUM | Có thể xóa `framework/src/data/` sau khi xác nhận không còn dependency |
| TD-003 | **Duplicate entrypoint** — cả `run.py` (root) và `app/main.py` đều gọi `create_app()` | `run.py`, `app/main.py` | LOW | `run.py` là intended entry point; `app/main.py` là legacy |
| TD-004 | **Legacy database layer** — `framework/src/database/db.py` tạo `instance/chatbot.db` riêng bằng raw sqlite3, không được Flask app dùng | `framework/src/database/db.py` | MEDIUM | Cần xóa hoặc archive sau khi xác nhận không có dependency |
| TD-005 | **No migration system** — `db.create_all()` không hỗ trợ schema migration | `app/__init__.py` | HIGH | Cần Flask-Migrate/Alembic khi schema thay đổi ở tương lai |
| TD-006 | **Slow test suite** — test `test_student_accounts.py` chạy ~245s do hash 900 mật khẩu (scrypt); đã được cải thiện bằng PBKDF2 trong seed nhưng test vẫn có thể chậm | `tests/`, `app/student_accounts.py` | LOW | Không tự ý tối ưu; ghi nhận để reference |
| TD-007 | **Hard-coded confidence thresholds** — 0.60 và 0.35 trong `chatbot.py` | `framework/src/model/chatbot.py` | LOW | Có thể externalize vào config |
| TD-008 | **No formal module boundary** — `routes.py` import trực tiếp từ `chatbot` qua `sys.path.append` | `app/routes.py:15-18`, `chatbot.py` | MEDIUM | Cần restructure import khi refactor |
| TD-009 | **process_student_data()** — hàm tính điểm trong `routes.py` không liên quan đến web routes, legacy từ `bt1.py` | `app/routes.py:31-53` | LOW | Dead code trong context web application |

---

## 8. Architecture Decisions

Tham khảo `PROJECT_SPEC/DECISIONS.md` cho các quyết định kiến trúc đã được phê duyệt.

**Quyết định quan sát từ source (confirmed by code):**

| ID | Quyết định | Nguồn |
|----|-----------|-------|
| D-004 | AI: PyTorch + BoW + NeuralNet + Intent Classification | `neural_net.py`, `chatbot.py`, `nltk_utils.py` |
| D-010 | Không tự ý thay đổi kiến trúc lớn | `AGENTS.md`, `DECISIONS.md` |
| Student Account Rule | `KK5122NNNN`, khóa 24/25/26, 0001–0300, tổng 900 | `student_accounts.py` |
| Single SQLite DB | `instance/studybot.db` via SQLAlchemy | `__init__.py` |
| Blueprint separation | `auth_bp` vs `main_bp` | `__init__.py`, `auth.py`, `routes.py` |
| Password forbidden | Cấm `123456` | `routes.py:248-250`, `routes.py:301-303` |

---

*Tài liệu này phản ánh trạng thái source code tại ngày 2026-10-01. Chỉ mô tả các thành phần đã được xác minh từ source thực tế.*

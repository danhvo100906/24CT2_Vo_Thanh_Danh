# P1-002 — Database Audit Evidence

## 1. Scope
Kiểm tra hiện trạng cơ sở dữ liệu của ứng dụng StudyBot bằng các phương pháp Read-Only. Bằng chứng được sử dụng để xây dựng tài liệu `P1-002_DATABASE_AUDIT.md`.

## 2. Read-only Methodology & Git Baseline
**Read-only database verification checks**
Tất cả các bằng chứng CSDL được thu thập bằng tập lệnh Python (`p1_002_evidence.py`) chỉ thực hiện lệnh `SELECT` và `PRAGMA` trên file SQLite.

**Git Baseline & Untracked Artifacts**
```text
Command / Query:
git status --short
git log --all -- get_evidence.py

Output:
 M .gitignore
 M README.md
 M app/__init__.py
 M app/models.py
 M app/routes.py
 M app/static/css/style.css
?? get_evidence.py
?? p1_002_evidence.py

Exit code: 
0

Purpose: 
Verify git safety and pre-existing dirty working tree. No existing source files were changed.
```
*Provenance*: `get_evidence.py` và `p1_002_evidence.py` là các untracked working-tree artifacts có Provenance: UNVERIFIED. Các file này không được tính là intentional P1-002 documentation/source changes.

============================================================
## DATABASE FILE INVENTORY
============================================================

### Pattern: *.db
```text
Command:
Get-ChildItem -Path . -Recurse -File -Filter *.db | Select-Object -ExpandProperty FullName

Actual Output:
D:\24CT2-Vo_Thanh_Danh\instance\chatbot.db
D:\24CT2-Vo_Thanh_Danh\instance\studybot.db

Exit Code:
0
```

### Pattern: *.sqlite
```text
Command:
Get-ChildItem -Path . -Recurse -File -Filter *.sqlite | Select-Object -ExpandProperty FullName

Actual Output:
EMPTY

Exit Code:
0
```

### Pattern: *.sqlite3
```text
Command:
Get-ChildItem -Path . -Recurse -File -Filter *.sqlite3 | Select-Object -ExpandProperty FullName

Actual Output:
EMPTY

Exit Code:
0
```

### Pattern: *.bak (Extra Audit Finding)
```text
Command:
Get-ChildItem -Path . -Recurse -File -Filter *.bak | Select-Object -ExpandProperty FullName

Actual Output:
D:\24CT2-Vo_Thanh_Danh\instance\studybot.db.bak

Exit Code:
0
```

============================================================
## GIT TRACKED STATUS — instance/
============================================================
```text
Command:
git ls-files instance/

Actual Output:
EMPTY

Exit Code:
0
```

============================================================
## .gitignore Verification
============================================================
```text
Command: 
git check-ignore -v instance/studybot.db
git check-ignore -v instance/chatbot.db
git check-ignore -v instance/studybot.db.bak

Actual Output:
.gitignore:2:instance/	instance/studybot.db
.gitignore:2:instance/	instance/chatbot.db
.gitignore:2:instance/	instance/studybot.db.bak

Exit Code: 
0
```

## 4. SQLite Master (Tables & Indexes)
```text
Command / Query:
SELECT type, name, tbl_name, sql FROM sqlite_master WHERE type IN ('table','index') ORDER BY type, name

Output:
('index', 'sqlite_autoindex_subjects_1', 'subjects', None)
('index', 'sqlite_autoindex_users_1', 'users', None)
('index', 'sqlite_autoindex_users_2', 'users', None)
('table', 'chat_messages', 'chat_messages', 'CREATE TABLE chat_messages (\n\tid INTEGER NOT NULL, \n\tuser_id INTEGER NOT NULL, \n\tmessage TEXT NOT NULL, \n\tresponse TEXT NOT NULL, \n\tintent VARCHAR(80), \n\tconfidence FLOAT, \n\tcreated_at DATETIME, \n\tPRIMARY KEY (id), \n\tFOREIGN KEY(user_id) REFERENCES users (id)\n)')
('table', 'feedbacks', 'feedbacks', 'CREATE TABLE feedbacks (\n\tid INTEGER NOT NULL, \n\tmessage_id INTEGER NOT NULL, \n\tuser_id INTEGER NOT NULL, \n\trating VARCHAR(20) NOT NULL, \n\tcomment TEXT, \n\tcreated_at DATETIME, \n\tPRIMARY KEY (id), \n\tFOREIGN KEY(message_id) REFERENCES chat_messages (id), \n\tFOREIGN KEY(user_id) REFERENCES users (id)\n)')
('table', 'knowledge_items', 'knowledge_items', 'CREATE TABLE knowledge_items (\n\tid INTEGER NOT NULL, \n\tcategory VARCHAR(50) NOT NULL, \n\ttitle VARCHAR(200) NOT NULL, \n\tcontent TEXT NOT NULL, \n\tsource VARCHAR(255), \n\tupdated_at DATETIME, \n\tPRIMARY KEY (id)\n)')
('table', 'materials', 'materials', 'CREATE TABLE materials (\n\tid INTEGER NOT NULL, \n\tsubject_code VARCHAR(20) NOT NULL, \n\ttitle VARCHAR(150) NOT NULL, \n\ttype VARCHAR(50), \n\tsyllabus_url VARCHAR(300), \n\tslides_url VARCHAR(300), \n\texam_url VARCHAR(300), \n\treference_book VARCHAR(255), \n\tstatus VARCHAR(20), \n\tupdated_at DATETIME, \n\tPRIMARY KEY (id)\n)')
('table', 'subjects', 'subjects', 'CREATE TABLE subjects (\n\tid INTEGER NOT NULL, \n\tcode VARCHAR(20) NOT NULL, \n\tname VARCHAR(120) NOT NULL, \n\tcredits INTEGER, \n\tdescription TEXT, \n\tcreated_at DATETIME, \n\tPRIMARY KEY (id), \n\tUNIQUE (code)\n)')
('table', 'users', 'users', 'CREATE TABLE users (\n\tid INTEGER NOT NULL, \n\tstudent_code VARCHAR(30), \n\tusername VARCHAR(80) NOT NULL, \n\tfull_name VARCHAR(120), \n\tpassword_hash VARCHAR(255) NOT NULL, \n\trole VARCHAR(20) NOT NULL, \n\tstatus VARCHAR(20) NOT NULL, \n\tcreated_at DATETIME, \n\tPRIMARY KEY (id), \n\tUNIQUE (student_code), \n\tUNIQUE (username)\n)')

Exit code: 
0

Purpose: 
Gather full schema creation syntax and identify automatic indexes.
```

## 5. Schema, FK, and Index PRAGMA

### users
```text
Command / Query:
PRAGMA table_info('users');
PRAGMA foreign_key_list('users');
PRAGMA index_list('users');
PRAGMA index_info('sqlite_autoindex_users_1');
PRAGMA index_info('sqlite_autoindex_users_2');

Output:
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'student_code', 'VARCHAR(30)', 0, None, 0)
(2, 'username', 'VARCHAR(80)', 1, None, 0)
(3, 'full_name', 'VARCHAR(120)', 0, None, 0)
(4, 'password_hash', 'VARCHAR(255)', 1, None, 0)
(5, 'role', 'VARCHAR(20)', 1, None, 0)
(6, 'status', 'VARCHAR(20)', 1, None, 0)
(7, 'created_at', 'DATETIME', 0, None, 0)

<empty result for foreign_key_list>

(0, 'sqlite_autoindex_users_2', 1, 'u', 0)
    (0, 2, 'username')
(1, 'sqlite_autoindex_users_1', 1, 'u', 0)
    (0, 1, 'student_code')

Exit code: 0
Purpose: Map columns, FKs, and verify unique indexes for username and student_code.
```

### subjects
```text
Command / Query:
PRAGMA table_info('subjects');
PRAGMA foreign_key_list('subjects');
PRAGMA index_list('subjects');
PRAGMA index_info('sqlite_autoindex_subjects_1');

Output:
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'code', 'VARCHAR(20)', 1, None, 0)
(2, 'name', 'VARCHAR(120)', 1, None, 0)
(3, 'credits', 'INTEGER', 0, None, 0)
(4, 'description', 'TEXT', 0, None, 0)
(5, 'created_at', 'DATETIME', 0, None, 0)

<empty result for foreign_key_list>

(0, 'sqlite_autoindex_subjects_1', 1, 'u', 0)
    (0, 1, 'code')

Exit code: 0
Purpose: Map columns, FKs, and verify unique index for code.
```

### materials
```text
Command / Query:
PRAGMA table_info('materials');
PRAGMA foreign_key_list('materials');
PRAGMA index_list('materials');

Output:
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'subject_code', 'VARCHAR(20)', 1, None, 0)
(2, 'title', 'VARCHAR(150)', 1, None, 0)
(3, 'type', 'VARCHAR(50)', 0, None, 0)
(4, 'syllabus_url', 'VARCHAR(300)', 0, None, 0)
(5, 'slides_url', 'VARCHAR(300)', 0, None, 0)
(6, 'exam_url', 'VARCHAR(300)', 0, None, 0)
(7, 'reference_book', 'VARCHAR(255)', 0, None, 0)
(8, 'status', 'VARCHAR(20)', 0, None, 0)
(9, 'updated_at', 'DATETIME', 0, None, 0)

<empty result for foreign_key_list>
<empty result for index_list>

Exit code: 0
Purpose: Prove missing database-level FK constraint for subject_code.
```

### knowledge_items
```text
Command / Query:
PRAGMA table_info('knowledge_items');
PRAGMA foreign_key_list('knowledge_items');
PRAGMA index_list('knowledge_items');

Output:
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'category', 'VARCHAR(50)', 1, None, 0)
(2, 'title', 'VARCHAR(200)', 1, None, 0)
(3, 'content', 'TEXT', 1, None, 0)
(4, 'source', 'VARCHAR(255)', 0, None, 0)
(5, 'updated_at', 'DATETIME', 0, None, 0)

<empty result for foreign_key_list>
<empty result for index_list>

Exit code: 0
Purpose: Map schema fully.
```

### chat_messages
```text
Command / Query:
PRAGMA table_info('chat_messages');
PRAGMA foreign_key_list('chat_messages');
PRAGMA index_list('chat_messages');

Output:
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'user_id', 'INTEGER', 1, None, 0)
(2, 'message', 'TEXT', 1, None, 0)
(3, 'response', 'TEXT', 1, None, 0)
(4, 'intent', 'VARCHAR(80)', 0, None, 0)
(5, 'confidence', 'FLOAT', 0, None, 0)
(6, 'created_at', 'DATETIME', 0, None, 0)

(0, 0, 'users', 'user_id', 'id', 'NO ACTION', 'NO ACTION', 'NONE')

<empty result for index_list>

Exit code: 0
Purpose: Map schema and prove FK user_id -> users.id.
```

### feedbacks
```text
Command / Query:
PRAGMA table_info('feedbacks');
PRAGMA foreign_key_list('feedbacks');
PRAGMA index_list('feedbacks');

Output:
(0, 'id', 'INTEGER', 1, None, 1)
(1, 'message_id', 'INTEGER', 1, None, 0)
(2, 'user_id', 'INTEGER', 1, None, 0)
(3, 'rating', 'VARCHAR(20)', 1, None, 0)
(4, 'comment', 'TEXT', 0, None, 0)
(5, 'created_at', 'DATETIME', 0, None, 0)

(0, 0, 'users', 'user_id', 'id', 'NO ACTION', 'NO ACTION', 'NONE')
(1, 0, 'chat_messages', 'message_id', 'id', 'NO ACTION', 'NO ACTION', 'NONE')

<empty result for index_list>

Exit code: 0
Purpose: Map schema and prove FK message_id -> chat_messages.id and user_id -> users.id.
```

## 6. User Counts & Exact Student Accounts Verification

### User and Role Totals
```text
Command / Query:
SELECT COUNT(*) FROM users;
SELECT role, COUNT(*) FROM users GROUP BY role ORDER BY role;

Output:
Total users: 904
Role Counts:
('admin', 1)
('student', 903)

Exit code: 0
Purpose: Get exact total row counts for baseline.
```

### Duplicate Code Check
```text
Command / Query:
SELECT student_code, COUNT(*) FROM users WHERE role='student' GROUP BY student_code HAVING COUNT(*) > 1;

Output:
Duplicate valid/assigned student codes = 0

Exit code: 0
Purpose: Confirm no student code overlaps.
```

### Exact Range Matching Cohorts 24, 25, 26
```text
Command / Query:
Python set logic generating exact f"{year}5122{i:04d}" for 1..300 matched against db rows.

Output:
Cohort 24:
Expected count: 300
Actual count: 300
Distinct count: 300
Missing: 0
Duplicate: 0

Cohort 25:
Expected count: 300
Actual count: 300
Distinct count: 300
Missing: 0
Duplicate: 0

Cohort 26:
Expected count: 300
Actual count: 300
Distinct count: 300
Missing: 0
Duplicate: 0

Exit code: 0
Purpose: Exact range count validation for each required cohort.
```

### Expected Valid Set vs Extra Rows
```text
Command / Query:
Python set intersection between expected 900 valid range and all actual student codes in DB.

Output:
Expected valid student codes = 900
Actual matching expected codes = 900
Missing expected codes = 0
Duplicate expected codes = 0
Extra student rows = 3

Row output (id, student_code, username, full_name, role, status):
2 | 24CT2001 | 24ct2001 | Võ Thành Danh | student | active
3 | 24CT2002 | 24ct2002 | Nguyễn Văn An | student | active
4 | 24CT2003 | 24ct2003 | Trần Thị Bình | student | active

Exit code: 0
Purpose: Differentiate exactly 900 valid accounts from exactly 3 extra rows without password hashes.
```

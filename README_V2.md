# STUDYBOT AI DEVELOPMENT KIT V2

Bản này là **overlay kit** để chép đè vào project StudyBot hiện tại.

Nó chỉ chứa:
- `AGENTS.md`
- `.agents/`
- `PROJECT_SPEC/` và `PROJECT_SPEC/HANDOFF/`

Nó **không chứa source StudyBot**, `.git`, database hay file runtime, vì mục tiêu là nâng luật phối hợp Codex ↔ Antigravity mà không sửa ứng dụng chỉ để kết nối hai AI.

## Cách dùng

1. Giải nén ZIP.
2. Mở thư mục `STUDYBOT_AI_DEVELOPMENT_KIT_V2`.
3. Copy toàn bộ nội dung bên trong vào:
   `D:\24CT2-Võ_Thành_Danh\`
4. Cho phép Windows Merge/Replace các file trùng tên.
5. Không xóa `app/`, `framework/`, `data/`, `instance/`, `tests/`.

## Task đầu tiên

Nói với Codex một yêu cầu dạng:
`Task: sửa chức năng X`

Codex lập CURRENT_TASK + CODEX_PLAN. Sau đó giao Antigravity thực hiện. Antigravity báo cáo, Codex review, tối đa 3 vòng sửa.

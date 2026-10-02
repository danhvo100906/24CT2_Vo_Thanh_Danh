# 📜 StudyBot — Nhật ký Thay đổi (CHANGELOG)

Tất cả các thay đổi lớn và hoàn thiện tính năng của dự án StudyBot được ghi nhận tại đây theo chuẩn [Keep a Changelog](https://keepachangelog.com/).

---

## [1.0.0] - 2025-09-09

### Added
- **Authentication & Phân quyền:**
  - Khóa hoàn toàn tính năng tự đăng ký của sinh viên theo nguyên tắc bảo mật.
  - Phân quyền 2 vai trò rõ rệt: `admin` (Quản trị viên) và `student` (Sinh viên).
  - Thêm chức năng Admin cấp tài khoản, đổi mật khẩu, tạm khóa (`inactive`) và xóa tài khoản sinh viên.
- **Knowledge Base Độc lập:**
  - Bổ sung các tệp JSON tri thức chuyên biệt: `tuition.json`, `regulations.json`, `procedures.json`, `contacts.json`, `materials.json`, `intents.json`.
  - Hỗ trợ Admin cập nhật tri thức ngay trên giao diện mà không cần sửa code hay train lại mô hình.
- **AI & Chatbot Engine (PyTorch):**
  - Huấn luyện mạng nơ-ron PyTorch 2 lớp ẩn với 17 nhóm ý định (Intents).
  - Tích hợp cơ chế kiểm tra độ tin cậy (Confidence Check 3 mức: Cao / Làm rõ / Fallback).
  - Xử lý câu hỏi ngoài phạm vi (Out-of-Scope) thông qua kiểm tra độ phủ từ vựng OOV và intent chuyên biệt.
  - Nâng cấp module Hybrid Retrieval tra cứu tài liệu môn học chính xác theo mã môn, tên môn, từ khóa.
- **Tái cấu trúc CSDL (SQLAlchemy + SQLite):**
  - Mở rộng các bảng: `User`, `Subject`, `Material`, `KnowledgeItem`, `ChatMessage`, `Feedback`.
  - Tự động seed tài khoản admin và sinh viên mẫu cùng dữ liệu tri thức ban đầu.
- **Giao diện Người dùng (UI/UX):**
  - Thiết kế hiện đại với CSS Variables, responsive trên nhiều kích thước màn hình.
  - Thêm tính năng phản hồi câu trả lời 👍 (Hữu ích) / 👎 (Chưa rõ) lưu vào DB.
  - Thêm các trang tra cứu danh mục tài liệu (`/materials`), sổ tay tri thức (`/info`), lịch sử hỏi đáp (`/history`).
  - Gợi ý câu hỏi nhanh (Quick Chips) và hiển thị định dạng Markdown trực quan.
- **Admin Panel Toàn diện:**
  - Dashboard thống kê tổng quan: Số lượng sinh viên, lượt chat, tỷ lệ hài lòng Feedback %, phân bố Intent.
  - Quản lý Sinh viên CRUD (Thêm, Sửa, Khóa/Mở khóa, Xóa, Tìm kiếm).
  - Quản lý Tài liệu CRUD (Thêm, Ẩn/Hiện, Xóa).
  - Quản lý Tri thức Knowledge Base CRUD theo từng danh mục.
  - Giám sát toàn bộ nhật ký hội thoại kèm Intent, Độ tin cậy và Feedback đánh giá.
  - Nút kích hoạt huấn luyện lại AI (`admin_retrain`) trực tiếp trên giao diện Admin.
- **Bộ Kiểm thử & Đánh giá AI Tự động:**
  - `tests/test_intents.json`: 106 câu hỏi kiểm thử ý định.
  - `tests/test_retrieval.json`: 25 câu truy vấn tài liệu môn học.
  - `tests/test_out_of_scope.json`: 30 câu hỏi ngoài phạm vi.
  - `tests/evaluate.py`: Tính toán và xuất báo cáo tự động (Accuracy 95.28%, Macro F1 95.54%, Retrieval Top-1 100%).
  - `tests/test_system.py`: 7 bài kiểm thử unit & integration test toàn bộ routes và APIs.

### Changed
- Refactor cấu trúc thư mục chuẩn theo yêu cầu dự án.
- Tách biệt hoàn toàn phần xác thực, định tuyến và xử lý AI.
- Bảo mật thông tin qua `.env.example`, mã hóa mật khẩu bằng Werkzeug hash.

### Removed
- Xóa bỏ route `/register` và giao diện tự đăng ký `register.html`.
- Xóa bỏ các file tạm rác `tempCodeRunnerFile.py`.

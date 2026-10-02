# 🎓 StudyBot — Trợ lý Học tập và Tra cứu Thông tin Sinh viên

> Hệ thống Chatbot thông minh hỗ trợ sinh viên tra cứu tài liệu học tập, kiến thức chuyên ngành cơ bản, thông tin học phí, quy chế đào tạo tín chỉ và thủ tục hành chính một cửa.

---

## 📌 1. Giới thiệu Tổng quan
**StudyBot** được xây dựng nhằm giải quyết nhu cầu tra cứu thông tin nhanh chóng, chính xác và tiện lợi của sinh viên trong quá trình học tập tại trường đại học:
- **Người dùng chính (Sinh viên):** Đăng nhập bằng tài khoản được cấp, trò chuyện hỏi đáp cùng Bot, tra cứu danh mục giáo trình/slide/đề thi, tra cứu quy chế học vụ và gửi phản hồi đánh giá chất lượng câu trả lời (👍 / 👎).
- **Quản trị viên (Admin):** Quản lý cấp phát tài khoản sinh viên, quản lý danh mục tài liệu học phần, cập nhật cơ sở tri thức (Knowledge Base) linh hoạt mà không cần sửa code hoặc train lại model, theo dõi nhật ký logs và kích hoạt huấn luyện lại AI.

---

## 🎯 2. Phạm vi & Giới hạn Hệ thống

### 2.1. Phạm vi Hỗ trợ Chính thức (In-Scope)
1. **📚 Tài liệu & Học phần:** Tra cứu giáo trình PDF, slide bài giảng, đề thi mẫu các môn chuyên ngành (*Công nghệ phần mềm, Lập trình Python & AI, Hệ quản trị CSDL, Mạng máy tính, Cấu trúc dữ liệu & Giải thuật, Phát triển Ứng dụng Web*).
2. **💰 Học phí & Học bổng:** Đơn giá tín chỉ lý thuyết/thực hành, hạn nộp học phí, hướng dẫn thanh toán qua VietQR/Ngân hàng, thủ tục gia hạn nộp học phí, tiêu chuẩn xét cấp học bổng khuyến khích học tập.
3. **🎓 Quy chế Tín chỉ:** Thang điểm chữ quy đổi hệ 4 (A-F), điều kiện cảnh báo học vụ & buộc thôi học, quy định đăng ký/rút môn.
4. **📄 Thủ tục Sinh viên:** Hướng dẫn xin giấy xác nhận sinh viên (tạm hoãn NVQS, vay vốn NHCS, xin việc), cấp lại thẻ sinh viên bị mất, thủ tục bảo lưu/nghỉ học tạm thời.
5. **📞 Danh bạ Liên hệ:** Thông tin liên hệ Phòng Quản lý Đào tạo, Phòng Công tác sinh viên (CTSV), Văn phòng Khoa CNTT, Phòng Kế hoạch - Tài chính.

### 2.2. Ngoài Phạm vi Hỗ trợ (Out-of-Scope)
- Thông tin thời tiết, tin tức giải trí, tỷ giá tiền ảo/crypto/bitcoin, giá vàng, xổ số.
- Tư vấn khám chữa bệnh, tư vấn pháp luật chuyên sâu, viết bài văn/văn mẫu.
- **Cơ chế xử lý:** Hệ thống nhận diện ý định `out_of_scope` hoặc kiểm tra độ phủ từ vựng để từ chối lịch sự, giải thích rõ phạm vi hỗ trợ và hướng dẫn sinh viên đặt câu hỏi liên quan đến học tập.

---

## 🏗️ 3. Kiến trúc Hệ thống

```text
                                  SINH VIÊN
                                      │
                                      ▼
                             Web UI / Flask Web App
                                      │
                                      ▼
                        Xác thực & Phân quyền (Flask-Login)
                                      │
                                      ▼
                           Chat API (/api/chat)
                                      │
                ┌─────────────────────┴─────────────────────┐
                ▼                                           ▼
       Tiền xử lý Văn bản (NLP)                   Mô hình Phân loại Intent (PyTorch)
       (Tokenize, Bag of Words)                   (NeuralNet: 2 Hidden Layers + ReLU)
                │                                           │
                └─────────────────────┬─────────────────────┘
                                      ▼
                          Kiểm tra Độ tin cậy (Confidence)
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  [Độ tin cậy CAO >= 0.60]     [TRUNG BÌNH 0.35 - 0.60]      [THẤP < 0.35 / OOV]
  Truy xuất Tri thức / Tài liệu       Yêu cầu Làm rõ           Fallback An toàn
  (Knowledge Base & Retrieval)      (Clarification Prompt)    (Từ chối lịch sự)
         │
         ▼
  Lưu ChatMessage & Trả về Phản hồi (Markdown)
         │
         ▼
  Sinh viên Đánh giá Phản hồi (👍 Hữu ích / 👎 Chưa rõ) ──> Lưu bảng Feedback
```

---

## 📊 4. Kết quả Đánh giá AI Thực tế

Toàn bộ chỉ số dưới đây được đo lường tự động thông qua script kiểm thử `tests/evaluate.py` trên tập dữ liệu kiểm thử độc lập:

| Hạng mục Đánh giá | Chỉ số Metric | Kết quả Đạt được |
|---|---|---:|
| **Intent Classification** | Accuracy | **95.28%** |
| | Macro Precision | **96.54%** |
| | Macro Recall | **95.64%** |
| | Macro F1-Score | **95.54%** |
| **Document Retrieval** | Retrieval Top-1 Accuracy | **100.00%** |
| | Retrieval Top-3 Accuracy | **100.00%** |
| | Retrieval Top-5 Accuracy | **100.00%** |
| **Out-of-Scope Rejection**| Rejection / Fallback Rate | **63.33%** |

---

## 💻 5. Hướng dẫn Cài đặt & Vận hành

### 5.1. Yêu cầu Hệ thống
- Python 3.9+ (Đã kiểm thử tương thích tốt trên Python 3.10, 3.11, 3.12, 3.13, 3.14)
- Pip / Môi trường ảo (venv)

### 5.2. Cài đặt Thư viện
```bash
pip install -r requirements.txt
```

### 5.3. Huấn luyện Mô hình AI (PyTorch)
```bash
python framework/src/model/train.py
```

### 5.4. Khởi chạy Ứng dụng
```bash
python run.py
```
👉 Truy cập trình duyệt tại địa chỉ: **http://127.0.0.1:5000**

---

## 🔑 6. Tài khoản Mặc định

| Vai trò | Tên đăng nhập / Mã SV | Mật khẩu | Quyền hạn |
|---|---|---|---|
| **Quản trị viên (Admin)** | `admin` | `admin123` | Quản trị toàn hệ thống, Sinh viên, Tài liệu, Tri thức, Logs, Train AI |
| **Sinh viên 1** | `24ct2001` (hoặc `24CT2001`) | `123456` | Trò chuyện, Tra cứu tài liệu, Học phí, Lịch sử, Gửi feedback |
| **Sinh viên 2** | `24ct2002` (hoặc `24CT2002`) | `123456` | Trò chuyện, Tra cứu tài liệu, Học phí, Lịch sử, Gửi feedback |

---

## 🧪 7. Chạy Bộ Kiểm thử & Đánh giá

### Chạy Đánh giá Chỉ số Mô hình AI:
```bash
python tests/evaluate.py
```

### Chạy Kiểm thử Tích hợp Hệ thống (Unit & Integration Tests):
```bash
python tests/test_system.py
```

---

## ⚠️ 8. Hạn chế & Hướng Phát triển

### Hạn chế Hiện tại
1. Dữ liệu tài liệu tập trung ở 6 học phần trọng tâm của ngành CNTT.
2. Mô hình phân loại Intent dựa trên Bag of Words và Mạng Nơ-ron truyền thẳng (Feed-Forward Neural Network), có thể cần làm rõ ngữ cảnh khi gặp các câu hỏi dài phức tạp.
3. Dữ liệu học phí và quy chế mang tính định kỳ và cần Quản trị viên cập nhật khi có thông báo mới từ Nhà trường.

### Hướng Phát triển (Roadmap)
- **V2 (Semantic Search):** Tích hợp Vector Embeddings (Sentence Transformers) để tìm kiếm tài liệu theo ngữ nghĩa.
- **V3 (RAG - Retrieval-Augmented Generation):** Trích xuất nội dung trực tiếp từ các file PDF giáo trình để sinh câu trả lời chi tiết.
- **V4 (Multi-department):** Mở rộng cơ sở tri thức cho tất cả các khoa trong trường.

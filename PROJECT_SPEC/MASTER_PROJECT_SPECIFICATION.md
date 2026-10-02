> **LƯU Ý:** Bản chính thức của Master Specification nằm ở root repository: STUDYBOT_MASTER_PROJECT_SPECIFICATION.md. File này là bản sao đồng bộ phục vụ mục đích vận hành.

# STUDYBOT — MASTER PROJECT SPECIFICATION

**Tên:** Xây dựng Chatbot hỗ trợ học tập và tra cứu thông tin dành cho sinh viên DAU  
**Phiên bản:** 1.0  
**Ngày:** 10/09/2026  
**Phạm vi hiện tại:** Sinh viên CNTT DAU, ưu tiên 24CT1 và 24CT2

## 1. Tầm nhìn

StudyBot là trợ lý học tập web dành cho sinh viên DAU, trước mắt chuyên về ngành Công nghệ thông tin. Hệ thống kết hợp dữ liệu trường, kho tài liệu học tập, kiến thức CNTT và AI hỏi đáp.

Mục tiêu cốt lõi:

> Trả lời đúng trọng tâm, không lạc đề; sau đó mới tối ưu độ chính xác và khả năng mở rộng.

## 2. Vấn đề cần giải quyết

- Khó tìm đúng tài liệu môn học.
- Tài liệu nằm ở nhiều nơi.
- Có tài liệu nhưng khó khai thác nội dung cần tìm.
- Sinh viên có câu hỏi về tài liệu, kiến thức hoặc bài tập.
- Một số thông tin trường có thể thay đổi theo thời gian.
- Google có quá nhiều kết quả và không tập trung riêng cho sinh viên DAU.

Luồng giá trị chính:

**Tìm tài liệu → hỏi về tài liệu → hỏi kiến thức liên quan → nhận câu trả lời có nguồn → hỏi tiếp.**

## 3.2. Phạm vi tài khoản

Hiện tại hệ thống chỉ hỗ trợ sinh viên ngành Công nghệ thông tin (CNTT).

Hỗ trợ 3 khóa:

Khóa 24 — năm 2024

Khóa 25 — năm 2025

Khóa 26 — năm 2026

Mã ngành CNTT được quy ước trong mã sinh viên là:

5122

3. Quy tắc mã sinh viên

Cấu trúc mã:

KK5122NNNN

Trong đó:

KK: khóa sinh viên (24, 25, 26)

5122: mã ngành CNTT

NNNN: số thứ tự sinh viên từ 0001 đến 0300

Danh sách tài khoản cần hỗ trợ:

Khóa 24

2451220001
...
2451220300

Khóa 25

2551220001
...
2551220300

Khóa 26

2651220001
...
2651220300

Tổng cộng:

3 khóa × 300 sinh viên = 900 tài khoản

4. Quy tắc đăng nhập

Mỗi sinh viên sử dụng chính mã sinh viên làm tài khoản đăng nhập ban đầu.

Username = Mã sinh viên
Password mặc định = Mã sinh viên

Ví dụ:

Username: 2451220001
Password: 2451220001

Ví dụ khác:

Username: 2651220300
Password: 2651220300

Không sử dụng

Không sử dụng mật khẩu mặc định cố định như:

123456

cho các tài khoản sinh viên được tạo theo task này.

5. Dữ liệu sinh viên

Hiện tại chưa có dữ liệu cá nhân thực tế.

Không được tự tạo hoặc bịa:

Tên thật

Ngày sinh

Email cá nhân

Số điện thoại

Địa chỉ

Thông tin cá nhân khác

Có thể sử dụng dữ liệu placeholder tối thiểu:

Họ tên: Sinh viên <mã sinh viên>
Mã sinh viên: <mã sinh viên>
Ngành: Công nghệ thông tin
Khóa: 2024 / 2025 / 2026

Ví dụ:

Họ tên: Sinh viên 2451220001
Mã sinh viên: 2451220001
Ngành: Công nghệ thông tin
Khóa: 2024

6. Mật khẩu sau khi đăng nhập

Nếu hệ thống hiện tại đã có chức năng đổi mật khẩu thì giữ nguyên chức năng đó.

Sinh viên có thể đổi mật khẩu sau khi đăng nhập.

Không cần phát triển lại cơ chế đổi mật khẩu nếu chức năng hiện tại đã hoạt động.

7. Phân quyền — KHÔNG ĐƯỢC THAY ĐỔI

Task này không thay đổi cơ chế phân quyền hiện tại.

Giữ nguyên:

Student

Admin

Các route bảo vệ

Các quyền truy cập

Các giao diện theo role

Các chức năng Demo 1 đã hoàn thành

Không được biến Student thành Admin hoặc ngược lại.

Không được xóa hoặc thay đổi các trang giao diện theo role chỉ vì cập nhật tài khoản.

8. Không mở rộng phạm vi

Không tự ý thay đổi:

Chatbot

Model AI

PyTorch

Intent classification

Tài liệu

Knowledge

Feedback

History

Database khác không liên quan

UI Demo 1 không liên quan trực tiếp đến đăng nhập

Cơ chế Student/Admin

Chỉ sửa những phần thực sự cần thiết để đáp ứng task tài khoản sinh viên.

9. Kiểm tra bắt buộc

Phải kiểm tra ít nhất các tài khoản sau:

Tài khoản hợp lệ

2451220001 / 2451220001
2451220300 / 2451220300

2551220001 / 2551220001
2551220300 / 2551220300

2651220001 / 2651220001
2651220300 / 2651220300

Tài khoản không hợp lệ

Phải kiểm tra tài khoản:

Sai mã ngành

Sai khóa ngoài phạm vi 24–26

Sai số thứ tự ngoài 0001–0300

Username hợp lệ nhưng password sai

Các trường hợp không hợp lệ phải bị từ chối đăng nhập.

10. Kiểm tra dữ liệu

Phải xác nhận:

Khóa 24: 300 tài khoản
Khóa 25: 300 tài khoản
Khóa 26: 300 tài khoản
Tổng: 900 tài khoản

Không được có:

Trùng mã sinh viên

Thiếu mã trong khoảng 0001–0300

Sai mã ngành 5122

Sai khóa

Password mặc định không khớp mã sinh viên

11. Yêu cầu trước khi code

Codex phải:

Đọc AGENTS.md.

Đọc .agents/rules/.

Đọc .agents/skills/.

Đọc PROJECT_SPEC/.

Kiểm tra source hiện tại.

Xác định authentication đang nằm ở đâu.

Xác định dữ liệu tài khoản sinh viên đang được lưu ở đâu.

Xác định database/schema/seed hiện tại.

Xác định cơ chế phân quyền Student/Admin hiện tại.

Xác định chính xác những file cần sửa.

Sau đó cập nhật:

PROJECT_SPEC/HANDOFF/CURRENT_TASK.md
PROJECT_SPEC/HANDOFF/CODEX_PLAN.md

Ở bước PLAN không sửa source code.

12. Yêu cầu đối với kế hoạch Codex

CODEX_PLAN.md phải nêu rõ:

File nào sẽ sửa

File nào sẽ tạo nếu thật sự cần

Cách tạo 900 tài khoản

Cách đặt username

Cách đặt password mặc định

Cách giữ nguyên Student/Admin

Cách kiểm tra dữ liệu

Cách test login

Cách tránh ảnh hưởng Demo 1

Cách rollback nếu phát sinh lỗi

Không được đề xuất thay đổi ngoài phạm vi task.

13. Tiêu chí hoàn thành

Task chỉ được xem là hoàn thành khi:

Có đủ 900 tài khoản.

Đúng mã sinh viên.

Đúng ngành CNTT (5122).

Đúng khóa 24–26.

Đúng thứ tự 0001–0300.

Username = mã sinh viên.

Password mặc định = mã sinh viên.

Không còn phụ thuộc vào password 123456 cho các tài khoản mới.

Placeholder không chứa thông tin cá nhân bịa đặt.

Student/Admin vẫn hoạt động như trước.
Login hợp lệ hoạt động.

Login không hợp lệ bị từ chối.

Test thực tế đã chạy.

ANTIGRAVITY_REPORT.md ghi rõ kết quả.

Codex đã review độc lập.

### Sau này
- Các lớp/khóa CNTT khác.
- Các ngành khác của DAU.
- Các chức năng tra cứu rộng hơn.

Không mở rộng quá sớm nếu làm giảm chất lượng chức năng học tập cốt lõi.

## 4. Đăng nhập và cá nhân hóa

- Chỉ sinh viên đăng nhập, không ưu tiên đăng ký tự do.
- Giai đoạn thử nghiệm: mã sinh viên dùng làm thông tin đăng nhập ban đầu.
- Sau đăng nhập có thể đổi mật khẩu.
- Mã sinh viên có thể giúp xác định khóa/ngành/năm học tương đối.
- Ví dụ: 24..., 25..., 26... tương ứng khóa 2024, 2025, 2026.
- Chỉ dùng thông tin cá nhân thực tế khi có dữ liệu chính xác và cơ chế bảo vệ phù hợp.

## 5. Chức năng chatbot hiện tại

### Hội thoại
- Chào hỏi.
- Hội thoại cơ bản.
- Tiếng Việt.
- Tiếng Anh.

### Tài liệu
- Tìm tài liệu.
- Slide.
- Giáo trình.
- Bài tập.
- Đề thi/đề ôn tập.
- Tìm theo môn.
- Hỏi về nội dung tài liệu.

### Hỗ trợ học tập
- Trả lời kiến thức CNTT.
- Giải thích kiến thức.
- Hỗ trợ bài tập liên quan.
- Hỏi đáp dựa trên tài liệu.
- Hỏi tiếp nội dung liên quan.

### Tra cứu
- Một số thông tin dành cho sinh viên DAU.
- Học phí và các tra cứu khác vẫn là hướng phát triển, nhưng hiện tại học tập là trọng tâm.

## 6. Nguyên tắc trả lời

Thứ tự ưu tiên:

1. Đúng trọng tâm.
2. Không lạc đề.
3. Chính xác.
4. Có nguồn.
5. Có ngày cập nhật khi dữ liệu có thể thay đổi.
6. Vừa đủ ý, không dài dòng.

Khi phù hợp, câu trả lời nên có:

- Nội dung.
- Nguồn.
- Ngày cập nhật.
- Tài liệu liên quan.
- Gợi ý câu hỏi tiếp theo.

## 7. Khi không có thông tin

Không tự bịa dữ liệu.

Luồng:

**Knowledge nội bộ → tài liệu → kiến thức đáng tin cậy → nguồn Internet đáng tin cậy (nếu phù hợp) → thông báo không tìm thấy.**

Ví dụ:

> Tôi chưa tìm thấy thông tin phù hợp. Bạn có thể thử hỏi lại theo cách khác hoặc tìm trong tài liệu liên quan.

Mục tiêu là giảm hallucination.

## 8. Dữ liệu

Nguồn dữ liệu gồm:

- Dữ liệu trường.
- Học phí.
- Quy định/thủ tục.
- Liên hệ.
- Tài liệu CNTT.
- Knowledge.
- Dữ liệu intent.

Hiện tài liệu thật còn ít, vì vậy:

> Thiết kế hệ thống trước, bổ sung dữ liệu dần.

Ít dữ liệu có nguồn tốt hơn nhiều dữ liệu không xác minh.

## 9. Thông tin cũ

Các dữ liệu như học phí, quy định, lịch và thủ tục phải có:

- Nguồn.
- Ngày cập nhật.
- Trạng thái hiệu lực.
- Cảnh báo nếu đã cũ.

Không trình bày dữ liệu cũ như dữ liệu hiện hành.

## 10. Quản lý tài liệu và Admin

Admin quản lý:

- Sinh viên.
- Tài liệu.
- Môn học.
- Knowledge.
- Intent.
- Câu trả lời chatbot.
- Feedback.
- Lịch sử chat.
- Thống kê.
- Model AI.
- Retrain.

Nhập tài liệu:

- Form.
- Upload PDF/DOCX.

Admin có thể thêm intent đơn giản, ưu tiên intent về học tập và tài liệu. Khi thay đổi intent ảnh hưởng model thì phải retrain và kiểm thử lại.

## 11. AI hiện tại

Giữ kiến trúc chính:

**PyTorch + Bag of Words + Neural Network + Intent Classification**

Không thay toàn bộ ngay.

Ưu tiên cải thiện:

1. Dữ liệu intent.
2. Câu hỏi mẫu.
3. Confidence threshold.
4. OOS/OOV.
5. Retrieval.
6. Kiểm thử.
7. Retrain.

## 12. Lộ trình AI

### Giai đoạn 1
Bag of Words + Neural Network + Intent Classification.

### Giai đoạn 2
Embedding + Semantic Search để hiểu câu hỏi gần nghĩa.

### Giai đoạn 3
RAG cơ bản:

**Câu hỏi → tìm tài liệu → lấy đoạn liên quan → AI trả lời → nguồn**

### Giai đoạn 4
RAG nâng cao:

- Chunking.
- Embedding.
- Vector Database.
- Reranking.
- Context management.
- Citation.

## 13. Bộ nhớ hội thoại

Cho phép AI nhớ khoảng **10–15 câu hỏi gần nhất**.

Mục tiêu là hiểu câu hỏi tiếp theo mà không làm hệ thống quá chậm hoặc bị nhiễu.

Chỉ tiếp tục context khi câu hỏi mới liên quan câu trước. Nếu người dùng đổi chủ đề thì chuyển sang chủ đề mới.

Multi-intent phức tạp chưa phải ưu tiên; có thể phát triển sau.

## 14. Feedback

Sau câu trả lời có thể đánh giá hữu ích/không hữu ích.

Feedback dùng để:

- Phát hiện câu trả lời lỗi.
- Phát hiện intent nhầm.
- Bổ sung dữ liệu.
- Cải thiện retrieval.
- Retrain model.

Thống kê nên có:

- Tỷ lệ hữu ích.
- Intent có nhiều lỗi.
- Câu hỏi không nhận diện được.
- Chủ đề được hỏi nhiều.

## 15. Web

Web là yêu cầu bắt buộc.

Luồng chính:

```text
Login
  ↓
Dashboard
  ├── Chatbot
  ├── Tài liệu
  ├── Lịch sử
  └── Thông tin sinh viên

Admin
  ├── Sinh viên
  ├── Tài liệu
  ├── Knowledge
  ├── Intent
  ├── Feedback
  ├── Lịch sử
  ├── Thống kê
  └── Model/Retrain
```

## 16. Database

Database là yêu cầu bắt buộc.

Nên quản lý tối thiểu:

- User.
- Subject.
- Material.
- Knowledge.
- Intent.
- Chat history.
- Feedback.
- Model/retrain metadata nếu cần.

Có PK/FK hợp lý, timestamp và trạng thái active/inactive.

## 17. UML

Bắt buộc có:

1. Use Case Diagram.
2. Class Diagram.
3. Activity Diagram.
4. Sequence Diagram.
5. ERD/mô hình dữ liệu.

UML phải phản ánh source thực tế; không trình bày tính năng chưa triển khai như đã hoàn thành.

## 18. Kiểm thử

### AI
- Intent.
- Confidence.
- OOS/OOV.
- Retrieval.
- Câu hỏi gần nghĩa.
- Sai chính tả.
- Ngoài phạm vi.

### Chatbot
- Câu hỏi thường.
- Câu hỏi nối tiếp.
- Đổi chủ đề.
- Không có dữ liệu.
- Câu hỏi cần nguồn.
- Hỏi dựa trên tài liệu.

### Web
- Login.
- Đổi mật khẩu.
- Student/Admin.
- CRUD.
- Feedback.
- History.
- Upload.

### Database
- CRUD.
- PK/FK.
- Dữ liệu sai/thiếu.
- Active/inactive.

## 19. Demo

Không cần trình diễn quá nhiều chức năng. Nên tập trung:

```text
Sinh viên đăng nhập
      ↓
StudyBot nhận diện người dùng
      ↓
Hỏi tài liệu CNTT
      ↓
Tìm tài liệu
      ↓
Hỏi tiếp nội dung tài liệu
      ↓
Giải thích / hỗ trợ bài tập
      ↓
Nguồn + ngày cập nhật
      ↓
Hỏi sâu hơn
```

Điểm ấn tượng:

> Trả lời đúng trọng tâm + có căn cứ + hiểu câu hỏi tiếp theo + biết giới hạn của mình.

## 20. Tính năng nâng cao / “WOW”

Ưu tiên:

- Hỗ trợ học tập và đối đáp.
- RAG.
- PDF.
- Tìm kiếm thông minh.
- Cá nhân hóa.
- AI nâng cao.

Thứ tự triển khai:

1. Chatbot trả lời đúng.
2. Tài liệu hoạt động tốt.
3. Hỏi đáp dựa trên tài liệu.
4. Context 10–15 câu.
5. Nguồn + ngày cập nhật.
6. Semantic Search.
7. PDF.
8. RAG.
9. Cá nhân hóa nâng cao.

## 21. Không làm lan man

Không ưu tiên các chức năng không phục vụ mục tiêu:

- Thời tiết.
- Giải trí.
- Crypto/Bitcoin.
- Vàng/xổ số.
- Các chatbot chung chung không liên quan học tập.
- Tính năng chỉ để tăng số lượng chức năng.

Tiêu chí:

> Nếu không giúp sinh viên học tập hoặc tra cứu thông tin DAU thì chưa cần ưu tiên.

## 22. Tiến độ

- Làm cá nhân.
- Giảng viên theo dõi hằng tuần.
- Mỗi tuần kiểm tra, hỏi đáp và đánh giá tiến độ.
- Dự kiến khoảng 2 tháng hoàn thiện phiên bản hiện tại.

## 23. Mục tiêu chất lượng

Định hướng nghiêm túc như một sản phẩm có khả năng triển khai.

Yêu cầu:

- Code có cấu trúc.
- Database rõ ràng.
- AI có kiểm thử.
- Dữ liệu có nguồn.
- History/logging.
- Feedback.
- UML.
- Test.
- Tài liệu dự án.
- Có khả năng nâng cấp.

## 24. Kiến trúc định hướng

```text
Student
   ↓
Web/UI
   ↓
Authentication
   ↓
Chat API
   ↓
AI / Intent Classifier
(PyTorch + BoW + NN)
   ↓
Retrieval / Knowledge
   ↓
Materials / School Data / Database
   ↓
Answer + Source
   ↓
History + Feedback
```

## 25. Lộ trình triển khai

### Phase 1 — Ổn định nền tảng
- [ ] Kiểm tra source hiện tại.
- [ ] Chạy web end-to-end.
- [ ] Kiểm tra database.
- [ ] Login.
- [ ] Chatbot.
- [ ] Admin.
- [ ] Test.
- [ ] Sửa lỗi.

### Phase 2 — Học tập
- [ ] Hoàn thiện intent.
- [ ] Hoàn thiện tìm tài liệu.
- [ ] Bổ sung tài liệu CNTT.
- [ ] Hỏi đáp tài liệu.
- [ ] Fallback.
- [ ] Source.
- [ ] Updated date.

### Phase 3 — Context
- [ ] Context 10–15 câu.
- [ ] Theo dõi chủ đề.
- [ ] Đổi chủ đề.
- [ ] Gợi ý câu hỏi tiếp theo.

### Phase 4 — Semantic Search
- [ ] Embedding.
- [ ] Semantic retrieval.
- [ ] So sánh với keyword retrieval.
- [ ] Đánh giá.

### Phase 5 — PDF/RAG
- [ ] Upload PDF.
- [ ] Parse.
- [ ] Chunk.
- [ ] Embedding.
- [ ] Vector storage.
- [ ] Retrieval.
- [ ] Generate answer.
- [ ] Citation.

### Phase 6 — Hoàn thiện
- [ ] Bảo mật.
- [ ] Logging.
- [ ] Feedback analytics.
- [ ] Admin dashboard.
- [ ] UI.
- [ ] End-to-end test.
- [ ] UML.
- [ ] Báo cáo.
- [ ] Demo.

## 26. Tiêu chí hoàn thành

Không đánh dấu 100% chỉ vì source có nhiều chức năng.

Một chức năng chỉ được xem là hoàn thành khi:

- Có code.
- Có dữ liệu cần thiết.
- Chạy được.
- Có test.
- Không phá chức năng liên quan.
- Đã kiểm tra end-to-end.
- Tài liệu/UML phản ánh đúng thực tế.

Đặc biệt không đánh dấu Semantic Search, RAG hoặc Vector DB là hoàn thành nếu mới chỉ có trong roadmap.

## 27. Các quyết định còn cần chốt

1. Danh sách tài liệu thật và nguồn hợp pháp.
2. Môn học ưu tiên.
3. Cơ chế tìm kiếm Internet và danh sách nguồn đáng tin cậy.
4. Cách upload/parse PDF.
5. Công nghệ embedding/vector database khi bước RAG bắt đầu.
6. Dữ liệu sinh viên nào được phép dùng cho cá nhân hóa.
7. Quy tắc bảo mật dữ liệu cá nhân.
8. Bộ test chuẩn để đánh giá sau mỗi lần thay model.
9. Tiêu chí cụ thể để xác định “trả lời đúng trọng tâm”.
10. Cơ chế đánh dấu dữ liệu cũ/hết hiệu lực.

## 28. Định nghĩa sản phẩm cuối

> StudyBot là một trợ lý học tập web dành cho sinh viên CNTT DAU, cho phép sinh viên đăng nhập bằng mã sinh viên, tìm và khai thác tài liệu học tập, đặt câu hỏi về kiến thức và tài liệu, nhận câu trả lời ngắn gọn đúng trọng tâm, có nguồn và ngày cập nhật, đồng thời hiểu ngữ cảnh của một số câu hỏi gần nhất.

AI hiện tại:

**PyTorch + Bag of Words + Neural Network + Intent Classification**

Hướng nâng cấp:

**Embedding → Semantic Search → RAG → RAG nâng cao**

## 29. Nguyên tắc cuối

```text
Đừng làm chatbot biết tất cả.
Hãy làm chatbot biết rõ mình phục vụ ai,
biết dữ liệu nào mình có,
biết trả lời dựa trên nguồn,
biết nói “không biết” khi cần,
và hiểu sinh viên đang hỏi gì.
```

**Ưu tiên: Đúng trọng tâm → Đúng nguồn → Hữu ích → Có ngữ cảnh → Mở rộng.**

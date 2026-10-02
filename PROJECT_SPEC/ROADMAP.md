> **LƯU Ý:** Bản chính thức của Roadmap nằm ở root repository: STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md. File này là bản sao đồng bộ phục vụ mục đích vận hành.

# STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN

## 1. Mục tiêu cuối cùng

Hoàn thiện StudyBot thành một hệ thống chatbot hỗ trợ sinh viên có đầy đủ:

* Website cho sinh viên và Admin.
* Đăng nhập, phân quyền và quản lý tài khoản.
* 900 tài khoản sinh viên.
* Chatbot nhận diện `Intent`.
* Xử lý câu hỏi ngoài phạm vi (`OOS`) và từ không nhận diện được (`OOV`).
* Kho kiến thức (`Knowledge Base`).
* Tìm kiếm thông tin (`Retrieval`).
* Theo dõi ngữ cảnh hội thoại (`Context`).
* Câu hỏi tiếp nối (`Follow-up`).
* Quản lý dữ liệu từ Admin.
* Tải tài liệu PDF/DOCX/TXT lên hệ thống.
* Chia tài liệu thành các đoạn nhỏ (`Chunking`).
* Chuyển nội dung thành vector (`Embedding`).
* Tìm kiếm theo ngữ nghĩa (`Semantic Search`).
* Tìm kiếm kết hợp (`Hybrid Search`).
* Trả lời dựa trên tài liệu bằng `RAG`.
* Trích dẫn nguồn (`Citation`).
* Kiểm tra dữ liệu cũ/hết hạn.
* Phản hồi của người dùng (`Feedback`).
* Thống kê và giám sát hệ thống.
* Quản lý phiên bản Model.
* Kiểm thử toàn hệ thống.
* Bảo mật.
* UML, ERD và tài liệu triển khai.
* Chuẩn bị Demo và nghiệm thu cuối cùng.

---

# 2. Nguyên tắc Agent phải tuân thủ

### Nguyên tắc 1 — Không phá chức năng đang chạy

Nếu một chức năng đã hoạt động tốt thì **không được viết lại chỉ vì muốn đổi cách làm**.

Agent phải:

1. Kiểm tra chức năng hiện tại.
2. Viết/kiểm tra Test.
3. Chỉ sửa nếu thực sự cần.
4. Đảm bảo các chức năng cũ vẫn chạy sau khi sửa.

---

### Nguyên tắc 2 — Không làm RAG ngay từ đầu

Không được nhảy thẳng vào:

`PDF → Embedding → Vector DB → RAG`

Trước tiên phải ổn định:

`Code hiện tại → Data → Admin → AI V1 → Context → Document → Search → RAG`

---

### Nguyên tắc 3 — Mỗi chức năng phải có đủ 5 phần

Một Task chỉ được xem là hoàn thành khi có:

1. Code/Implementation.
2. Test.
3. Kiểm tra không gây lỗi chức năng cũ.
4. Cập nhật tài liệu.
5. Có bằng chứng kết quả.

---

### Nguyên tắc 4 — Nếu chức năng đã tồn tại

Agent phải phân loại:

* Đã hoàn chỉnh + có Test → giữ nguyên, đánh dấu `DONE`.
* Có chức năng nhưng chưa có Test → bổ sung Test.
* Có nhưng mới là Placeholder → hoàn thiện.
* Có nhưng khác Specification → xác định tài liệu nào là nguồn chính rồi mới sửa.
* Không tồn tại → triển khai mới.

Không được tạo thêm một phiên bản chức năng thứ hai chỉ vì chưa đọc kỹ code hiện tại.

---

# 3. Thứ tự triển khai chính thức

Agent phải thực hiện theo thứ tự:

**Phase 0 — Kiểm tra hiện trạng**

↓

**Phase 1 — Chuẩn hóa tài liệu**

↓

**Phase 2 — Kiểm tra Architecture và Database**

↓

**Phase 3 — Chuẩn hóa dữ liệu**

↓

**Phase 4 — Hoàn thiện Admin**

↓

**Phase 5 — Ổn định AI V1**

↓

**Phase 6 — Context**

↓

**Phase 7 — Follow-up**

↓

**Phase 8 — Tải và xử lý tài liệu**

↓

**Phase 9 — Chia tài liệu thành Chunk**

↓

**Phase 10 — Embedding**

↓

**Phase 11 — Semantic Search + Hybrid Search**

↓

**Phase 12 — RAG**

↓

**Phase 13 — Reranking**

↓

**Phase 14 — Knowledge Router**

↓

**Phase 15 — Trusted Source**

↓

**Phase 16 — Feedback và Analytics**

↓

**Phase 17 — Model Management**

↓

**Phase 18 — Security**

↓

**Phase 19 — Logging và Monitoring**

↓

**Phase 20 — Testing**

↓

**Phase 21 — AI Evaluation**

↓

**Phase 22 — Dataset Versioning**

↓

**Phase 23 — Hoàn thiện giao diện**

↓

**Phase 24 — UML / ERD**

↓

**Phase 25 — Deployment**

↓

**Phase 26 — Demo**

↓

**Phase 27 — Final QA và Release**

---

# PHASE 0 — KIỂM TRA HIỆN TRẠNG

## P0-001 — Kiểm tra trạng thái hiện tại

Trước khi sửa code:

* Chạy toàn bộ Test hiện có.
* Kiểm tra Flask app.
* Kiểm tra Database.
* Kiểm tra đăng nhập.
* Kiểm tra Student.
* Kiểm tra Admin.
* Kiểm tra Chatbot.
* Kiểm tra Retrieval.
* Kiểm tra Feedback.
* Kiểm tra History.
* Kiểm tra 900 tài khoản.

Tạo:

`docs/audit/BASELINE.md`

Ghi lại:

* Chức năng đang hoạt động.
* Chức năng lỗi.
* Chức năng thiếu.
* Test đã có.
* Test chưa có.
* Các vấn đề phát hiện.

---

## P0-002 — Kiểm tra toàn bộ Repository

Agent phải đọc toàn bộ cấu trúc dự án và xác định:

* Flask app nằm ở đâu.
* Route nằm ở đâu.
* Service nằm ở đâu.
* Model nằm ở đâu.
* AI code nằm ở đâu.
* Knowledge Base nằm ở đâu.
* Test nằm ở đâu.
* File cấu hình nằm ở đâu.
* Model AI nằm ở đâu.
* Database được tạo/migrate như thế nào.

Không được triển khai tính năng mới trước khi hiểu cấu trúc hiện tại.

---

## P0-003 — Kiểm tra và thống nhất tài liệu

Đối chiếu:

* `README.md`
* `README_V2.md`
* `MASTER_PROJECT_SPECIFICATION.md`
* `PROJECT_SPEC/...`
* `CURRENT_STATUS.md`
* `TASK_QUEUE.md`
* `ROADMAP.md`
* `CHANGELOG.md`
* Handoff documents.

Tạo một tài liệu chính thức duy nhất:

`docs/MASTER_SPECIFICATION.md`

Các tài liệu cũ nếu còn cần giữ thì chuyển thành tài liệu tham khảo/archive.

Đặc biệt phải giải quyết các số liệu AI không thống nhất, ví dụ kết quả `OOS`.

---

# PHASE 1 — CHUẨN HÓA TÀI LIỆU

## P1-001 — Chuẩn hóa Architecture

Tạo tài liệu mô tả:

```text
Browser
   ↓
Flask Routes
   ↓
Service Layer
   ↓
AI / Retrieval / Knowledge
   ↓
Database / Files / Vector Store
```

Ghi rõ trách nhiệm của từng thành phần.

---

## P1-002 — Kiểm tra Database

Kiểm tra các Model hiện có:

* User
* Subject
* Material
* KnowledgeItem
* ChatMessage
* Feedback

Xác định:

* Quan hệ giữa các bảng.
* Primary Key.
* Foreign Key.
* Index.
* Unique constraint.
* Nullable field.
* Migration.

---

## P1-003 — Dọn Migration

Nếu Database có Migration:

* Kiểm tra lịch sử.
* Xóa Migration lỗi nếu cần.
* Không làm mất dữ liệu hợp lệ.
* Đảm bảo tạo Database mới vẫn hoạt động.

---

# PHASE 2 — CHUẨN HÓA KNOWLEDGE BASE

## P2-001 — Chuẩn hóa cấu trúc Knowledge

Mỗi Knowledge Item nên có:

* `id`
* `category`
* `title`
* `content`
* `source`
* `source_type`
* `updated_at`
* `status`
* `valid_from`
* `valid_until`

Có thể bổ sung:

* `created_at`
* `created_by`
* `updated_by`

---

## P2-002 — Quản lý nguồn dữ liệu

Phân biệt:

* Dữ liệu do Admin nhập.
* Dữ liệu từ Database.
* Dữ liệu từ tài liệu.
* Dữ liệu từ Website đáng tin cậy.

Mỗi nguồn phải có thông tin để truy xuất lại.

---

## P2-003 — Phát hiện dữ liệu cũ

Xây dựng cơ chế:

**Dữ liệu còn hiệu lực / sắp cũ / đã cũ / hết hạn**

Ví dụ:

```text
VALID
WARNING
STALE
EXPIRED
```

Thời gian hết hạn phải có thể cấu hình.

---

## P2-004 — Hiển thị nguồn

Khi chatbot trả lời dựa trên Knowledge Base:

* Cho biết nguồn.
* Cho biết thời gian cập nhật nếu cần.
* Không được tự tạo nguồn.

---

# PHASE 3 — HOÀN THIỆN ADMIN

## P3-001 — Subject CRUD

Admin có thể:

* Thêm môn học.
* Sửa môn học.
* Xem môn học.
* Xóa/ẩn môn học.
* Quản lý mã môn.
* Quản lý tên môn.
* Quản lý alias/keyword.

---

## P3-002 — Intent CRUD

Admin có thể:

* Xem Intent.
* Thêm Intent.
* Sửa Intent.
* Xóa/ẩn Intent.
* Quản lý training examples.
* Xem trạng thái Intent.

Không được sửa trực tiếp dữ liệu AI mà không có kiểm tra.

---

## P3-003 — Quản lý tài liệu

Admin có thể:

* Xem tài liệu.
* Tải file lên.
* Xem trạng thái xử lý.
* Xóa tài liệu.
* Ẩn tài liệu.
* Khôi phục tài liệu.
* Xem nguồn.
* Xem ngày cập nhật.

---

## P3-004 — Hoàn thiện Admin

Admin Dashboard phải có khả năng theo dõi:

* Sinh viên.
* Môn học.
* Knowledge.
* Intent.
* Tài liệu.
* Hội thoại.
* Feedback.
* Model.
* Thống kê hệ thống.

---

# PHASE 4 — ỔN ĐỊNH AI V1

## P4-001 — Đánh giá Intent

Giữ hệ thống Intent hiện tại nếu đang hoạt động tốt.

Đánh giá:

* Accuracy.
* Precision.
* Recall.
* F1.
* Confusion Matrix.

Không chỉ nhìn Accuracy.

---

## P4-002 — Đánh giá OOS

Tạo Dataset riêng cho câu hỏi ngoài phạm vi.

Ví dụ:

* Câu hỏi về thể thao.
* Tin tức.
* Giải trí.
* Chính trị.
* Chủ đề không liên quan đến StudyBot.

Đánh giá:

* Có nhận ra OOS hay không.
* Có trả lời linh tinh hay không.
* Có từ chối đúng cách hay không.

---

## P4-003 — Đánh giá OOV

Kiểm tra:

* Từ viết sai.
* Không dấu.
* Viết tắt.
* Từ lạ.
* Tiếng Anh.
* Từ không tồn tại trong Vocabulary.

---

## P4-004 — Đánh giá Retrieval

Kiểm tra:

* Subject code.
* Subject name.
* Alias.
* Keyword.
* Không dấu.
* Viết tắt.
* Từ đồng nghĩa.

Lưu kết quả đánh giá thành Dataset có thể chạy lại.

---

# PHASE 5 — CONTEXT

## P5-001 — Lưu Context

Chatbot phải có khả năng nhớ khoảng **10–15 lượt hội thoại gần nhất**.

Context nên chứa:

* Câu hỏi hiện tại.
* Câu hỏi trước.
* Intent trước.
* Subject hiện tại.
* Tài liệu vừa tìm được.
* Entity liên quan.
* Chủ đề hiện tại.

---

## P5-002 — Context Resolver

Ví dụ:

> Sinh viên: Môn CNPM học gì?

Chatbot trả lời.

> Sinh viên: Còn điều kiện tiên quyết?

Chatbot phải hiểu:

> "điều kiện tiên quyết của môn CNPM"

không phải một câu hỏi hoàn toàn mới.

---

## P5-003 — Giữ chủ đề

Nếu người dùng tiếp tục hỏi về cùng một môn:

```text
CNPM
↓
nội dung
↓
điều kiện
↓
tài liệu
↓
đề cương
```

Chatbot phải duy trì đúng Subject.

---

## P5-004 — Chuyển chủ đề

Nếu người dùng chuyển:

```text
CNPM
→
Python
```

Chatbot phải cập nhật Context sang Python.

Không được tiếp tục lấy dữ liệu của CNPM.

---

# PHASE 6 — FOLLOW-UP

## P6-001 — Tạo Follow-up

Sau khi trả lời, chatbot có thể đề xuất câu hỏi tiếp theo dựa trên:

* Intent.
* Subject.
* Context.
* Nội dung vừa tìm được.

Ví dụ:

> Bạn có muốn xem **điều kiện tiên quyết** của môn này không?

Hoặc:

> Bạn có muốn xem **tài liệu học tập** không?

---

## P6-002 — Kiểm tra Follow-up

Đảm bảo Follow-up:

* Liên quan câu hỏi.
* Không lặp vô nghĩa.
* Không dẫn sang chủ đề sai.
* Có thể click và tiếp tục hội thoại.

---

# PHASE 7 — TẢI VÀ XỬ LÝ TÀI LIỆU

## P7-001 — Tải file lên

Cho phép Admin tải:

* PDF.
* DOCX.
* TXT.

Kiểm tra:

* Định dạng.
* Dung lượng.
* Tên file.
* Nội dung.
* File lỗi.
* File độc hại.

---

## P7-002 — Đọc PDF

Hệ thống phải:

1. Nhận file.
2. Đọc nội dung.
3. Xác định trang.
4. Trích xuất text.
5. Chuẩn hóa text.
6. Lưu metadata.

Nếu PDF không có text hoặc bị lỗi phải báo rõ.

---

## P7-003 — Đọc DOCX

Trích xuất:

* Paragraph.
* Heading.
* Table nếu cần.
* Metadata.

---

## P7-004 — Metadata tài liệu

Mỗi tài liệu cần lưu:

* Tên file.
* Loại file.
* Người tải.
* Thời gian tải.
* Nguồn.
* Môn học.
* Phiên bản.
* Trạng thái xử lý.

---

# PHASE 8 — CHUNKING

## P8-001 — Chia tài liệu

Không đưa cả tài liệu lớn vào một lần.

Chia thành các `Chunk` nhỏ theo:

* Heading.
* Paragraph.
* Section.
* Page.

Có thể dùng overlap giữa các Chunk nếu cần.

---

## P8-002 — Metadata của Chunk

Mỗi Chunk phải biết:

* Document ID.
* Page.
* Section.
* Chunk ID.
* Nội dung.
* Vị trí trong tài liệu.

Mục đích là sau này chatbot có thể nói chính xác:

> Thông tin này nằm trong tài liệu X, trang Y.

---

## P8-003 — Test Chunking

Test với:

* Tài liệu ngắn.
* Tài liệu dài.
* Heading.
* Bảng.
* PDF nhiều trang.
* DOCX.
* File lỗi.

---

# PHASE 9 — EMBEDDING

## P9-001 — Xây dựng Embedding Service

Chọn Model Embedding phù hợp với tiếng Việt.

Embedding Service phải có thể:

* Chuyển câu hỏi thành vector.
* Chuyển Chunk thành vector.
* Lưu Model version.
* Chạy lại khi đổi Model.

---

## P9-002 — Vector Store

Chọn một Vector Store phù hợp với quy mô StudyBot.

Lưu:

```text
chunk_id
embedding
document_id
metadata
model_version
```

---

## P9-003 — Indexing

Khi tài liệu được xử lý:

```text
File
→ Text
→ Chunk
→ Embedding
→ Vector Store
```

---

## P9-004 — Re-indexing

Khi:

* Đổi Embedding Model.
* Tài liệu thay đổi.
* Chunking thay đổi.

Có thể chạy lại Index.

---

# PHASE 10 — SEMANTIC SEARCH

## P10-001 — Semantic Search

Cho phép tìm theo ý nghĩa thay vì chỉ tìm từ giống nhau.

Ví dụ:

> "môn này cần học trước môn nào?"

vẫn có thể tìm ra nội dung:

> "điều kiện tiên quyết".

---

## P10-002 — Hybrid Search

Không bỏ Retrieval hiện tại.

Kết hợp:

```text
Keyword Search
+
Semantic Search
+
Metadata
```

Sau đó tính điểm và xếp hạng kết quả.

---

## P10-003 — Đánh giá Retrieval

Dataset phải có:

* Câu hỏi chính xác.
* Câu hỏi viết lại.
* Câu hỏi không dấu.
* Câu hỏi sai chính tả.
* Từ đồng nghĩa.
* Câu hỏi dài/ngắn.
* Tiếng Việt + tiếng Anh.

Đánh giá:

* Recall@K.
* Precision@K.
* MRR.
* Top-1.
* Top-3.
* Top-5.

---

# PHASE 11 — RAG

## P11-001 — Xây dựng RAG Pipeline

Pipeline chính:

```text
User Question
      ↓
Intent
      ↓
Context
      ↓
Query Reformulation
      ↓
Hybrid Search
      ↓
Top-K Chunks
      ↓
Reranking
      ↓
Prompt
      ↓
LLM
      ↓
Grounded Answer
      ↓
Citation
```

---

## P11-002 — Grounding

Chatbot chỉ được trả lời dựa trên thông tin có trong nguồn được truy xuất.

Nếu không có đủ thông tin:

> Không tìm thấy thông tin phù hợp trong dữ liệu hiện có.

Không được tự bịa.

---

## P11-003 — Citation

Câu trả lời phải có thể chỉ ra:

* Tên tài liệu.
* Trang.
* Section.
* Nguồn.

Tùy loại dữ liệu mà hiển thị mức Citation phù hợp.

---

## P11-004 — Chống Hallucination

Test các trường hợp:

* Không có tài liệu.
* Tài liệu không liên quan.
* Câu hỏi ngoài phạm vi.
* Tài liệu thiếu thông tin.
* Hai tài liệu mâu thuẫn.

Mục tiêu là chatbot **thà nói không biết còn hơn tự tạo thông tin**.

---

# PHASE 12 — RERANKING

## P12-001 — Reranking

Nếu Hybrid Search trả về nhiều kết quả:

```text
Top 20
↓
Reranker
↓
Top 5
```

Chỉ triển khai nếu Evaluation cho thấy có lợi ích thực tế.

---

## P12-002 — Đánh giá Reranking

So sánh:

```text
Không Reranking
vs
Có Reranking
```

Dựa trên Dataset Retrieval.

Nếu không cải thiện đáng kể thì không cần ép sử dụng.

---

# PHASE 13 — KNOWLEDGE ROUTER

## P13-001 — Knowledge Router

Xác định câu hỏi nên lấy dữ liệu từ đâu:

```text
Structured Data
      ↓
Knowledge Base
      ↓
Material Search
      ↓
RAG
      ↓
Trusted Web
```

Không phải câu hỏi nào cũng cần RAG.

---

## P13-002 — Source Priority

Thiết lập thứ tự ưu tiên nguồn.

Ví dụ:

```text
Dữ liệu chính thức của hệ thống
        ↓
Knowledge Base
        ↓
Tài liệu môn học
        ↓
Nguồn Web đáng tin cậy
```

---

# PHASE 14 — TRUSTED SOURCE

## P14-001 — Nguồn Web đáng tin cậy

Nếu hệ thống cần lấy thông tin bên ngoài:

* Chỉ sử dụng nguồn được phép.
* Ghi URL.
* Ghi thời gian lấy dữ liệu.
* Ghi nguồn.

---

## P14-002 — Kiểm tra nguồn

Không được sử dụng nguồn:

* Không xác định.
* Không thể kiểm chứng.
* Có nội dung đáng ngờ.
* Không phù hợp với câu hỏi.

---

# PHASE 15 — FEEDBACK

## P15-001 — Phân loại Feedback

Ngoài:

* Helpful.
* Unhelpful.

Có thể phân loại:

* Sai Intent.
* Sai Retrieval.
* Thông tin cũ.
* Thiếu thông tin.
* Trả lời không đúng.
* Hallucination.
* Không hiểu Context.

---

## P15-002 — Feedback Analytics

Admin có thể xem:

* Intent có nhiều lỗi.
* Câu hỏi hay bị lỗi.
* Tài liệu hay bị truy xuất sai.
* Câu hỏi OOS.
* Tỷ lệ Helpful/Unhelpful.
* Các lỗi phổ biến.

---

## P15-003 — Cải thiện từ Feedback

Feedback được sử dụng để:

```text
Feedback
→ Phân tích
→ Sửa Dataset / Knowledge
→ Test
→ Retrain nếu cần
→ Evaluation
```

Không được tự động lấy mọi Feedback đưa thẳng vào Training Dataset.

---

# PHASE 16 — MODEL MANAGEMENT

## P16-001 — Model Registry

Quản lý:

* Model ID.
* Version.
* Dataset version.
* Metrics.
* Ngày tạo.
* Người tạo.
* Trạng thái.

---

## P16-002 — Model Versioning

Ví dụ:

```text
Model V1
Model V2
Model V3
```

Không ghi đè Model cũ.

---

## P16-003 — Quy trình Retrain

Quy trình:

```text
Dataset
↓
Train
↓
Evaluate
↓
READY
↓
Activate
```

Không được đưa Model chưa Evaluate vào sử dụng.

---

## P16-004 — Rollback

Nếu Model mới lỗi:

```text
Model V3
↓
Rollback
↓
Model V2
```

---

# PHASE 17 — SECURITY

## P17-001 — Kiểm tra Security

Kiểm tra:

* Authentication.
* Authorization.
* Session.
* Password.
* CSRF nếu phù hợp.
* XSS.
* SQL Injection.
* Input Validation.
* Path Traversal.
* File Upload.

---

## P17-002 — Bảo mật file tải lên

Không cho phép người dùng tải lên file nguy hiểm.

Kiểm tra:

* Extension.
* MIME type.
* Dung lượng.
* Nội dung.
* Tên file.
* Đường dẫn lưu.

---

## P17-003 — Kiểm tra phân quyền

Đảm bảo:

```text
Student
≠
Admin
```

Student không được truy cập:

* Admin Dashboard.
* Quản lý User.
* Knowledge Management.
* Document Management.
* Model Management.

---

# PHASE 18 — LOGGING VÀ MONITORING

## P18-001 — Logging

Ghi Log các sự kiện quan trọng:

* Login.
* Logout.
* Chat.
* Error.
* Upload.
* Retrain.
* Admin action.

Không ghi Password hoặc dữ liệu nhạy cảm vào Log.

---

## P18-002 — Metrics

Theo dõi:

* Số câu hỏi.
* Response time.
* OOS rate.
* OOV rate.
* Retrieval hit rate.
* Feedback.
* Error rate.
* RAG usage.
* Citation rate.

---

## P18-003 — Error Monitoring

Các lỗi nghiêm trọng phải dễ phát hiện và truy vết.

---

# PHASE 19 — TESTING

## P19-001 — Unit Test

Test:

* Intent.
* OOS.
* OOV.
* Retrieval.
* Context.
* Chunking.
* Embedding.
* Search.
* RAG.

---

## P19-002 — Integration Test

Kiểm tra luồng:

```text
Login
→ Dashboard
→ Chat
→ Retrieval
→ Answer
→ Feedback
→ History
```

---

## P19-003 — E2E Test

Test như người dùng thật.

### Student:

```text
Login
→ Chat
→ Hỏi câu hỏi
→ Follow-up
→ Xem History
→ Feedback
→ Logout
```

### Admin:

```text
Login
→ Dashboard
→ Quản lý Student
→ Quản lý Knowledge
→ Tải tài liệu
→ Kiểm tra xử lý
→ Xem Chat
→ Xem Feedback
→ Logout
```

---

## P19-004 — Regression Test

Sau mỗi thay đổi lớn:

**Phải chạy lại toàn bộ Test quan trọng.**

---

# PHASE 20 — AI EVALUATION

## P20-001 — Dataset Intent

Tạo Dataset chuẩn:

```text
Question
Expected Intent
```

Có nhiều cách viết khác nhau cho cùng Intent.

---

## P20-002 — Dataset Retrieval

Tạo:

```text
Question
Expected Document/Chunk
```

Dùng để đo:

* Recall@K.
* Precision@K.
* MRR.

---

## P20-003 — Dataset RAG

Đánh giá:

* Correctness.
* Groundedness.
* Citation.
* Refusal khi thiếu thông tin.

---

## P20-004 — Dataset OOS

Dataset OOS phải tách khỏi Training Dataset.

Mục đích:

**Đánh giá khả năng nhận biết câu hỏi ngoài phạm vi một cách công bằng.**

---

# PHASE 21 — DATASET VERSIONING

## P21-001 — Phiên bản Dataset

Ví dụ:

```text
dataset_v1
dataset_v2
dataset_v3
```

Mỗi Model phải biết nó được Train từ Dataset nào.

---

## P21-002 — Phiên bản Evaluation

Lưu:

```text
Model Version
+
Dataset Version
+
Evaluation Result
```

để sau này biết tại sao Model mới tốt/xấu hơn Model cũ.

---

# PHASE 22 — HOÀN THIỆN UI/UX

## P22-001 — Giao diện Student

Kiểm tra:

* Login.
* Dashboard.
* Chat.
* Materials.
* History.
* Info.
* Change Password.

---

## P22-002 — Giao diện Chat

Chat phải thể hiện rõ:

* Câu hỏi.
* Câu trả lời.
* Loading.
* Error.
* Source/Citation.
* Follow-up.
* Feedback.

---

## P22-003 — Giao diện Admin

Admin cần có:

* Dashboard.
* Students.
* Subjects.
* Knowledge.
* Materials.
* Documents.
* Intents.
* Conversations.
* Feedback.
* Models.
* System Status.

---

# PHASE 23 — UML / ERD

## P23-001 — Use Case Diagram

Thể hiện:

* Student.
* Admin.
* Chatbot.
* Các chức năng chính.

---

## P23-002 — Class Diagram

Thể hiện các Class quan trọng:

* User.
* Student.
* Admin.
* Subject.
* Material.
* KnowledgeItem.
* ChatMessage.
* Feedback.
* Document.
* Chunk.
* ModelVersion.

---

## P23-003 — Activity Diagram

Vẽ các luồng:

* Login.
* Chat.
* Upload tài liệu.
* RAG.

---

## P23-004 — Sequence Diagram

Đặc biệt cần có:

```text
Student
→ Flask
→ AI
→ Retrieval
→ RAG
→ Knowledge
→ Response
```

---

## P23-005 — ERD

Vẽ quan hệ Database đầy đủ.

---

# PHASE 24 — DEPLOYMENT

## P24-001 — Tài liệu cài đặt

Viết rõ:

* Requirements.
* Python version.
* Dependencies.
* Database.
* Environment variables.
* AI Model.
* Vector Store.
* Cách chạy.

---

## P24-002 — Tài liệu Production

Mô tả:

* Server.
* Database.
* Storage.
* Model.
* Backup.
* Security.
* Logging.

---

## P24-003 — Backup / Restore

Phải có hướng dẫn:

```text
Backup
↓
Lưu
↓
Restore
↓
Kiểm tra
```

---

# PHASE 25 — CHUẨN BỊ DEMO

## P25-001 — Kịch bản Demo

Chuẩn bị các tình huống:

### Demo 1

Student đăng nhập.

### Demo 2

Hỏi câu hỏi thông thường.

### Demo 3

Hỏi câu hỏi tiếp nối để chứng minh Context.

### Demo 4

Hỏi câu hỏi từ tài liệu PDF/DOCX.

### Demo 5

Hiển thị Citation.

### Demo 6

Hỏi câu ngoài phạm vi để chứng minh OOS.

### Demo 7

Admin tải tài liệu lên.

### Demo 8

Admin xem Feedback.

### Demo 9

Admin quản lý Knowledge.

### Demo 10

Retrain / Model Version.

---

## P25-002 — Chuẩn bị dữ liệu Demo

Đảm bảo Demo có:

* User.
* Subject.
* Knowledge.
* Document.
* Chunk.
* Embedding.
* Model.
* Feedback.

---

## P25-003 — Demo Checklist

Trước khi Demo phải kiểm tra:

* Server chạy.
* Database chạy.
* Model tồn tại.
* Vector Store tồn tại.
* Tài liệu tồn tại.
* Account tồn tại.
* Không có lỗi Console nghiêm trọng.

---

# PHASE 26 — FINAL QA

## P26-001 — Kiểm tra cuối

Kiểm tra 7 nhóm:

### 1. Chức năng

Tất cả chức năng chính hoạt động.

### 2. AI

Intent, OOS, OOV, Retrieval, Context, RAG hoạt động.

### 3. Data

Knowledge có nguồn và ngày cập nhật.

### 4. Security

Không có lỗi nghiêm trọng.

### 5. Testing

Test quan trọng đều Pass.

### 6. Documentation

Tài liệu khớp với Code.

### 7. Deployment

Có thể cài đặt và chạy lại hệ thống.

---

## P26-002 — Regression cuối

Chạy toàn bộ Test Suite.

Không được Release nếu có Regression nghiêm trọng.

---

## P26-003 — Hoàn thiện Documentation

Đảm bảo:

```text
Code
=
Test
=
Documentation
=
Actual behavior
```

Không được để README nói một đằng nhưng hệ thống chạy một nẻo.

---

## P26-004 — RELEASE

Khi tất cả đạt yêu cầu:

```text
Development
↓
Testing
↓
Final QA
↓
Release Candidate
↓
Demo
↓
Release
```

---

# 4. Các Task ID chính thức

Agent phải sử dụng các Task ID sau để theo dõi:

```text
P0-001 → P0-003

P1-001 → P1-003

P2-001 → P2-004

P3-001 → P3-004

P4-001 → P4-004

P5-001 → P5-004

P6-001 → P6-002

P7-001 → P7-004

P8-001 → P8-003

P9-001 → P9-004

P10-001 → P10-003

P11-001 → P11-004

P12-001 → P12-002

P13-001 → P13-002

P14-001 → P14-002

P15-001 → P15-003

P16-001 → P16-004

P17-001 → P17-003

P18-001 → P18-003

P19-001 → P19-004

P20-001 → P20-004

P21-001 → P21-002

P22-001 → P22-003

P23-001 → P23-005

P24-001 → P24-003

P25-001 → P25-003

P26-001 → P26-004
```

---

# 5. Cách Agent phải thực hiện từng Task

Với **mỗi Task**, Agent bắt buộc thực hiện theo thứ tự:

### Bước 1 — Đọc code hiện tại

Không được giả định chức năng chưa tồn tại.

### Bước 2 — Đọc Specification liên quan

Xác định chính xác yêu cầu.

### Bước 3 — Kiểm tra Dependency

Xem Task này phụ thuộc Task nào.

### Bước 4 — Thực hiện

Triển khai đúng phạm vi.

### Bước 5 — Viết Test

Test chức năng mới.

### Bước 6 — Chạy Test

Kiểm tra kết quả.

### Bước 7 — Sửa Regression

Nếu chức năng cũ bị hỏng thì phải sửa trước khi tiếp tục.

### Bước 8 — Cập nhật Documentation

Cập nhật tài liệu liên quan.

### Bước 9 — Ghi Evidence

Ghi:

* Đã sửa gì.
* File nào thay đổi.
* Test nào chạy.
* Kết quả.
* Vấn đề còn lại.

### Bước 10 — Đánh dấu Task

Chỉ được đánh:

```text
DONE
```

khi Task thực sự hoàn thành.

---

# 6. Báo cáo sau mỗi Phase

Sau mỗi Phase, Agent phải báo cáo theo mẫu:

```text
PHASE: P5 — CONTEXT

Completed:
- P5-001
- P5-002

Changed:
- ...
- ...

Tests:
- ...
- ...

Passed:
- ...

Failed:
- ...

Known Issues:
- ...

Next:
- P5-003
```

Không được chỉ báo:

> "Phase hoàn thành."

mà không có bằng chứng.

---

# 7. Mức độ ưu tiên

## P0 — Bắt buộc

Phải hoàn thành:

* Audit.
* Documentation.
* Data Quality.
* Testing.
* Security.
* Regression.

---

## P1 — Chức năng cốt lõi

Phải hoàn thành:

* Context.
* Follow-up.
* Admin.
* Document Upload.
* Chunking.
* Embedding.
* Semantic Search.
* Hybrid Search.
* RAG.
* Citation.

---

## P2 — Chức năng nâng cao

Có thể triển khai sau:

* Reranking.
* Trusted Web.
* Model Registry nâng cao.
* Analytics nâng cao.
* Personalization nâng cao.

---

# 8. Các mốc Release

## Release 0 — Stable V1

Phải có:

* Website.
* Login.
* Student/Admin.
* 900 tài khoản.
* Chatbot.
* Intent.
* OOS.
* OOV.
* Retrieval.
* Knowledge Base.
* History.
* Feedback.

---

## Release 1 — Context V1

Thêm:

* Context.
* Topic continuity.
* Topic switching.
* Follow-up.
* Data freshness.
* OOS/OOV được đánh giá tốt hơn.

---

## Release 2 — RAG V1

Thêm:

```text
PDF/DOCX
↓
Text
↓
Chunk
↓
Embedding
↓
Semantic Search
↓
Hybrid Search
↓
RAG
↓
Citation
```

---

## Release 3 — FINAL

Bao gồm:

* Admin hoàn chỉnh.
* Model Management.
* Feedback Analytics.
* Security.
* Logging.
* Monitoring.
* Testing đầy đủ.
* AI Evaluation.
* Dataset Versioning.
* UML.
* ERD.
* Deployment Documentation.
* Demo.
* Final QA.

---

# 9. Definition of Done

StudyBot chỉ được xem là **hoàn thành toàn bộ** khi đáp ứng đồng thời:

### Chức năng

Các chức năng chính hoạt động đúng.

### AI

Có:

* Intent.
* OOS.
* OOV.
* Retrieval.
* Context.
* Follow-up.
* Semantic Search.
* Hybrid Search.
* RAG.
* Citation.

### Data

Có:

* Source.
* Updated time.
* Status.
* Stale detection.

### Admin

Có khả năng quản lý:

* Student.
* Subject.
* Knowledge.
* Material.
* Document.
* Intent.
* Conversation.
* Feedback.
* Model.

### Security

Đã kiểm tra các lỗi bảo mật quan trọng.

### Testing

Có:

* Unit Test.
* Integration Test.
* E2E Test.
* Regression Test.
* AI Evaluation.

### Documentation

Có:

* Specification.
* README.
* Architecture.
* UML.
* ERD.
* Deployment Guide.
* Backup/Restore.

### Release

Có:

* Demo Scenario.
* Demo Data.
* Final QA.
* Release Checklist.

---

# 10. Quy tắc quan trọng nhất cho Agent

**Không được chạy theo số lượng Task.**

Mục tiêu không phải là:

```text
P0 → P1 → P2 → ... → P26
```

mà là:

```text
Requirement
↓
Implementation
↓
Test
↓
Integration
↓
Documentation
↓
Evidence
↓
DONE
```

Nếu một chức năng **đã có sẵn và hoạt động tốt**, Agent phải tận dụng lại.

Nếu một chức năng **chưa hoàn chỉnh**, Agent phải hoàn thiện nó.

Nếu một chức năng **không tồn tại**, Agent mới triển khai mới.

Nếu Specification và Code mâu thuẫn, Agent phải **dừng để xác định nguồn yêu cầu chính thức**, không tự ý chọn một bên.

---

# 11. Thứ tự thực hiện cuối cùng — Bản cực ngắn

Agent có thể dùng chuỗi sau làm checklist tổng:

```text
1. Kiểm tra hiện trạng
2. Chạy Test hiện tại
3. Chuẩn hóa tài liệu
4. Kiểm tra Architecture
5. Kiểm tra Database
6. Chuẩn hóa Knowledge
7. Hoàn thiện Admin
8. Ổn định AI V1
9. Xây Context
10. Xây Follow-up
11. Tải tài liệu
12. Đọc PDF/DOCX
13. Chunking
14. Embedding
15. Semantic Search
16. Hybrid Search
17. RAG
18. Citation
19. Reranking
20. Knowledge Router
21. Trusted Source
22. Feedback Analytics
23. Model Management
24. Security
25. Logging/Monitoring
26. Testing
27. AI Evaluation
28. Dataset Versioning
29. Hoàn thiện UI
30. UML/ERD
31. Deployment
32. Demo
33. Final QA
34. Release
```

**Đây là thứ tự chính thức để Agent triển khai StudyBot. Không đảo thứ tự các nhóm lớn nếu chưa kiểm tra Dependency.**

# Documentation Consolidation Evidence

## Status
DONE

## Official Master Spec
`STUDYBOT_MASTER_PROJECT_SPECIFICATION.md` (tại thư mục root)

## Official Roadmap
`STUDYBOT — KẾ HOẠCH TRIỂN KHAI HOÀN THIỆN TOÀN BỘ DỰ ÁN.md` (tại thư mục root)

## Operational Documents
- `PROJECT_SPEC/TASK_QUEUE.md`
- `PROJECT_SPEC/CURRENT_STATUS.md`
- `PROJECT_SPEC/DECISIONS.md`
- `PROJECT_SPEC/STUDYBOT_PROGRESS_TRACKER.md`

## Documents Classified as Legacy/Duplicate
- `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` (DUPLICATE / REFERENCE - Đã được đồng bộ nội dung từ file chuẩn ở root và gắn header lưu ý).
- `PROJECT_SPEC/ROADMAP.md` (DUPLICATE / REFERENCE - Đã được đồng bộ nội dung từ bản Kế hoạch 27 Phase ở root và gắn header lưu ý).
- `README.md` (LEGACY - Đang chứa dữ liệu account giả cũ `24ct2001 / 123456`, cần update trong task sau).
- `README_V2.md` (LEGACY - Hướng dẫn giải nén cũ).

## Intentional Changes of This Task

Các file được sửa **có chủ đích** bởi Documentation Consolidation task:

- `PROJECT_SPEC/MASTER_PROJECT_SPECIFICATION.md` — Ghi đè nội dung từ root + Header lưu ý; bao gồm đầy đủ requirement 900 accounts.
- `PROJECT_SPEC/ROADMAP.md` — Ghi đè nội dung từ root + Header lưu ý; phản ánh 27 Phases / 89 Tasks.
- `PROJECT_SPEC/TASK_QUEUE.md` — Ghi nhận P0-001, P0-002, P0-003, SPEC CONSOLIDATION hoàn thành; link đến 89 Tasks chuẩn.
- `PROJECT_SPEC/CURRENT_STATUS.md` — Cập nhật đúng tiến độ, khẳng định AI hiện tại chỉ là BoW+NN, chưa có RAG/Context.
- `docs/audit/SPEC_ROADMAP_CONSOLIDATION_AUDIT.md` — Thêm phần Post-Consolidation Resolution ghi rõ audit gốc là PRE-CONSOLIDATION.

Tất cả các file trên xuất hiện trong `git status` với ký hiệu `??` (untracked), xác nhận chúng là file mới do task này tạo ra/cập nhật và chưa có commit lưu chúng.

## Existing Unrelated Working-Tree Changes

Working tree hiện tại có các thay đổi source code **không thuộc** Documentation Consolidation task:

- Tracked changes (M/D): `app/__init__.py`, `app/auth.py`, `app/main.py`, `app/models.py`, `app/routes.py`, `app/static/css/style.css`, `app/templates/` (nhiều file), `framework/src/data/intents.json`, `framework/src/model/` (nhiều file), `framework/src/processing/retrieval.py`, `requirements.txt`, `.gitignore`, `README.md`.

Các changes này tồn tại trước Documentation Consolidation task theo Git log:

```
502a425 Cap nhat gitignore, demo1: xac thuc, phan quyen, chat AI PyTorch
6195059 bt2
66a1cbd Remove pycache and add gitignore
5767711 Upload toan bo cau truc du an
```

**Documentation Consolidation did not intentionally modify source code. Existing source-code changes in the working tree were not modified by this task and could not be attributed to this task without a baseline.**

## Git Baseline Limitation

Existing working-tree changes could not be attributed to Documentation Consolidation because no clean baseline/commit boundary was available. Task này không có commit riêng biệt để phân ranh giới. Tất cả thay đổi documentation của task đều là file untracked (`??`) — file mới, chưa từng được commit, tách biệt với tracked source changes.

## Important Requirements Verified
- **900 accounts:** Đã được giữ nguyên (từ Khóa 24, 25, 26 ngành CNTT mã 5122, serial 0001-0300).
- **P0–P26 / 27 Phases / 89 Tasks:** Đã được giữ nguyên lộ trình chuẩn.
- **PyTorch + BoW + Neural Network + Intent Classification:** Được bảo lưu làm công nghệ AI hiện hành. Context và RAG được giữ ở phần tương lai.
- **Student/Admin:** Được bảo lưu phân quyền rõ ràng.

## Source Code

Documentation Consolidation did not intentionally modify source code. Existing source-code changes in the working tree were not modified by this task and could not be attributed to this task without a baseline.

(Tuyên bố "Đã chạy git diff và git status, xác nhận KHÔNG CÓ sự thay đổi nào đối với các file mã nguồn" trong evidence version cũ là không chính xác — working tree thực tế có nhiều tracked source changes. Tuy nhiên, chúng là changes từ trước task này, không phải do task này tạo ra.)

## Validation
- Các file .md trong `PROJECT_SPEC/` đã được đồng bộ nội dung mà không mất đi yêu cầu chuẩn.
- `git status` xác nhận tất cả documentation files của task này đều là `??` (untracked) — không phải tracked modified.
- `git log` cho thấy không có commit nào chứa các file documentation task này — chưa được commit.

## Remaining Issues
- `README.md` đang chứa tài liệu cũ (account `24ct2001 / 123456` và số liệu AI cũ), cần được cập nhật ở một task chuyên biệt về chuẩn hóa README.

---

**Last Updated:** 2026-10-01 — Documentation Consolidation Review Fix (Antigravity)


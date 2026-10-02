import io
import sys

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

sys.path.append('framework/src/model')
from chatbot import get_response_details

test_queries = [
    'Xin chào bot',
    'Tài liệu môn Công nghệ phần mềm',
    'Học phí kỳ này bao nhiêu tiền một tín chỉ',
    'Cách tính điểm gpa thang điểm 4',
    'Làm sao để xin giấy xác nhận sinh viên',
    'OOP là gì',
    'Bitcoin hôm nay giá bao nhiêu',
    'Số điện thoại phòng đào tạo'
]

print("=== KIỂM THỬ NHANH CHATBOT ===")
for q in test_queries:
    res = get_response_details(q)
    print(f"👉 Câu hỏi: {q}")
    print(f"🎯 Intent: {res['intent']} | Độ tin cậy: {res['confidence']:.2f} | Trạng thái: {res['status']}")
    print(f"💬 Trả lời:\n{res['response'][:160]}...")
    print("-" * 55)

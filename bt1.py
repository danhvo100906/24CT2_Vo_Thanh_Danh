import sys
import io
from pathlib import Path

# Đảm bảo Terminal nhận diện UTF-8 không bị lỗi tiếng Việt
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thêm Root Path vào sys.path để import các module dễ dàng
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.routes import process_student_data

def main():
    # Dữ liệu giả lập đầu vào
    students = [
        {"name": "Võ Thành Danh", "scores": [9.0, 8.5, 9.5]},
        {"name": "Nguyen Van A", "scores": [6.0, 7.0, 6.5]},
        {"name": "Tran Thi B", "scores": [4.0, 3.5, 5.0]}
    ]

    print("================ KẾT QUẢ XỬ LÝ ================\n")
    for student in students:
        result = process_student_data(student["name"], student["scores"])
        print(f"👨‍🎓 Sinh viên : {result['name']}")
        print(f"📊 Điểm TB  : {result['average']}")
        print(f"🏅 Xếp loại  : {result['rank']}")
        print("-" * 45)

if __name__ == "__main__":
    main()
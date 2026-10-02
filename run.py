import sys
import os
import io

# Đảm bảo Terminal trên Windows nhận diện UTF-8
if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

# Thêm thư mục gốc vào sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 55)
    print("🚀 StudyBot Server đang khởi động...")
    print("👉 Mở trình duyệt và truy cập: http://127.0.0.1:5000")
    print("👉 Tài khoản Admin: admin / admin123")
    print("=" * 55)
    app.run(debug=True, port=5000)

import sys
import os
import io

# Đảm bảo Terminal trên Windows nhận UTF-8 không bị lỗi charmap
if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

# Đảm bảo thư mục gốc dự án luôn có trong sys.path để import app hoạt động từ bất cứ đâu
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 55)
    print("🚀 StudyBot Server đang khởi động...")
    print("👉 Mở trình duyệt và truy cập: http://127.0.0.1:5000")
    print("👉 Tài khoản Admin: admin / admin123")
    print("=" * 55)
    app.run(debug=True, port=5000)
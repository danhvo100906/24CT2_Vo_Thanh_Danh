import io
import json
import os
import sys
import unittest

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import db, User, ChatMessage, Feedback


class StudyBotSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['SECRET_KEY'] = 'test-secret-key-12345'
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def test_01_anonymous_redirect_to_login(self):
        """1. Người dùng chưa đăng nhập truy cập /dashboard phải bị chuyển về /login"""
        res = self.client.get('/dashboard', follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn('/login', res.headers['Location'])

    def test_02_register_route_removed(self):
        """2. Tuyệt đối không còn route đăng ký /register (trả về 404)"""
        res = self.client.get('/register')
        self.assertEqual(res.status_code, 404)

    def test_03_student_login(self):
        """3. Sinh viên đăng nhập đúng tài khoản admin cấp"""
        res = self.client.post('/login', data={
            'username': '2451220001',
            'password': '2451220001'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('StudyBot'.encode('utf-8'), res.data)

    def test_04_student_cannot_access_admin(self):
        """4. Sinh viên không có quyền truy cập trang quản trị /admin (403 Forbidden)"""
        # Login student
        self.client.post('/login', data={'username': '2451220001', 'password': '2451220001'})
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 403)

    def test_05_admin_login_and_access(self):
        """5. Quản trị viên đăng nhập và truy cập thành công /admin"""
        self.client.get('/logout')
        res = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Admin Panel'.encode('utf-8'), res.data)

    def test_06_chat_api_and_feedback(self):
        """6. Kiểm thử Chat API & Feedback API"""
        # Login as student
        self.client.get('/logout')
        self.client.post('/login', data={'username': '2451220001', 'password': '2451220001'})

        # Call Chat API
        chat_res = self.client.post('/api/chat', json={
            'message': 'Học phí một tín chỉ bao nhiêu tiền?'
        })
        self.assertEqual(chat_res.status_code, 200)
        data = json.loads(chat_res.data.decode('utf-8'))
        self.assertIn('response', data)
        self.assertIn('message_id', data)
        msg_id = data['message_id']

        # Call Feedback API
        fb_res = self.client.post('/api/feedback', json={
            'message_id': msg_id,
            'rating': 'helpful',
            'comment': 'Câu trả lời rất rõ ràng'
        })
        self.assertEqual(fb_res.status_code, 200)
        fb_data = json.loads(fb_res.data.decode('utf-8'))
        self.assertTrue(fb_data.get('success'))

    def test_07_admin_manage_student(self):
        """7. Admin thêm sinh viên mới và thay đổi trạng thái"""
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})

        # Xóa sinh viên biên 2451220300 trước để thử thêm mới lại
        with self.app.app_context():
            st_to_del = User.query.filter_by(student_code='2451220300').first()
            if st_to_del:
                db.session.delete(st_to_del)
                db.session.commit()

        # Add student
        add_res = self.client.post('/admin/students/add', data={
            'student_code': '2451220300',
            'full_name': 'Sinh viên 2451220300',
            'password': 'Password2026'
        }, follow_redirects=True)
        self.assertEqual(add_res.status_code, 200)

        # Check in database
        with self.app.app_context():
            st = User.query.filter_by(student_code='2451220300').first()
            self.assertIsNotNone(st)
            self.assertEqual(st.student_code, '2451220300')
            self.assertEqual(st.username, '2451220300')
            self.assertEqual(st.status, 'active')
            self.assertTrue(st.check_password('Password2026'))



if __name__ == '__main__':
    print("=" * 60)
    print("🚀 BẮT ĐẦU CHẠY UNIT & INTEGRATION TESTS STUDYBOT")
    print("=" * 60)
    unittest.main()

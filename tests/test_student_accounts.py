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
from app.models import db, User
from app.student_accounts import (
    generate_student_codes,
    is_valid_student_code,
    get_student_placeholder_name,
    seed_student_accounts,
    VALID_COHORTS,
    MAJOR_CODE,
    MIN_SERIAL,
    MAX_SERIAL
)


class TestStudentAccountRules(unittest.TestCase):
    """Kiểm thử tính đúng đắn của generator và validator danh mục 900 mã sinh viên CNTT"""

    def test_01_cardinality_and_uniqueness(self):
        codes = generate_student_codes()
        self.assertEqual(len(codes), 900, "Tổng số mã sinh viên phải đúng 900")
        self.assertEqual(len(set(codes)), 900, "Tất cả 900 mã sinh viên phải duy nhất, không trùng lặp")

    def test_02_cohort_distribution(self):
        codes = generate_student_codes()
        for cohort in ['24', '25', '26']:
            cohort_codes = [c for c in codes if c.startswith(cohort)]
            self.assertEqual(len(cohort_codes), 300, f"Khóa {cohort} phải có đúng 300 mã sinh viên")

    def test_03_major_code_and_serial_range(self):
        codes = generate_student_codes()
        for c in codes:
            self.assertEqual(len(c), 10, f"Mã {c} phải có đúng 10 ký tự")
            self.assertEqual(c[2:6], '5122', f"Mã {c} phải chứa mã ngành 5122")
            serial = int(c[6:10])
            self.assertTrue(1 <= serial <= 300, f"Số thứ tự {serial} trong mã {c} phải từ 0001 đến 0300")

    def test_04_validator_boundaries(self):
        boundaries = [
            '2451220001', '2451220300',
            '2551220001', '2551220300',
            '2651220001', '2651220300'
        ]
        for code in boundaries:
            self.assertTrue(is_valid_student_code(code), f"Mã biên {code} phải hợp lệ")

    def test_05_validator_rejections(self):
        invalid_codes = [
            '2351220001',  # Khóa 23 ngoài phạm vi
            '2751220001',  # Khóa 27 ngoài phạm vi
            '2451210001',  # Sai mã ngành (5121 thay vì 5122)
            '2451230001',  # Sai mã ngành (5123 thay vì 5122)
            '2451220000',  # Số thứ tự 0000
            '2451220301',  # Số thứ tự 0301 (vượt quá 300)
            '2551220500',  # Số thứ tự 0500
            '245122001',   # Thiếu ký tự (9 ký tự)
            '24512200001', # Thừa ký tự (11 ký tự)
            '24CT2001',    # Mã theo định dạng cũ
            '',            # Rỗng
            None,          # None
            'abcdefghij'   # Không phải chữ số
        ]
        for code in invalid_codes:
            self.assertFalse(is_valid_student_code(code), f"Mã {code} phải bị từ chối")

    def test_06_placeholder_name(self):
        name = get_student_placeholder_name('2451220001')
        self.assertEqual(name, 'Sinh viên 2451220001')


class TestStudentSeedAndDatabase(unittest.TestCase):
    """Kiểm thử quá trình seed tài khoản vào SQLite in-memory"""

    @classmethod
    def setUpClass(cls):
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['SECRET_KEY'] = 'test-seed-secret-key'
        cls.app = create_app()
        cls.app.config['TESTING'] = True

    def test_01_seed_cardinality_and_fields(self):
        with self.app.app_context():
            students = User.query.filter_by(role='student').all()
            self.assertEqual(len(students), 900, "Database sau seed phải có đúng 900 sinh viên")

            admin = User.query.filter_by(role='admin').first()
            self.assertIsNotNone(admin, "Admin phải tồn tại riêng")
            self.assertEqual(admin.username, 'admin')

            # Kiểm tra phân bố theo khóa
            for cohort in ['24', '25', '26']:
                c_students = [s for s in students if s.student_code.startswith(cohort)]
                self.assertEqual(len(c_students), 300, f"Khóa {cohort} phải có 300 sinh viên trong database")

            # Kiểm tra tính toàn vẹn của dữ liệu sinh viên
            sample_codes = [
                '2451220001', '2451220300',
                '2551220001', '2551220300',
                '2651220001', '2651220300',
                '2451220150', '2551220150', '2651220150'
            ]
            for code in sample_codes:
                st = User.query.filter_by(student_code=code).first()
                self.assertIsNotNone(st, f"Sinh viên {code} phải tồn tại")
                self.assertEqual(st.username, code, f"Username phải trùng student_code đối với {code}")
                self.assertEqual(st.role, 'student')
                self.assertEqual(st.status, 'active')
                self.assertEqual(st.full_name, f"Sinh viên {code}")
                # Kiểm tra mật khẩu mặc định được hash từ chính mã sinh viên
                self.assertTrue(st.check_password(code), f"Mật khẩu mặc định của {code} phải là chính mã sinh viên")
                self.assertFalse(st.check_password('123456'), f"Mật khẩu của {code} không được là 123456")

    def test_02_seed_idempotency_and_password_preservation(self):
        with self.app.app_context():
            # Đổi mật khẩu của 1 sinh viên
            st = User.query.filter_by(student_code='2451220001').first()
            st.set_password('MatKhauMoi@2026')
            db.session.commit()

            # Chạy lại seed
            report = seed_student_accounts(db.session)
            self.assertEqual(report['created_count'], 0, "Lần seed thứ hai không được tạo thêm tài khoản")
            self.assertEqual(report['preserved_count'], 900, "900 tài khoản hiện có phải được bảo toàn")

            # Xác minh mật khẩu mới không bị ghi đè
            st_reloaded = User.query.filter_by(student_code='2451220001').first()
            self.assertTrue(st_reloaded.check_password('MatKhauMoi@2026'), "Mật khẩu đã đổi phải được bảo toàn sau khi seed lại")
            self.assertFalse(st_reloaded.check_password('2451220001'), "Mật khẩu mặc định cũ không còn hiệu lực")

            # Tổng số sinh viên vẫn đúng 900
            total = User.query.filter_by(role='student').count()
            self.assertEqual(total, 900)

    def test_03_mismatched_student_preservation(self):
        with self.app.app_context():
            # Giả lập tồn tại tài khoản sinh viên ngoài danh mục
            legacy = User(
                username='legacy_student_99',
                student_code='LEGACY99',
                full_name='Sinh viên cũ ngoài danh mục',
                role='student',
                status='active'
            )
            legacy.set_password('legacypass')
            db.session.add(legacy)
            db.session.commit()

            # Chạy seed
            report = seed_student_accounts(db.session)
            self.assertGreaterEqual(report['mismatched_count'], 1)

            # Xác minh tài khoản legacy không bị tự xóa
            found_legacy = User.query.filter_by(username='legacy_student_99').first()
            self.assertIsNotNone(found_legacy, "Tài khoản ngoài danh mục không được tự ý xóa")

            # Dọn dẹp bản ghi giả lập
            db.session.delete(found_legacy)
            db.session.commit()


class TestStudentAuthAndProtection(unittest.TestCase):
    """Kiểm thử đăng nhập, phân quyền và đổi mật khẩu"""

    @classmethod
    def setUpClass(cls):
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['SECRET_KEY'] = 'test-auth-secret-key'
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_01_six_boundary_logins(self):
        boundaries = [
            '2451220001', '2451220300',
            '2551220001', '2551220300',
            '2651220001', '2651220300'
        ]
        for code in boundaries:
            self.client.get('/logout')
            res = self.client.post('/login', data={
                'username': code,
                'password': code
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('StudyBot'.encode('utf-8'), res.data)
            self.assertIn(f'Sinh viên {code}'.encode('utf-8'), res.data)

    def test_02_login_rejections(self):
        # 1. Sai mật khẩu
        self.client.get('/logout')
        res = self.client.post('/login', data={'username': '2451220001', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn('Tên đăng nhập hoặc mật khẩu không chính xác'.encode('utf-8'), res.data)

        # 2. Sai ngành (5121)
        res = self.client.post('/login', data={'username': '2451210001', 'password': '2451210001'}, follow_redirects=True)
        self.assertIn('Tên đăng nhập hoặc mật khẩu không chính xác'.encode('utf-8'), res.data)

        # 3. Khóa ngoài phạm vi (23, 27)
        for bad_code in ['2351220001', '2751220001']:
            res = self.client.post('/login', data={'username': bad_code, 'password': bad_code}, follow_redirects=True)
            self.assertIn('Tên đăng nhập hoặc mật khẩu không chính xác'.encode('utf-8'), res.data)

        # 4. Số thứ tự ngoài biên (0000, 0301)
        for bad_code in ['2451220000', '2451220301']:
            res = self.client.post('/login', data={'username': bad_code, 'password': bad_code}, follow_redirects=True)
            self.assertIn('Tên đăng nhập hoặc mật khẩu không chính xác'.encode('utf-8'), res.data)

        # 5. Username không tồn tại
        res = self.client.post('/login', data={'username': 'nonexistent_user', 'password': 'password'}, follow_redirects=True)
        self.assertIn('Tên đăng nhập hoặc mật khẩu không chính xác'.encode('utf-8'), res.data)

        # 6. Tài khoản inactive bị chặn
        with self.app.app_context():
            st = User.query.filter_by(student_code='2451220050').first()
            st.status = 'inactive'
            db.session.commit()

        res = self.client.post('/login', data={'username': '2451220050', 'password': '2451220050'}, follow_redirects=True)
        self.assertIn('tạm khóa'.encode('utf-8'), res.data)

        # Khôi phục trạng thái active
        with self.app.app_context():
            st = User.query.filter_by(student_code='2451220050').first()
            st.status = 'active'
            db.session.commit()

    def test_03_authorization_student_cannot_access_admin(self):
        # Đăng nhập student
        self.client.get('/logout')
        self.client.post('/login', data={'username': '2451220001', 'password': '2451220001'})

        # Thử vào /admin -> 403
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 403)

        # Thử vào các route admin khác
        self.assertEqual(self.client.get('/admin/students').status_code, 403)
        self.assertEqual(self.client.get('/admin/materials').status_code, 403)

    def test_04_admin_login_and_access(self):
        self.client.get('/logout')
        res = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Admin Panel'.encode('utf-8'), res.data)

        # Admin truy cập được /admin
        admin_res = self.client.get('/admin')
        self.assertEqual(admin_res.status_code, 200)

    def test_05_anonymous_route_protection(self):
        self.client.get('/logout')
        protected_routes = ['/dashboard', '/materials', '/info', '/history', '/change-password', '/admin']
        for r in protected_routes:
            res = self.client.get(r, follow_redirects=False)
            self.assertEqual(res.status_code, 302, f"Route {r} phải chuyển hướng khi chưa đăng nhập")
            self.assertIn('/login', res.headers['Location'])

    def test_06_student_change_password_flow(self):
        # Đăng nhập với tài khoản 2451220002
        self.client.get('/logout')
        self.client.post('/login', data={'username': '2451220002', 'password': '2451220002'})

        # 1. Sai mật khẩu hiện tại
        res = self.client.post('/change-password', data={
            'current_password': 'wrongcurrentpassword',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123'
        }, follow_redirects=True)
        self.assertIn('Mật khẩu hiện tại không chính xác'.encode('utf-8'), res.data)

        # 2. Mật khẩu xác nhận không khớp
        res = self.client.post('/change-password', data={
            'current_password': '2451220002',
            'new_password': 'NewPassword123',
            'confirm_password': 'DifferentPassword'
        }, follow_redirects=True)
        self.assertIn('không khớp'.encode('utf-8'), res.data)

        # 3. Mật khẩu quá ngắn (< 6 ký tự)
        res = self.client.post('/change-password', data={
            'current_password': '2451220002',
            'new_password': '123',
            'confirm_password': '123'
        }, follow_redirects=True)
        self.assertIn('ít nhất 6 ký tự'.encode('utf-8'), res.data)

        # 4. Đổi mật khẩu thành công
        res = self.client.post('/change-password', data={
            'current_password': '2451220002',
            'new_password': 'MyNewSecurePass2026',
            'confirm_password': 'MyNewSecurePass2026'
        }, follow_redirects=True)
        self.assertIn('Đổi mật khẩu thành công'.encode('utf-8'), res.data)

        # 5. Đăng xuất và thử lại: Mật khẩu cũ phải thất bại
        self.client.get('/logout')
        res_old = self.client.post('/login', data={
            'username': '2451220002',
            'password': '2451220002'
        }, follow_redirects=True)
        self.assertIn('Tên đăng nhập hoặc mật khẩu không chính xác'.encode('utf-8'), res_old.data)

        # 6. Mật khẩu mới đăng nhập thành công
        res_new = self.client.post('/login', data={
            'username': '2451220002',
            'password': 'MyNewSecurePass2026'
        }, follow_redirects=True)
        self.assertEqual(res_new.status_code, 200)
        self.assertIn('StudyBot'.encode('utf-8'), res_new.data)

    def test_07_admin_manage_student_rules(self):
        # Đăng nhập Admin
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})

        # Admin không thể tạo sinh viên với mã không hợp lệ (sai khóa 23)
        res_bad_code = self.client.post('/admin/students/add', data={
            'student_code': '2351220001',
            'password': ''
        }, follow_redirects=True)
        self.assertIn('Mã sinh viên không hợp lệ'.encode('utf-8'), res_bad_code.data)

        # Admin không thể đặt mật khẩu là 123456 khi thêm mới
        res_123456 = self.client.post('/admin/students/add', data={
            'student_code': '2451220299',
            'password': '123456'
        }, follow_redirects=True)
        self.assertIn('Không được đặt mật khẩu'.encode('utf-8'), res_123456.data)

        # Admin không thể đổi mật khẩu sinh viên thành 123456
        with self.app.app_context():
            st = User.query.filter_by(student_code='2451220001').first()
            st_id = st.id

        res_edit_123456 = self.client.post(f'/admin/students/edit/{st_id}', data={
            'full_name': 'Sinh viên 2451220001',
            'new_password': '123456'
        }, follow_redirects=True)
        self.assertIn('Không được đặt mật khẩu'.encode('utf-8'), res_edit_123456.data)


if __name__ == '__main__':
    print("=" * 65)
    print("🚀 BẮT ĐẦU CHẠY KIỂM THỬ TÀI KHOẢN SINH VIÊN TASK-003")
    print("=" * 65)
    unittest.main()

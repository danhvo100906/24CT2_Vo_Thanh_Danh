"""
Module quan ly danh muc ma sinh vien va khoi tao tai khoan sinh vien CNTT DAU.
Quy tac ma sinh vien: KK5122NNNN
- KK: Khoa (24, 25, 26)
- 5122: Ma nganh CNTT tai DAU
- NNNN: So thu tu tu 0001 den 0300 (300 sinh vien / khoa)
Tong cong: 900 tai khoan sinh vien.
"""

from typing import List, Set, Dict, Any, Optional
from .models import User

VALID_COHORTS = ('24', '25', '26')
MAJOR_CODE = '5122'
MIN_SERIAL = 1
MAX_SERIAL = 300
SERIAL_LENGTH = 4


def generate_student_codes() -> List[str]:
    """Sinh danh sach day du 900 ma sinh vien hop le theo thu tu khoa va so thu tu."""
    codes = []
    for cohort in VALID_COHORTS:
        for serial in range(MIN_SERIAL, MAX_SERIAL + 1):
            codes.append(f"{cohort}{MAJOR_CODE}{serial:0{SERIAL_LENGTH}d}")
    return codes


def is_valid_student_code(code: Optional[str]) -> bool:
    """Kiem tra ma sinh vien co thuoc danh muc 900 ma hop le hay khong."""
    if not code or not isinstance(code, str):
        return False
    code = code.strip().upper()
    if len(code) != 10 or not code.isdigit():
        return False
    cohort = code[:2]
    major = code[2:6]
    serial_str = code[6:10]
    if cohort not in VALID_COHORTS:
        return False
    if major != MAJOR_CODE:
        return False
    serial = int(serial_str)
    if not (MIN_SERIAL <= serial <= MAX_SERIAL):
        return False
    return True


def get_student_placeholder_name(code: str) -> str:
    """Tra ve placeholder ho ten theo quy dinh: Sinh vien <ma sinh vien>."""
    return f"Sinh viên {code}"


def seed_student_accounts(session) -> Dict[str, Any]:
    """
    Khoi tao idempotent 900 tai khoan sinh vien CNTT.
    - Neu chua co: tao moi voi username == student_code == ma SV, role='student', status='active',
      full_name='Sinh vien <ma>', password default duoc hash tu chinh ma SV.
    - Neu da co: bao toan password_hash (khong ghi de vi sinh vien co the da doi mat khau).
    - Neu phat hien tai khoan sinh vien ngoai danh muc: bao cao mismatch, khong tu y xoa.
    """
    target_codes = generate_student_codes()
    target_set = set(target_codes)

    existing_users = session.query(User).all()
    existing_by_code: Dict[str, User] = {}
    existing_by_username: Dict[str, User] = {}
    mismatched_students: List[Dict[str, Any]] = []

    for u in existing_users:
        if u.role == 'admin':
            continue
        code = u.student_code
        uname = u.username
        if code:
            existing_by_code[code] = u
        if uname:
            existing_by_username[uname] = u

        # Phat hien sinh vien ngoai danh muc
        is_outside = False
        if code and code not in target_set:
            is_outside = True
        elif not code and uname and uname not in target_set:
            is_outside = True

        if is_outside:
            mismatched_students.append({
                "id": u.id,
                "username": uname,
                "student_code": code
            })

    created_count = 0
    preserved_count = 0

    for code in target_codes:
        existing_user = existing_by_code.get(code) or existing_by_username.get(code)
        if existing_user:
            preserved_count += 1
            if not existing_user.student_code:
                existing_user.student_code = code
            if not existing_user.username:
                existing_user.username = code
            if existing_user.role != 'student':
                existing_user.role = 'student'
        else:
            new_student = User(
                student_code=code,
                username=code,
                full_name=get_student_placeholder_name(code),
                role='student',
                status='active'
            )
            # Dung pbkdf2 nhanh hon scrypt khi seed hang loat 900 tai khoan.
            # Mat khau mac dinh = ma sinh vien, sinh vien nen doi sau khi dang nhap.
            from werkzeug.security import generate_password_hash
            new_student.password_hash = generate_password_hash(
                code, method='pbkdf2:sha256:260000'
            )
            session.add(new_student)
            created_count += 1

    report = {
        "total_target": len(target_codes),
        "created_count": created_count,
        "preserved_count": preserved_count,
        "mismatched_count": len(mismatched_students),
        "mismatched_students": mismatched_students
    }

    if mismatched_students:
        print(f"[SEED WARNING] Phat hien {len(mismatched_students)} tai khoan sinh vien ngoai danh muc 900 ma hop le (duoc giu nguyen, khong xoa)")

    return report

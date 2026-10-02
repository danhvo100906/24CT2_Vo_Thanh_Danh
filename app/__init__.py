import os
import json
from flask import Flask
from flask_login import LoginManager
from .models import db, User, Subject, Material, KnowledgeItem

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    
    # Cau hinh bao mat & database
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'studybot-secret-key-production-2025')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///studybot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main_bp
    from .auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app


def seed_initial_data():
    """Khoi tao du lieu mau va tai khoan he thong khi tao database moi"""
    # 1. Khoi tao tai khoan Admin
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            student_code='ADMIN01',
            full_name='Quản trị viên Hệ thống',
            role='admin',
            status='active'
        )
        admin.set_password('admin123')
        db.session.add(admin)

    # 2. Khoi tao danh muc 900 tai khoan Sinh vien CNTT theo quy dinh TASK-003
    # Chi seed khi so sinh vien < 900 (tranh lam cham startup do bcrypt 900 lan)
    student_count = User.query.filter_by(role='student').count()
    if student_count < 900:
        from .student_accounts import seed_student_accounts
        seed_student_accounts(db.session)

    # 3. Khoi tao Mon hoc & Tai lieu tu JSON
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    materials_file = os.path.join(base_dir, 'data', 'materials.json')
    if os.path.exists(materials_file) and Subject.query.count() == 0:
        try:
            with open(materials_file, 'r', encoding='utf-8') as f:
                mat_list = json.load(f)
                for item in mat_list:
                    sub = Subject(
                        code=item['code'],
                        name=item['name'],
                        credits=item.get('credits', 3),
                        description=item.get('description', '')
                    )
                    db.session.add(sub)
                    mat = Material(
                        subject_code=item['code'],
                        title=f"Tài liệu & Giáo trình môn {item['name']}",
                        type='textbook',
                        syllabus_url=item.get('syllabus'),
                        slides_url=item.get('slides'),
                        exam_url=item.get('exam_sample'),
                        reference_book=item.get('reference_book'),
                        status='active'
                    )
                    db.session.add(mat)
        except Exception as e:
            print("Lỗi khi seed materials:", e)

    # 4. Khoi tao Knowledge Base items tu JSON
    if KnowledgeItem.query.count() == 0:
        data_dir = os.path.join(base_dir, 'data')
        
        # Tuition
        tui_path = os.path.join(data_dir, 'tuition.json')
        if os.path.exists(tui_path):
            try:
                with open(tui_path, 'r', encoding='utf-8') as f:
                    for t in json.load(f):
                        k = KnowledgeItem(
                            category='tuition',
                            title=t['category'],
                            content=f"{t['category']}: {t.get('price', 0):,} VNĐ. {t.get('description', '')}",
                            source=t.get('source', '')
                        )
                        db.session.add(k)
            except Exception:
                pass

        # Regulations
        reg_path = os.path.join(data_dir, 'regulations.json')
        if os.path.exists(reg_path):
            try:
                with open(reg_path, 'r', encoding='utf-8') as f:
                    for r in json.load(f):
                        k = KnowledgeItem(
                            category='regulations',
                            title=r['title'],
                            content=r['content'],
                            source=r.get('source', '')
                        )
                        db.session.add(k)
            except Exception:
                pass

        # Procedures
        proc_path = os.path.join(data_dir, 'procedures.json')
        if os.path.exists(proc_path):
            try:
                with open(proc_path, 'r', encoding='utf-8') as f:
                    for p in json.load(f):
                        k = KnowledgeItem(
                            category='procedures',
                            title=p['procedure_name'],
                            content=f"Yêu cầu: {p.get('requirements')}\nCác bước: {p.get('steps')}\nThời gian: {p.get('processing_time')}\nĐịa điểm: {p.get('location')}",
                            source=p.get('source', '')
                        )
                        db.session.add(k)
            except Exception:
                pass

        # Contacts
        cont_path = os.path.join(data_dir, 'contacts.json')
        if os.path.exists(cont_path):
            try:
                with open(cont_path, 'r', encoding='utf-8') as f:
                    for c in json.load(f):
                        k = KnowledgeItem(
                            category='contacts',
                            title=c['department'],
                            content=f"Chức năng: {c.get('function')}\nSĐT: {c.get('phone')}\nEmail: {c.get('email')}\nĐịa điểm: {c.get('location')}",
                            source=c.get('source', '')
                        )
                        db.session.add(k)
            except Exception:
                pass

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Lỗi commit seed data:", e)

from flask import Flask
from flask_login import LoginManager
from .models import db, User

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'doi-key-nay-khi-trien-khai-that'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main_bp
    from .auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        # Tạo tài khoản admin mặc định nếu chưa có
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Đã tạo tài khoản admin mặc định (admin / admin123)")

    return app
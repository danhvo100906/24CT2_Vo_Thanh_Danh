from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            if user.is_admin():
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu', 'error')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, role='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công, vui lòng đăng nhập', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
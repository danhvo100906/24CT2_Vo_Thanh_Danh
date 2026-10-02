from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.', 'error')
            return render_template('login.html')

        # Cho phep dang nhap bang username hoac student_code
        user = User.query.filter(
            (User.username == username) | (User.student_code == username.upper())
        ).first()

        if user and user.check_password(password):
            if not user.is_active_user():
                flash('Tài khoản của bạn đang bị tạm khóa. Vui lòng liên hệ Quản trị viên.', 'error')
                return render_template('login.html')

            login_user(user)
            flash(f'Chào mừng {user.full_name or user.username} đăng nhập thành công!', 'success')
            if user.is_admin():
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không chính xác.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not current_password or not new_password or not confirm_password:
            flash('Vui lòng nhập đầy đủ tất cả các trường mật khẩu.', 'error')
            return render_template('user/change_password.html', user=current_user)

        if not current_user.check_password(current_password):
            flash('Mật khẩu hiện tại không chính xác.', 'error')
            return render_template('user/change_password.html', user=current_user)

        if new_password != confirm_password:
            flash('Mật khẩu mới và xác nhận mật khẩu không khớp.', 'error')
            return render_template('user/change_password.html', user=current_user)

        if len(new_password) < 6:
            flash('Mật khẩu mới phải có ít nhất 6 ký tự.', 'error')
            return render_template('user/change_password.html', user=current_user)

        current_user.set_password(new_password)
        db.session.commit()

        flash('Đổi mật khẩu thành công! Vui lòng sử dụng mật khẩu mới cho các lần đăng nhập sau.', 'success')
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))

    return render_template('user/change_password.html', user=current_user)

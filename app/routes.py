from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)


def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


# ---- Giao diện User ----
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html', user=current_user)


# ---- Giao diện Admin ----
@main_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    from .models import User
    total_users = User.query.filter_by(role='user').count()
    return render_template('admin/dashboard.html', user=current_user, total_users=total_users)


@main_bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    from .models import User
    users = User.query.filter_by(role='user').all()
    return render_template('admin/users.html', user=current_user, users=users)
from flask import jsonify, request
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'framework', 'src', 'model'))


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    from chatbot import get_response
    from .models import db, ChatHistory

    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "Tin nhắn trống"}), 400

    bot_response = get_response(user_message)

    history = ChatHistory(
        user_id=current_user.id,
        message=user_message,
        response=bot_response
    )
    db.session.add(history)
    db.session.commit()

    return jsonify({"response": bot_response})


@main_bp.route('/history')
@login_required
def chat_history():
    from .models import ChatHistory
    history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.created_at.desc()).all()
    return render_template('user/history.html', user=current_user, history=history)
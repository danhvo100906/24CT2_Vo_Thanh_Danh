import json
import os
import subprocess
import sys
from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, abort, jsonify, request, flash
from flask_login import login_required, current_user

from .models import db, User, Subject, Material, KnowledgeItem, ChatMessage, Feedback

main_bp = Blueprint('main', __name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'framework', 'src', 'model')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
if MODEL_DIR not in sys.path:
    sys.path.append(MODEL_DIR)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# ---- Hàm bổ trợ tính điểm sinh viên (dùng cho bt1.py & quy chế) ----
def process_student_data(name, scores):
    """Tính điểm trung bình và xếp loại học tập của sinh viên"""
    if not scores:
        avg = 0.0
    else:
        avg = round(sum(scores) / len(scores), 2)

    if avg >= 9.0:
        rank = "Xuất sắc"
    elif avg >= 8.0:
        rank = "Giỏi"
    elif avg >= 6.5:
        rank = "Khá"
    elif avg >= 5.0:
        rank = "Trung bình"
    else:
        rank = "Yếu"

    return {
        "name": name,
        "average": avg,
        "rank": rank
    }


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


# ==========================================
# GIAO DIỆN SINH VIÊN (STUDENT)
# ==========================================
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html', user=current_user)


@main_bp.route('/materials')
@login_required
def user_materials():
    query = request.args.get('q', '').strip().lower()
    materials = Material.query.filter_by(status='active').all()
    subjects = {s.code: s for s in Subject.query.all()}
    
    if query:
        filtered_materials = []
        for m in materials:
            sub = subjects.get(m.subject_code)
            sub_name = sub.name.lower() if sub else ""
            if query in m.subject_code.lower() or query in m.title.lower() or query in sub_name:
                filtered_materials.append(m)
        materials = filtered_materials

    return render_template('user/materials.html', user=current_user, materials=materials, subjects=subjects, query=query)


@main_bp.route('/info')
@login_required
def user_info():
    category = request.args.get('category', 'all')
    if category != 'all':
        items = KnowledgeItem.query.filter_by(category=category).all()
    else:
        items = KnowledgeItem.query.all()
    return render_template('user/info.html', user=current_user, items=items, active_cat=category)


@main_bp.route('/history')
@login_required
def chat_history():
    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.created_at.desc()).all()
    return render_template('user/history.html', user=current_user, messages=messages)


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    from chatbot import get_response_details

    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "Tin nhắn không được để trống"}), 400

    result = get_response_details(user_message)
    bot_response = result.get('response', '')
    intent_tag = result.get('intent', '')
    confidence_val = float(result.get('confidence', 0.0))

    msg_record = ChatMessage(
        user_id=current_user.id,
        message=user_message,
        response=bot_response,
        intent=intent_tag,
        confidence=confidence_val
    )
    db.session.add(msg_record)
    db.session.commit()

    return jsonify({
        "response": bot_response,
        "intent": intent_tag,
        "confidence": confidence_val,
        "status": result.get('status', 'answered'),
        "message_id": msg_record.id
    })


@main_bp.route('/api/feedback', methods=['POST'])
@login_required
def api_feedback():
    data = request.get_json() or {}
    message_id = data.get('message_id')
    rating = data.get('rating')  # 'helpful' hoac 'unhelpful'
    comment = data.get('comment', '').strip()

    if not message_id or rating not in ['helpful', 'unhelpful']:
        return jsonify({"error": "Dữ liệu đánh giá không hợp lệ"}), 400

    # Kiem tra message ton tai va thuoc ve current_user
    msg = ChatMessage.query.get(message_id)
    if not msg or msg.user_id != current_user.id:
        return jsonify({"error": "Không tìm thấy tin nhắn"}), 404

    # Cap nhat hoac tao moi feedback
    fb = Feedback.query.filter_by(message_id=message_id).first()
    if fb:
        fb.rating = rating
        fb.comment = comment
    else:
        fb = Feedback(
            message_id=message_id,
            user_id=current_user.id,
            rating=rating,
            comment=comment
        )
        db.session.add(fb)

    db.session.commit()
    return jsonify({"success": True, "message": "Đã lưu phản hồi thành công!"})


# ==========================================
# GIAO DIỆN QUẢN TRỊ VIÊN (ADMIN)
# ==========================================
@main_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_students = User.query.filter_by(role='student').count()
    active_students = User.query.filter_by(role='student', status='active').count()
    total_chats = ChatMessage.query.count()
    total_materials = Material.query.count()
    total_knowledge = KnowledgeItem.query.count()

    helpful_feedbacks = Feedback.query.filter_by(rating='helpful').count()
    unhelpful_feedbacks = Feedback.query.filter_by(rating='unhelpful').count()
    total_feedbacks = helpful_feedbacks + unhelpful_feedbacks
    satisfaction_rate = round((helpful_feedbacks / total_feedbacks * 100), 1) if total_feedbacks > 0 else 100.0

    recent_chats = ChatMessage.query.order_by(ChatMessage.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        user=current_user,
        total_students=total_students,
        active_students=active_students,
        total_chats=total_chats,
        total_materials=total_materials,
        total_knowledge=total_knowledge,
        helpful_feedbacks=helpful_feedbacks,
        unhelpful_feedbacks=unhelpful_feedbacks,
        satisfaction_rate=satisfaction_rate,
        recent_chats=recent_chats
    )


# ---- Quản lý Sinh viên ----
@main_bp.route('/admin/students')
@login_required
@admin_required
def admin_students():
    q = request.args.get('q', '').strip()
    if q:
        students = User.query.filter(
            User.role == 'student',
            (User.username.ilike(f'%{q}%')) | (User.student_code.ilike(f'%{q}%')) | (User.full_name.ilike(f'%{q}%'))
        ).all()
    else:
        students = User.query.filter_by(role='student').order_by(User.created_at.desc()).all()
    return render_template('admin/students.html', user=current_user, students=students, query=q)


@main_bp.route('/admin/students/add', methods=['POST'])
@login_required
@admin_required
def admin_add_student():
    student_code = request.form.get('student_code', '').strip().upper()
    full_name = request.form.get('full_name', '').strip()
    password = request.form.get('password', '').strip()

    if not student_code:
        flash('Vui lòng nhập Mã sinh viên.', 'error')
        return redirect(url_for('main.admin_students'))

    from .student_accounts import is_valid_student_code, get_student_placeholder_name
    if not is_valid_student_code(student_code):
        flash('Mã sinh viên không hợp lệ. Mã phải thuộc danh mục khóa 24-26 CNTT (ví dụ: 2451220001).', 'error')
        return redirect(url_for('main.admin_students'))

    if password == '123456':
        flash('Không được đặt mật khẩu khởi tạo là 123456. Mật khẩu mặc định là mã sinh viên.', 'error')
        return redirect(url_for('main.admin_students'))

    username = student_code

    if User.query.filter((User.username == username) | (User.student_code == student_code)).first():
        flash('Mã sinh viên này đã tồn tại trong hệ thống.', 'error')
        return redirect(url_for('main.admin_students'))

    init_password = password if password else student_code

    new_student = User(
        student_code=student_code,
        username=username,
        full_name=full_name or get_student_placeholder_name(student_code),
        role='student',
        status='active'
    )
    new_student.set_password(init_password)
    db.session.add(new_student)
    db.session.commit()
    flash(f'Đã tạo tài khoản cho sinh viên {new_student.full_name} ({student_code}) thành công!', 'success')
    return redirect(url_for('main.admin_students'))


@main_bp.route('/admin/students/edit/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_edit_student(id):
    student = User.query.get_or_404(id)
    if student.role == 'admin':
        flash('Không thể chỉnh sửa tài khoản Quản trị viên tại đây.', 'error')
        return redirect(url_for('main.admin_students'))

    full_name = request.form.get('full_name', '').strip()
    if full_name:
        student.full_name = full_name

    new_code = request.form.get('student_code', '').strip().upper()
    if new_code and new_code != student.student_code:
        from .student_accounts import is_valid_student_code
        if not is_valid_student_code(new_code):
            flash('Mã sinh viên mới không hợp lệ. Mã phải thuộc danh mục khóa 24-26 CNTT (ví dụ: 2451220001).', 'error')
            return redirect(url_for('main.admin_students'))
        if User.query.filter(User.student_code == new_code, User.id != id).first():
            flash('Mã sinh viên mới đã tồn tại ở tài khoản khác.', 'error')
            return redirect(url_for('main.admin_students'))
        student.student_code = new_code
        student.username = new_code

    new_pass = request.form.get('new_password', '').strip()
    if new_pass:
        if new_pass == '123456':
            flash('Không được đặt mật khẩu là 123456.', 'error')
            return redirect(url_for('main.admin_students'))
        student.set_password(new_pass)

    db.session.commit()
    flash(f'Đã cập nhật thông tin sinh viên {student.full_name} thành công!', 'success')
    return redirect(url_for('main.admin_students'))



@main_bp.route('/admin/students/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_toggle_student(id):
    student = User.query.get_or_404(id)
    if student.role == 'admin':
        flash('Không thể khóa tài khoản Quản trị viên.', 'error')
        return redirect(url_for('main.admin_students'))

    student.status = 'inactive' if student.status == 'active' else 'active'
    db.session.commit()
    status_text = 'Mở khóa' if student.status == 'active' else 'Tạm khóa'
    flash(f'Đã {status_text} tài khoản {student.username}.', 'info')
    return redirect(url_for('main.admin_students'))


@main_bp.route('/admin/students/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_student(id):
    student = User.query.get_or_404(id)
    if student.role == 'admin':
        flash('Không thể xóa tài khoản Quản trị viên.', 'error')
        return redirect(url_for('main.admin_students'))

    name = student.full_name or student.username
    db.session.delete(student)
    db.session.commit()
    flash(f'Đã xóa tài khoản sinh viên {name}.', 'success')
    return redirect(url_for('main.admin_students'))


# ---- Quản lý Tài liệu ----
@main_bp.route('/admin/materials')
@login_required
@admin_required
def admin_materials():
    materials = Material.query.all()
    subjects = Subject.query.all()
    return render_template('admin/materials.html', user=current_user, materials=materials, subjects=subjects)


@main_bp.route('/admin/materials/add', methods=['POST'])
@login_required
@admin_required
def admin_add_material():
    subject_code = request.form.get('subject_code', '').strip().upper()
    title = request.form.get('title', '').strip()
    mat_type = request.form.get('type', 'textbook')
    syllabus_url = request.form.get('syllabus_url', '').strip()
    slides_url = request.form.get('slides_url', '').strip()
    exam_url = request.form.get('exam_url', '').strip()
    reference_book = request.form.get('reference_book', '').strip()

    if not title or not subject_code:
        flash('Vui lòng nhập Mã môn học và Tiêu đề tài liệu.', 'error')
        return redirect(url_for('main.admin_materials'))

    mat = Material(
        subject_code=subject_code,
        title=title,
        type=mat_type,
        syllabus_url=syllabus_url,
        slides_url=slides_url,
        exam_url=exam_url,
        reference_book=reference_book,
        status='active'
    )
    db.session.add(mat)
    db.session.commit()
    flash('Đã thêm tài liệu môn học mới thành công!', 'success')
    return redirect(url_for('main.admin_materials'))


@main_bp.route('/admin/materials/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_toggle_material(id):
    mat = Material.query.get_or_404(id)
    mat.status = 'inactive' if mat.status == 'active' else 'active'
    db.session.commit()
    flash('Đã cập nhật trạng thái tài liệu.', 'info')
    return redirect(url_for('main.admin_materials'))


@main_bp.route('/admin/materials/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_material(id):
    mat = Material.query.get_or_404(id)
    db.session.delete(mat)
    db.session.commit()
    flash('Đã xóa tài liệu khỏi hệ thống.', 'success')
    return redirect(url_for('main.admin_materials'))


# ---- Quản lý Tri thức (Knowledge Base) ----
@main_bp.route('/admin/knowledge')
@login_required
@admin_required
def admin_knowledge():
    category = request.args.get('category', 'all')
    if category != 'all':
        items = KnowledgeItem.query.filter_by(category=category).all()
    else:
        items = KnowledgeItem.query.all()
    return render_template('admin/knowledge.html', user=current_user, items=items, active_cat=category)


@main_bp.route('/admin/knowledge/add', methods=['POST'])
@login_required
@admin_required
def admin_add_knowledge():
    category = request.form.get('category', 'tuition')
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    source = request.form.get('source', '').strip()

    if not title or not content:
        flash('Vui lòng điền đầy đủ tiêu đề và nội dung tri thức.', 'error')
        return redirect(url_for('main.admin_knowledge', category=category))

    k = KnowledgeItem(
        category=category,
        title=title,
        content=content,
        source=source
    )
    db.session.add(k)
    db.session.commit()
    flash('Đã thêm mục tri thức mới vào Knowledge Base!', 'success')
    return redirect(url_for('main.admin_knowledge', category=category))


@main_bp.route('/admin/knowledge/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_knowledge(id):
    k = KnowledgeItem.query.get_or_404(id)
    cat = k.category
    db.session.delete(k)
    db.session.commit()
    flash('Đã xóa mục tri thức khỏi hệ thống.', 'success')
    return redirect(url_for('main.admin_knowledge', category=cat))


# ---- Giám sát Hội thoại & Nhật ký Logs ----
@main_bp.route('/admin/conversations')
@login_required
@admin_required
def admin_conversations():
    chats = ChatMessage.query.order_by(ChatMessage.created_at.desc()).limit(200).all()
    return render_template('admin/conversations.html', user=current_user, chats=chats)


# ---- Huấn luyện lại Bot ----
@main_bp.route('/admin/retrain', methods=['POST'])
@login_required
@admin_required
def admin_retrain():
    train_script = os.path.join(MODEL_DIR, 'train.py')
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        result = subprocess.run(
            [sys.executable, '-u', train_script],
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        flash('Đã huấn luyện lại mô hình PyTorch thành công!', 'success')
    except Exception as e:
        flash(f'Lỗi khi huấn luyện mô hình: {str(e)}', 'error')

    return redirect(url_for('main.admin_dashboard'))

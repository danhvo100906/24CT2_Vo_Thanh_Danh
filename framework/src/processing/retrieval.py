import os
import json
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DATA_DIR = os.path.join(BASE_DIR, '..', '..', '..', 'data')
LOCAL_DATA_DIR = os.path.join(BASE_DIR, '..', 'data')


def get_data_filepath(filename):
    """Lấy đường dẫn tệp dữ liệu ưu tiên root data/ rồi đến local data/"""
    path = os.path.join(ROOT_DATA_DIR, filename)
    if os.path.exists(path):
        return path
    return os.path.join(LOCAL_DATA_DIR, filename)


def load_materials():
    """Đọc danh sách tài liệu môn học"""
    filepath = get_data_filepath('materials.json')
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def load_knowledge_file(filename):
    """Đọc tệp tri thức bất kỳ (tuition.json, regulations.json, v.v.)"""
    filepath = get_data_filepath(filename)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def strip_vietnamese_accents(text):
    """Loại bỏ dấu tiếng Việt để đối sánh linh hoạt giữa chuỗi có dấu và không dấu"""
    if not text:
        return ""
    text = text.replace('đ', 'd').replace('Đ', 'd')
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return unicodedata.normalize('NFC', text)


def normalize_text(text):
    """Chuẩn hóa văn bản tiếng Việt để tìm kiếm: chữ thường, bỏ ký tự thừa"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())


def phrase_in_text(phrase, text):
    """Kiểm tra cụm từ có xuất hiện trọn vẹn (theo ranh giới từ) trong văn bản hay không"""
    if not phrase or not text:
        return False
    pattern = r'(?:\b|^)' + re.escape(phrase) + r'(?:\b|$)'
    return bool(re.search(pattern, text))


# Tập từ khóa truy vấn chung trong ngữ cảnh hỏi tài liệu/đề thi
GENERIC_QUERY_WORDS = {
    'tai', 'lieu', 'giao', 'trinh', 'slide', 'slides', 'bai', 'giang', 'tap', 'de', 'thi', 'mon', 'hoc', 'phan',
    'xin', 'cho', 'minh', 'hoi', 've', 'cac', 'nhung', 'cua', 'va', 'voi', 'o', 'la', 'gi', 'nao', 'the', 'sao',
    'nam', 'truoc', 'mau', 'tim', 'co', 'biet', 'em', 'ban'
}


def search_materials(query):
    """
    Tìm kiếm tài liệu môn học theo từ khóa, tên môn hoặc mã môn.
    Trả về danh sách môn học phù hợp theo thứ tự điểm giảm dần,
    hoặc [] nếu không có truy vấn, không khớp môn học nào hoặc dưới ngưỡng tin cậy.
    """
    if not query or not str(query).strip():
        return []

    norm_query = normalize_text(str(query))
    if not norm_query:
        return []

    unacc_query = strip_vietnamese_accents(norm_query)
    query_tokens = norm_query.split()
    unacc_tokens = unacc_query.split()

    materials = load_materials()
    results = []

    for item in materials:
        score = 0
        code_norm = normalize_text(item.get('code', ''))
        name_norm = normalize_text(item.get('name', ''))
        name_unacc = strip_vietnamese_accents(name_norm)
        desc_norm = normalize_text(item.get('description', ''))
        desc_unacc = strip_vietnamese_accents(desc_norm)
        desc_tokens = set(desc_norm.split())
        desc_unacc_tokens = set(desc_unacc.split())

        # 1. Khớp chính xác mã môn (ưu tiên cao nhất: CNPM, CSDL, MMT, CTDL, WEB, PYTHON)
        if code_norm:
            if phrase_in_text(code_norm, norm_query) or phrase_in_text(code_norm, unacc_query):
                score += 40

        # 2. Khớp chính xác tên môn học (có dấu hoặc không dấu)
        if name_norm:
            if phrase_in_text(name_norm, norm_query):
                score += 35
            elif phrase_in_text(name_unacc, unacc_query):
                score += 30

        # 3. Khớp từ khóa / biệt danh học phần
        for kw in item.get('keywords', []):
            kw_norm = normalize_text(kw)
            if not kw_norm:
                continue
            kw_unacc = strip_vietnamese_accents(kw_norm)
            is_multi = ' ' in kw_norm

            if phrase_in_text(kw_norm, norm_query):
                score += 25 if is_multi else 20
            elif phrase_in_text(kw_unacc, unacc_query):
                score += 20 if is_multi else 16

        # 4. Khớp mô tả môn học theo từ khóa nội dung (loại trừ từ hỏi chung và từ quá ngắn)
        desc_matches = 0
        for token, u_token in zip(query_tokens, unacc_tokens):
            if u_token in GENERIC_QUERY_WORDS or len(u_token) < 3:
                continue
            if token in desc_tokens or u_token in desc_unacc_tokens:
                desc_matches += 1
        score += min(desc_matches * 2, 6)

        if score > 0:
            results.append((score, item))

    if not results:
        return []

    # Sắp xếp xác định: điểm số giảm dần, nếu bằng điểm sắp xếp theo mã môn A-Z
    results.sort(key=lambda x: (-x[0], x[1].get('code', '')))

    top_score = results[0][0]
    min_threshold = 12
    filtered = [item for score, item in results if score >= min_threshold and score >= top_score * 0.5]
    return filtered



def format_material_response(items):
    """Định dạng kết quả tìm kiếm tài liệu môn học thành Markdown"""
    if not items:
        return (
            "🔍 **StudyBot không tìm thấy tài liệu phù hợp với môn học này.**\n"
            "Hiện tại hệ thống đã cập nhật tài liệu cho các môn: *Công nghệ phần mềm (CNPM), "
            "Lập trình Python & AI, Hệ quản trị CSDL, Mạng máy tính, Cấu trúc dữ liệu & Giải thuật (CTDL), Lập trình Web*.\n"
            "Bạn có thể gõ: *\"tài liệu cnpm\"* hoặc *\"slide môn csdl\"* nhé!"
        )

    responses = ["📚 **TÀI LIỆU HỌC TẬP & HỌC PHẦN ĐƯỢC TÌM THẤY:**\n"]
    for idx, item in enumerate(items[:2], 1):
        responses.append(
            f"### {idx}. {item['name']} (`{item['code']}` - {item['credits']} Tín chỉ)\n"
            f"- **Tóm tắt nội dung:** {item['description']}\n"
            f"- **Sách/Giáo trình tham khảo:** *{item.get('reference_book', 'Đang cập nhật')}*\n"
            f"- 📥 **[Xem Giáo trình PDF]({item.get('syllabus', '#')})**\n"
            f"- 📂 **[Thư mục Slide bài giảng]({item.get('slides', '#')})**\n"
            f"- 📝 **[Ngân hàng Đề thi & Bài tập mẫu]({item.get('exam_sample', '#')})**\n"
        )

    responses.append("💡 *Mẹo: Bạn có thể bấm vào link Drive để tải trọn bộ bài giảng và đề ôn tập về máy.*")
    return "\n".join(responses)


def get_all_available_subjects():
    """Trả về danh mục tất cả các môn hiện có trong hệ thống"""
    materials = load_materials()
    lines = ["📖 **Danh mục các học phần hiện có tài liệu:**\n"]
    for item in materials:
        lines.append(f"- **{item['name']}** (`{item['code']}` - {item['credits']} TC)")
    lines.append("\nBạn có thể hỏi cụ thể, ví dụ: *\"Tài liệu môn " + (materials[0]['name'] if materials else 'CNPM') + "\"*.")
    return "\n".join(lines)

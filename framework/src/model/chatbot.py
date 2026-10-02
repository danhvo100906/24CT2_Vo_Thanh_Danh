import io
import json
import os
import random
import sys
import torch

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

PROCESSING_DIR = os.path.join(BASE_DIR, '..', 'processing')
if PROCESSING_DIR not in sys.path:
    sys.path.append(PROCESSING_DIR)

from neural_net import NeuralNet
from nltk_utils import bag_of_words, tokenize, normalize_vietnamese
from retrieval import search_materials, format_material_response

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load data intents
DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'intents.json')
if not os.path.exists(DATA_FILE):
    DATA_FILE = os.path.join(BASE_DIR, '..', '..', '..', 'data', 'intents.json')

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Load pretrained model
MODEL_FILE = os.path.join(BASE_DIR, 'data.pth')
data = torch.load(MODEL_FILE, map_location=device)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

BOT_NAME = "StudyBot"

INTENT_TITLES = {
    "chao_hoi": "Chào hỏi & Giới thiệu",
    "tam_biet": "Tạm biệt",
    "cam_on": "Cảm ơn",
    "tro_giup": "Hướng dẫn sử dụng",
    "tai_lieu_hoc_tap": "Tài liệu & Giáo trình môn học",
    "de_thi_on_tap": "Đề thi & Đề ôn tập",
    "thong_tin_hoc_phan": "Thông tin học phần & Tín chỉ",
    "hoi_kien_thuc": "Kiến thức CNTT cơ bản",
    "hoc_phi": "Học phí & Đơn giá tín chỉ",
    "han_dong_hoc_phi": "Hạn nộp & Gia hạn học phí",
    "cach_dong_hoc_phi": "Hướng dẫn & Cú pháp nộp học phí",
    "hoc_bong": "Chính sách học bổng",
    "quy_che_tin_chi": "Quy chế đào tạo & Điểm GPA",
    "thu_tuc_sinh_vien": "Thủ tục hành chính sinh viên",
    "lien_he": "Thông tin liên hệ phòng ban",
    "lop_24ct2": "Thông tin lớp 24CT2",
    "out_of_scope": "Chủ đề ngoài phạm vi hỗ trợ"
}


def predict_raw_intent(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    confidence = float(probs[0][predicted.item()].item())
    return tag, confidence


def get_response_details(msg):
    msg_clean = msg.strip()
    if not msg_clean:
        return {
            "response": "Bạn vui lòng nhập câu hỏi nhé!",
            "intent": "none",
            "confidence": 0.0,
            "status": "fallback"
        }

    # 1. Tìm kiếm tài liệu từ module retrieval
    matched_materials = search_materials(msg_clean)

    # 2. Kiểm tra độ phủ từ vựng miền học tập
    sentence_tokens = tokenize(msg_clean)
    known_tokens = [w for w in sentence_tokens if normalize_vietnamese(w) in all_words]
    oov_ratio = 1.0 - (len(known_tokens) / len(sentence_tokens)) if sentence_tokens else 0.0

    # 3. Dự đoán Intent bằng PyTorch Neural Network
    tag, confidence = predict_raw_intent(msg_clean)

    # Neu cau hoi co >= 30% tu ngu la hoan toan va khong phai cau chao hoi rat ngan
    if len(sentence_tokens) >= 4 and oov_ratio >= 0.30 and not matched_materials:
        tag = "out_of_scope"
        confidence = 0.95

    # 4. Ưu tiên xử lý Out of Scope
    if tag == "out_of_scope":
        for intent in intents['intents']:
            if intent['tag'] == 'out_of_scope':
                return {
                    "response": random.choice(intent['responses']),
                    "intent": "out_of_scope",
                    "confidence": confidence,
                    "status": "out_of_scope"
                }

    # 5. Ưu tiên trả về tài liệu môn học nếu người dùng hỏi về môn học cụ thể
    keywords_material = [
        'tài liệu', 'tai lieu', 'slide', 'giáo trình', 'giao trinh', 
        'đề thi', 'de thi', 'bài tập', 'bai tap', 'môn', 'hoc phan', 'học phần'
    ]
    is_asking_material = any(kw in msg_clean.lower() for kw in keywords_material)
    if matched_materials and (tag in ['tai_lieu_hoc_tap', 'de_thi_on_tap', 'thong_tin_hoc_phan'] or is_asking_material):
        actual_intent = tag if tag in ['tai_lieu_hoc_tap', 'de_thi_on_tap', 'thong_tin_hoc_phan'] else "tai_lieu_hoc_tap"
        return {
            "response": format_material_response(matched_materials),
            "intent": actual_intent,
            "confidence": max(confidence, 0.85),
            "status": "answered"
        }

    # 6. Độ tin cậy cao (HIGH >= 0.60) -> Trả lời trực tiếp
    if confidence >= 0.60:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return {
                    "response": random.choice(intent['responses']),
                    "intent": tag,
                    "confidence": confidence,
                    "status": "answered"
                }

    # 7. Độ tin cậy trung bình (MEDIUM 0.35 <= confidence < 0.60) -> Yêu cầu làm rõ
    if confidence >= 0.35:
        topic_name = INTENT_TITLES.get(tag, "chủ đề này")
        clarify_text = (
            f"🤔 **StudyBot chưa chắc chắn lắm:**\n"
            f"Có phải bạn đang muốn hỏi về **{topic_name}** không?\n\n"
            f"💡 *Bạn có thể bấm vào các nút gợi ý bên dưới hoặc đặt câu hỏi chi tiết hơn để mình hỗ trợ chính xác nhất nhé!*"
        )
        return {
            "response": clarify_text,
            "intent": tag,
            "confidence": confidence,
            "status": "clarified"
        }

    # 8. Safe Fallback
    fallback_text = (
        "Xin lỗi, mình chưa tìm thấy thông tin phù hợp trong dữ liệu học tập hiện có.\n"
        "StudyBot hiện hỗ trợ: *Tài liệu môn học, Học phí, Học bổng, Quy chế tín chỉ, Điểm GPA và Thủ tục sinh viên*.\n"
        "Bạn hãy thử chọn các nút gợi ý nhanh bên dưới nhé!"
    )
    return {
        "response": fallback_text,
        "intent": "out_of_scope",
        "confidence": confidence,
        "status": "fallback"
    }


def get_response(msg):
    return get_response_details(msg)["response"]

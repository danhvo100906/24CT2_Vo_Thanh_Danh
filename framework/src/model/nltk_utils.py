import re
import numpy as np


def normalize_vietnamese(text):
    """Chuẩn hóa ký tự và chữ thường"""
    if not text:
        return ""
    text = text.lower().strip()
    return text


def tokenize(sentence):
    """Tách câu thành các từ/token nhanh bằng biểu thức chính quy"""
    sentence = normalize_vietnamese(sentence)
    # Tách các từ tiếng Việt và chữ số
    tokens = re.findall(r'[a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệđìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+', sentence)
    return tokens


def bag_of_words(tokenized_sentence, words):
    """
    Trả về mảng bag of words:
    1 cho mỗi từ xuất hiện trong câu, 0 cho từ còn lại
    """
    sentence_words = [normalize_vietnamese(w) for w in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1.0
    return bag

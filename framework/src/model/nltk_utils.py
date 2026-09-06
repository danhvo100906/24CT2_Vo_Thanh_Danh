import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()


def tokenize(sentence):
    """Tách câu thành danh sách các từ/token"""
    return nltk.word_tokenize(sentence)


def stem(word):
    """Đưa từ về dạng gốc (ví dụ: organize, organizes -> organ)"""
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    """
    Trả về vector bag-of-words:
    1 nếu từ xuất hiện trong câu, 0 nếu không
    """
    sentence_words = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in sentence_words:
            bag[idx] = 1
    return bag
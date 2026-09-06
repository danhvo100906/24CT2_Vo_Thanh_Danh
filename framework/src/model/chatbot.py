import random
import json
import torch
import os
import sys

sys.path.append(os.path.dirname(__file__))

from neural_net import NeuralNet
from nltk_utils import bag_of_words, tokenize

BASE_DIR = os.path.dirname(__file__)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load dữ liệu intents
with open(os.path.join(BASE_DIR, '..', 'data', 'intents.json'), 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Load mô hình đã huấn luyện
FILE = os.path.join(BASE_DIR, 'data.pth')
data = torch.load(FILE, map_location=device)

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


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "Xin lỗi, mình chưa hiểu rõ câu hỏi này. Bạn có thể diễn đạt khác được không?"
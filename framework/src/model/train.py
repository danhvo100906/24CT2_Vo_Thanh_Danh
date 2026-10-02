import io
import json
import os
import sys

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from nltk_utils import tokenize, bag_of_words, normalize_vietnamese
from neural_net import NeuralNet

DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'intents.json')
if not os.path.exists(DATA_FILE):
    DATA_FILE = os.path.join(BASE_DIR, '..', '..', '..', 'data', 'intents.json')

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?', '!', '.', ',', ':', ';', '...', 'a', 'à', 'ơi', 'nhé', 'cho', 'với']
all_words = [normalize_vietnamese(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(f"Tổng số mẫu câu training: {len(xy)}")
print(f"Tổng số Intent tags: {len(tags)}")
print(f"Kích thước từ vựng (Vocabulary): {len(all_words)}")

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


num_epochs = 120
batch_size = 32
learning_rate = 0.005
input_size = len(all_words)
hidden_size = 64
output_size = len(tags)

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-4)

print("Bắt đầu huấn luyện mô hình PyTorch...")
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        outputs = model(words)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 30 == 0:
        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")

print(f"Hoàn tất huấn luyện. Final loss: {loss.item():.4f}")

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

OUTPUT_FILE = os.path.join(BASE_DIR, 'data.pth')
torch.save(data, OUTPUT_FILE)
print(f"Đã lưu mô hình thành công vào: {OUTPUT_FILE}")

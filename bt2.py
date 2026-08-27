from flask import Flask
import torch

app = Flask(__name__)

@app.route('/')
def home():
    # Lấy phiên bản PyTorch đang cài đặt trên máy
    pytorch_version = torch.__version__

    # Trả về giao diện HTML khớp chính xác với ảnh
    return f'''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>CNPM - DAU</title>
    </head>
    <body>
        <h1>Chào bạn khóa 24CT2 đến với học phần CNPM-DAU</h1>
        <h2>Thông tin</h2>
        <p><b>Phiên bản PyTorch:</b> {pytorch_version}</p>
        <p><b>Ngành nghề liên quan:</b> ( AI Engineer )</p>
        <p><b>Ngôn ngữ lập trình:</b> Python</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Chạy server ở port 5000
    app.run(debug=True, port=5000)
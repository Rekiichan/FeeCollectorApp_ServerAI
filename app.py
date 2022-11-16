from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS, cross_origin
from model import sum_predict
import cv2 as cv

# Khởi tạo Flask Server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = ''


@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*')
def predict():
    if request.method == 'POST':
        image = request.files['file']
        path = 'image_recognize.jpg'
        image.save(path)
        res = sum_predict(path)
        return res
    return ''


# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)


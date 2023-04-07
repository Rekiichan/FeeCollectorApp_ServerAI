from flask import Flask, request
from flask_cors import CORS, cross_origin
from model import predict
from datetime import datetime
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import numpy as np
import cv2 as cv
import os
import cloudinary as cd

# Khởi tạo Flask Server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = ''

# Config Cloudinary
cd.config(
    cloud_name="ds3knqnuh",
    api_key="382549695322695",
    api_secret="X20yMm21kH3OUU2va2SOR75lSIE",
    secure=True
)

@app.route('/predict', methods=['POST', 'GET'])
@cross_origin(origin='*')
def home():
    if request.method == 'POST':
        # request the image for detecting
        image = request.files['file'].read()

        # convert to np.uint8
        file_bytes = np.fromstring(image, np.uint8)

        # convert this matrix to rgb image
        img = cv.imdecode(file_bytes, cv.IMREAD_UNCHANGED)
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # detect image
        res = predict(imgRGB)

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-")
        
        img_name = dt_string+res

        upload(image, public_id=img_name)
        url, options = cloudinary_url(img_name)
        mydict = {'license_plate': res, 'image_link': url}
        return mydict

    if request.method == 'GET':
        return 'test'

    return 'no method detect'


# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

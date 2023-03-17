from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS, cross_origin
from model import predict
from datetime import datetime
import numpy as np
import cv2 as cv
import os

# Khởi tạo Flask Server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = ''

def checkResponseIsValid(lp):
    # check the license plate detected always have 8 or 9 character
    if (len(lp) < 8 or len(lp) > 9):
        return False
    # num1 is represent for 2 first number following city number    
    num1 = lp[0:2]

    # str1 is represent for 3rd character of the license plate, it is always non-number
    str1 = lp[2]

    # num2 is represent for the rest of the numbers from 4th character and it's always numbers
    num2 = lp[3:]

    # num for test the type of number
    num = 1
    if 'A' > str1 or 'Z' < str1:
        return False
    
    try:
        num = int(num1) + int(num2)
    except:
        return False
    if type(num) == int:
        return True
    return False

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

        #path for save image
        path = "images"
        
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:
        # Create a new directory because it does not exist
            os.makedirs(path)

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-")

        if checkResponseIsValid(res):
            img_name = dt_string+res+".png"
            cv.imwrite("images\\" + img_name, img)
            mydict = {'license_plate': res, 'image_link': img_name}
            return mydict
        else:
            return 'Detect license plate false! Please try again'
    if request.method == 'GET':
        return 'test'
    return 'no method detect'

# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

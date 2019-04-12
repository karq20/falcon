import sys
import urllib.request
import json
import cv2
import numpy as np
from flask import Flask, request, render_template
from flask_restful import Api, Resource
#from models import db
#from application import Application
import requests
from video import success

sys.path.append("/src/")

app = Flask(__name__)
api = Api(app)
VideoScreenshotURL = 'http://127.0.0.1:5001'

app.config['DEBUG'] = False

#class VideoScreen(Resource):
vidcap = cv2.VideoCapture('videos/1.mp4')
success, image = vidcap.read()
count = 0
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*5000))
    cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1

    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def verify():

    video_url = request.form['url']
    data = json.dumps({'url': video_url})
    url = VideoScreenshotURL + '/submit'
    response = requests.post(url, data=data)
    result = video.compare_faces(img1, img2)
    compare_result = {"RESULT": result}
    json_value = json.dumps(compare_result)
    return json_value

    return render_template('index.html', verify_result=verify_result, vidcap=video_url)

if __name__ == "__main__":
    app.run(port=5001)
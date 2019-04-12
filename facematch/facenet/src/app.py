import sys
import urllib.request
import json
import cv2
import numpy as np
from flask import Flask, request, render_template
from flask_restful import Api, Resource
from models import db
from application import Application
from .visualize import render_detect_results
import requests

sys.path.append("/src/")

app = Flask(__name__)
api = Api(app)
facenetapiURL = 'http://127.0.0.1:5001'
#   facenet.load_model("20170512-110547/20170512-110547.pb")
app.config['MODEL_PATH'] = '/Users/moneyview/Desktop/Face Detect:Recognition/facematchapi/facenet/src/utils/models/20170512-110547/20170512-110547.pb'

POSTGRES = {
    'user': 'moneyview',
    'pw': 'akash1997',
    'db': 'moneyview',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
with app.app_context():

    db.create_all()

application = Application(app.config['MODEL_PATH'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def verify():
    image_url1 = request.form['imageURL1']
    image_url2 = request.form['imageURL2']

    data = json.dumps({'url1': image_url1, 'url2': image_url2})
    url = facenetapiURL + '/face/compare'
    response = requests.post(url, data=data)
    verify_result = response.json()

    return render_template('index.html', verify_result=verify_result, image1=image_url1, image2=image_url2)

@app.route('/detect', methods=['POST'])
def detect():
    image_url = request.form['imageURL']

    data = json.dumps({'url': image_url})
    url = facenetapiURL + '/face/detect'
    response = requests.post(url, data=data)
    detected_faces = response.json()

    image = render_detect_results(image_url, detected_faces['detected_faces'])

    return render_template('index.html', detected_faces=detected_faces, image=image)

class FaceCompare(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        url1 = json_data['url1']
        url2 = json_data['url2']

        with urllib.request.urlopen(url1) as resp:
            img1 = np.asarray(bytearray(resp.read()), dtype="uint8")
            img1 = cv2.imdecode(img1, cv2.IMREAD_COLOR)

        with urllib.request.urlopen(url2) as resp:
            img2 = np.asarray(bytearray(resp.read()), dtype="uint8")
            img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)

        result = application.compare_faces(img1, img2)
        compare_result = {"RESULT": result}
        json_value = json.dumps(compare_result)
        return json_value


class FaceDetect(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        url = json_data['url']

        with urllib.request.urlopen(url) as resp:
            img = np.asarray(bytearray(resp.read()), dtype="uint8")
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        detected_faces = application.detect_faces(img)
        return {'detected_faces': detected_faces}

api.add_resource(FaceCompare, '/face/compare')
api.add_resource(FaceDetect, '/face/detect')

if __name__ == "__main__":
    app.run(port=5001)
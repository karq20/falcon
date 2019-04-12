from flask import Flask, render_template, request, redirect, jsonify
from visualize import render_detect_results
import requests, json
app = Flask(__name__)

facenetapiURL = 'http://127.0.0.1:5001'

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

if __name__ == '__main__':
    app.run()
@app.route('/detect', methods=['POST'])
def detect():
    image_url = request.form['imageURL']

    data = json.dumps({'url': image_url})
    url = facenetapiURL + '/face/detect'
    response = requests.post(url, data=data)
    detected_faces = response.json()

    image = render_detect_results(image_url, detected_faces['detected_faces'])

    return render_template('index.html', detected_faces=detected_faces, image=image)



class FaceDetect(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        url = json_data['url']

        with urllib.request.urlopen(url) as resp:
            img = np.asarray(bytearray(resp.read()), dtype="uint8")
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        detected_faces = application.detect_faces(img)
        return {'detected_faces': detected_faces}


    class FindSimilar(Resource):
        def post(self):
            json_data = request.get_json(force=True)
            url = json_data['url']
            return None


        api.add_resource(FaceDetect, '/face/detect')


        vidcap = cv2.VideoCapture('videos/')
success, image = vidcap.read()
count = 0
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*5000))
    cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1

    cv2.destroyAllWindows()
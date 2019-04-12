import cv2
def screenshot():

    vidcap = cv2.VideoCapture('/Users/moneyview/Downloads/facematch/videos/jurrasic_park_intro.mp4')
    success, image = vidcap.read()
    count = 0
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*5000))
    cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1

    cv2.destroyAllWindows()
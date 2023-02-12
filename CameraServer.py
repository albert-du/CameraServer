import threading
from flask import Flask, make_response
from cv2 import VideoCapture
import cv2

app = Flask(__name__)

height = 1080
width = 1920

cameras = dict()

lock = threading.Lock()

def getCamera(index):
    cam = cameras.get(index)
    if cam is None:
        cam = VideoCapture(int(index))
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cameras[index] = cam
    return cam


@app.route("/")
def hello_world():
    return "<p>Camera Server</p>"


@app.route("/picture/<index>")
def picture(index):
    lock.acquire()
    try:
        cam = getCamera(index)
        result, image = cam.read()
        if result:
            x = int((width - height) / 2)
            image = image[0: height, x: x + height]
            result, png = cv2.imencode(".png", image)
            response = make_response(png.tobytes())
            response.headers.set('Content-Type', 'image/png')
            app.logger.info('Picture taken on camera %s', index)
            return response
        else:
            app.logger.info('Failed to take picture on camera %s', index)
            return "Could not take picture.", 400
    finally:
        lock.release()

@app.route("/alignment/<index>")
def alignment(index):
    lock.acquire()
    try:
        cam = getCamera(index)
        result, image = cam.read()
        if result:
            x = int((width - height) / 2)
            image = image[0: height, x: x + height]
            cheight = image.shape[0]
            cwidth = image.shape[1]
            cv2.line(image, (0, 0), (cwidth, cheight), (127, 127, 127), 5)
            cv2.line(image, (cwidth, 0), (0, cheight), (127, 127, 127), 5)
            result, png = cv2.imencode(".png", image)
            response = make_response(png.tobytes())
            response.headers.set('Content-Type', 'image/png')
            app.logger.info('Alignment picture taken on camera %s', index)
            return response
        else:
            app.logger.info('Failed to take alignment picture on camera %s', index)
            return "Could not take picture.", 400
    finally:
        lock.release()
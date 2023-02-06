from flask import Flask, make_response
from cv2 import VideoCapture
import cv2

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Camera Server</p>"


@app.route("/picture/<index>")
def picture(index):
    cam = VideoCapture(int(index))
    result, image = cam.read()
    if result:
        result, png = cv2.imencode(".png", image)
        response = make_response(png.tobytes())
        response.headers.set('Content-Type', 'image/png')
        return response
    else:
        return "Could not take picture.", 400

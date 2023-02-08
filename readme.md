# CameraServer

Returns a png from the webcam on a get request to /picture/{cameraIndex}.

## Setup
* `python -m venv venv`
* `.\Scripts\activate` (Windows), `source ./bin/activate` (Linux/Mac) 
* `pip install opencv.python flask waitress`

## Run
* `waitress-serve --host 127.0.0.1 --port 7701 CameraServer:app`

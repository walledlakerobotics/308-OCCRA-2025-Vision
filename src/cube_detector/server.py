import cv2
from flask import Flask, Response
from .camera import Camera

app = Flask(__name__, static_url_path="/")


def generate_camera_feed(index: int):
    camera = Camera(index)
    
    while True:
        ret, frame = camera.read()
        if not ret:
            continue

        img = cv2.imencode(".jpg", frame)[1].tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + img)


@app.route("/stream/<int:index>")
def stream(index: int):
    return Response(
        generate_camera_feed(index),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/index.html")
def index_redirect():
    return app.redirect("/")


@app.route("/")
def index():
    return app.send_static_file("index.html")

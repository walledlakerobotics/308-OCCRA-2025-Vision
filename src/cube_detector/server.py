import cv2

from cv2_enumerate_cameras import enumerate_cameras
from flask import Flask, Response
from .camera import Camera

app = Flask(__name__, static_url_path="/")


@app.route("/stream/<string:name>/<int:index>")
def stream(name: str, index: int):
    camera = Camera(index)

    return camera.stream(name)


@app.route("/index.html")
def index_redirect():
    return app.redirect("/")


@app.route("/")
def index():
    return app.send_static_file("index.html")

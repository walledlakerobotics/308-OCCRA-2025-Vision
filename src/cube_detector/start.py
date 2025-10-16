import waitress
import cv2
import sys
import time

from threading import Thread

from .camera import Camera
from .server import app

from cv2_enumerate_cameras import enumerate_cameras

def test_stream():
    camera = Camera(0)

    frame: cv2.typing.MatLike

    camera.reg_stream("test", lambda: frame)

    while True:
        ret, frame = camera.read()
        if not ret:
            time.sleep(0.01)
            continue

        # Define text properties
        text = "Hello, OpenCV!"
        org = (50, 150)  # Bottom-left corner of the text
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1.5
        color = (0, 0, 255) # Red color in BGR
        thickness = 2
        lineType = cv2.LINE_AA

        # Put the text on the image
        cv2.putText(frame, text, org, fontFace, fontScale, color, thickness, lineType)

def get_preffered_api():
    if sys.platform == "win32":
        return cv2.CAP_MSMF
    elif sys.platform == "darwin":
        return cv2.CAP_AVFOUNDATION
    else:
        return cv2.CAP_V4L2


def start():
    Thread(target=test_stream, daemon=True).start()

    for camera in enumerate_cameras(get_preffered_api()):
        print(camera, camera.path)

    waitress.serve(app, host="0.0.0.0", port=5800, threads=8)


if __name__ == "__main__":
    start()

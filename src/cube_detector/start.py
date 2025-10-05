import cv2
import waitress

from threading import Thread
from .server import app


def cv():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def start():
    cv_thread = Thread(target=cv, daemon=True)
    cv_thread.start()

    waitress.serve(app, host="0.0.0.0", port=80)


if __name__ == "__main__":
    start()

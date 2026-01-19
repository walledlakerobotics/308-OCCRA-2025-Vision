from threading import Thread

import cv2
import waitress
from cv2_enumerate_cameras import enumerate_cameras

from .cameras import get_api
from .pipeline import start_all
from .server import app

from .pipeline import pipeline


def start():
    frame = cv2.imread("test_images/test1.jpg")
    if frame is None:
        return

    h, w = frame.shape[:2]
    aspect_ratio = w / h

    new_width = 500  # Desired width
    new_height = int(new_width / aspect_ratio)
    resized_frame = cv2.resize(
        frame, (new_width, new_height), interpolation=cv2.INTER_AREA
    )

    processed_frame = pipeline(resized_frame, "")
    cv2.imshow("Processed Frame", processed_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # for camera in enumerate_cameras(get_api()):
    #     print(camera, camera.path)

    # start_all()

    # waitress.serve(app, host="0.0.0.0", port=5800, threads=8)


if __name__ == "__main__":
    start()

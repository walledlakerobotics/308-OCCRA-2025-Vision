from itertools import chain
from threading import Thread
from types import EllipsisType
from typing import Callable

import cv2
import numpy as np
from cv2.typing import MatLike

from .cameras import Camera
from .config import config
from .streams import Stream

started: dict[str, bool] = {}

YELLOW_LOWER = np.array([20, 0, 0])
YELLOW_UPPER = np.array([23, 255, 255])

# yellow_lower = np.array([24, 160, 100])
# yellow_upper = np.array([27, 255, 255])

WHITE_LOWER = np.array([0, 0, 100])
WHITE_UPPER = np.array([180, 45, 255])

CANNY_THRESH_1 = 85
CANNY_THRESH_2 = 180

CUBE_EDGE_LENGTH = 0.3048  # 1 ft
FACE_OBJECT_POINTS = np.array(
    [
        [0, 0, 0],
        [CUBE_EDGE_LENGTH, 0, 0],
        [CUBE_EDGE_LENGTH, CUBE_EDGE_LENGTH, 0],
        [0, CUBE_EDGE_LENGTH, 0],
    ],
    dtype=np.float32,
)


def pipeline(frame: MatLike, name: str) -> MatLike:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)
    white_mask = cv2.inRange(hsv, WHITE_LOWER, WHITE_UPPER)

    kernel_size = 2
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, kernel)

    edges = cv2.bitwise_not(edges)

    yellow_mask = cv2.bitwise_and(yellow_mask, edges)
    white_mask = cv2.bitwise_and(white_mask, edges)

    yellow_contours, _ = cv2.findContours(
        yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    white_contours, _ = cv2.findContours(
        white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not yellow_contours and not white_contours:
        return frame

    # contours = chain(yellow_contours or (), white_contours or ())
    contours = yellow_contours

    contour = max(contours, key=cv2.contourArea)

    polygon = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    cv2.polylines(frame, [polygon], True, (242, 224, 143))

    if not len(polygon) == 4:
        return frame

    corners = polygon.astype(np.float32)

    image_points = cv2.cornerSubPix(
        gray,
        corners,
        (5, 5),
        (-1, -1),
        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001),
    )

    ret, rvecs, tvecs, reprojection_errors = cv2.solvePnPGeneric(
        FACE_OBJECT_POINTS,
        image_points,
        np.array(
            [
                [615.0, 0.0, 0],
                [0.0, 615.0, 0],
                [0.0, 0.0, 1.0],
            ]
        ),
        np.array([0.0, 0.0, 0.0, 0.0]),
        flags=cv2.SOLVEPNP_IPPE_SQUARE,
    )

    if not ret:
        return frame

    best_rvec = None
    best_tvec = None
    lowest_error = float("inf")

    for rvec, tvec, rp_err in zip(rvecs, tvecs, reprojection_errors):
        if rp_err < lowest_error and tvec[2] > 0:
            best_rvec = rvec
            best_tvec = tvec
            lowest_error = rp_err

    if best_rvec is None or best_tvec is None:
        return frame

    print(best_rvec, best_tvec, lowest_error)

    return frame


def run_pipeline(pipeline: Callable, name: str):
    camera = Camera(name)
    stream = Stream(f"{name}/processed")

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                continue

            processed_frame = pipeline(frame, name)
            stream.send(processed_frame)
    finally:
        started[name] = False


def start(name: str):
    if name in started and started[name] is True:
        return

    started[name] = True

    Thread(target=run_pipeline, args=(pipeline, name), daemon=True).start()


def start_all():
    for name in config.cameras:
        start(name)

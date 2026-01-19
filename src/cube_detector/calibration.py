from threading import Event
from typing import Sequence

import cv2
from cv2 import aruco
from cv2.aruco import CharucoBoard, CharucoDetector
from cv2.typing import MatLike

from .cameras import Camera
from .config import config
from .streams import Stream


def calibration_process(
    name: str,
    horizontal: int,
    vertical: int,
    square_length: int,
    marker_length: int,
    save_frame: Event,
    run_calibration: Event,
):
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

    board = CharucoBoard(
        (vertical, horizontal), square_length, marker_length, dictionary
    )
    detector = CharucoDetector(board)

    camera = Camera(name)
    stream = Stream("calibration")

    saved_detections: list[tuple[MatLike, MatLike, Sequence[MatLike], MatLike]] = []

    gray = None

    while not run_calibration.is_set() or len(saved_detections) < 10:
        ret, frame = camera.read()
        if not ret:
            continue

        frame_copy = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detection = detector.detectBoard(gray)
        charuco_corners, _, marker_corners, _ = detection

        if charuco_corners is not None and len(charuco_corners) > 3:
            aruco.drawDetectedMarkers(frame_copy, marker_corners)
            aruco.drawDetectedCornersCharuco(frame_copy, charuco_corners)

            if save_frame.is_set():
                save_frame.clear()

                saved_detections.append(detection)

        for charuco_corners, _, marker_corners, _ in saved_detections:
            aruco.drawDetectedMarkers(frame_copy, marker_corners)
            aruco.drawDetectedCornersCharuco(frame_copy, charuco_corners)

        stream.send(frame_copy)

        if len(saved_detections) < 10 and run_calibration.is_set():
            run_calibration.clear()

    all_charuco_corners: list[MatLike] = [
        charuco_corners for charuco_corners, _, _, _ in saved_detections
    ]
    all_charuco_ids: list[MatLike] = [
        charuco_ids for _, charuco_ids, _, _ in saved_detections
    ]

    if gray is not None:
        size = gray.shape[::-1]
    else:
        size = (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT)

    _, camera_matrix, dist_coeffs, _, _ = aruco.calibrateCameraCharuco(
        all_charuco_corners, all_charuco_ids, board, size, None, None  # type: ignore
    )

    config.camera_matricies[name] = camera_matrix
    config.dist_coeffs[name] = dist_coeffs

    config.save()

    print("Done calibrating!")
    print(camera_matrix)
    print(dist_coeffs)

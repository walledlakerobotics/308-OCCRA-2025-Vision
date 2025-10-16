import cv2
import numpy as np
import time
import sys

from flask import Response, abort
from cv2_enumerate_cameras import enumerate_cameras
from cv2_enumerate_cameras.camera_info import CameraInfo

from threading import Thread, Lock, Event

from typing import Callable, ClassVar, overload

type Frame = cv2.typing.MatLike


def get_preffered_api():
    if sys.platform == "win32":
        return cv2.CAP_MSMF
    elif sys.platform == "darwin":
        return cv2.CAP_AVFOUNDATION
    else:
        return cv2.CAP_V4L2


def get_index_for_path(path: str) -> int | None:
    for camera in enumerate_cameras(get_preffered_api()):
        if camera.path == path:
            return camera.index


def read_camera(path: str, stop: Event, init_done: Event):
    index = get_index_for_path(path)
    if index is None:
        abort(404)

    camera = cv2.VideoCapture(index)

    init_done.set()

    while not stop.is_set():
        Camera.frames[path] = camera.read()
        time.sleep(0.01)

    del Camera.frames[path]

    with Camera.stop_events_lock:
        del Camera.stop_events[path]


class Camera:
    frames: ClassVar[dict[str, tuple[bool, Frame]]] = {}

    streams: ClassVar[dict[str, dict[str, Callable[[], Frame]]]] = {}
    streams_lock: ClassVar[Lock] = Lock()

    stop_events: ClassVar[dict[str, Event]] = {}
    stop_events_lock: ClassVar[Lock] = Lock()

    num_instances: ClassVar[dict[str, int]] = {}
    num_instances_lock: ClassVar[Lock] = Lock()

    path: str

    def __init__(self, path: str):
        self.path = path

        with Camera.stop_events_lock:
            if self.path not in Camera.stop_events:
                Camera.stop_events[self.path] = Event()

                init_done = Event()
                Thread(
                    target=read_camera,
                    args=(path, Camera.stop_events[self.path], init_done),
                ).start()

                init_done.wait()

        with Camera.num_instances_lock:
            if self.path not in Camera.num_instances:
                Camera.num_instances[self.path] = 0

            Camera.num_instances[self.path] += 1

        with Camera.streams_lock:
            if self.path not in Camera.streams:
                Camera.streams[self.path] = {}

    def read_nocopy(self) -> tuple[bool, Frame]:
        if self.path not in Camera.frames:
            return (
                False,
                np.zeros(
                    [cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_WIDTH, 3],
                    np.uint8,
                ),
            )

        return Camera.frames[self.path]

    def read(self) -> tuple[bool, Frame]:
        if self.path not in Camera.frames:
            return (
                False,
                np.zeros(
                    [cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_WIDTH, 3],
                    np.uint8,
                ),
            )

        ret, frame = Camera.frames[self.path]
        frame = frame.copy()

        return ret, frame

    @overload
    def stream(self) -> Response:
        pass

    @overload
    def stream(self, name: str) -> Response:
        pass

    def stream(self, name: str | None = None) -> Response:
        read: Callable[[], Frame]

        if name is None or name == "raw":
            read = lambda: self.read()[1]
        else:
            with Camera.streams_lock:
                if name not in Camera.streams[self.path]:
                    abort(404)

                read = Camera.streams[self.path][name]

        def gen_frames():
            while True:
                frame = read()

                img = cv2.imencode(".jpg", frame)[1].tobytes()

                yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + img)

        return Response(
            gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )

    def reg_stream(self, name: str, read: Callable[[], Frame]):
        with Camera.streams_lock:
            Camera.streams[self.path][name] = read

    def __del__(self):
        with Camera.num_instances_lock:
            Camera.num_instances[self.path] -= 1

            if not Camera.num_instances[self.path]:
                del Camera.num_instances[self.path]

                with Camera.stop_events_lock:
                    Camera.stop_events[self.path].set()


__all__ = ["Camera"]

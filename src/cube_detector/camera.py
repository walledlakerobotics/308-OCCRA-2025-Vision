import cv2
import numpy as np
import time

from flask import Response, abort
from cv2_enumerate_cameras.camera_info import CameraInfo

from threading import Thread, Lock, Event

from typing import Callable, ClassVar, overload

type Frame = cv2.typing.MatLike


def read_camera(index: int, stop: Event, init_done: Event):
    camera = cv2.VideoCapture(index)

    init_done.set()

    while not stop.is_set():
        Camera.frames[index] = camera.read()
        time.sleep(0.01)

    del Camera.frames[index]

    with Camera.stop_events_lock:
        del Camera.stop_events[index]


class Camera:
    frames: ClassVar[dict[int, tuple[bool, Frame]]] = {}

    streams: ClassVar[dict[int, dict[str, Callable[[], Frame]]]] = {}
    streams_lock: ClassVar[Lock] = Lock()

    stop_events: ClassVar[dict[int, Event]] = {}
    stop_events_lock: ClassVar[Lock] = Lock()

    num_instances: ClassVar[dict[int, int]] = {}
    num_instances_lock: ClassVar[Lock] = Lock()

    index: int

    def __init__(self, index: int):
        self.index = index

        with Camera.stop_events_lock:
            if self.index not in Camera.stop_events:
                Camera.stop_events[self.index] = Event()

                init_done = Event()
                Thread(
                    target=read_camera,
                    args=(index, Camera.stop_events[self.index], init_done),
                ).start()

                init_done.wait()

        with Camera.num_instances_lock:
            if self.index not in Camera.num_instances:
                Camera.num_instances[self.index] = 0

            Camera.num_instances[self.index] += 1

        with Camera.streams_lock:
            if self.index not in Camera.streams:
                Camera.streams[self.index] = {}

    def read_nocopy(self) -> tuple[bool, Frame]:
        if self.index not in Camera.frames:
            return (
                False,
                np.zeros(
                    [cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_WIDTH, 3],
                    np.uint8,
                ),
            )

        return Camera.frames[self.index]

    def read(self) -> tuple[bool, Frame]:
        if self.index not in Camera.frames:
            return (
                False,
                np.zeros(
                    [cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_WIDTH, 3],
                    np.uint8,
                ),
            )

        ret, frame = Camera.frames[self.index]
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
                if name not in Camera.streams[self.index]:
                    abort(404)

                read = Camera.streams[self.index][name]

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
            Camera.streams[self.index][name] = read

    def __del__(self):
        with Camera.num_instances_lock:
            Camera.num_instances[self.index] -= 1

            if not Camera.num_instances[self.index]:
                del Camera.num_instances[self.index]

                with Camera.stop_events_lock:
                    Camera.stop_events[self.index].set()


__all__ = ["Camera"]

import cv2
import numpy as np
import time

from flask import Response
from typing import ClassVar
from queue import Empty, Queue
from threading import Thread, Lock

type Frame = cv2.typing.MatLike
type FrameQueue = Queue[Frame]


def read_camera(index: int):
    camera = cv2.VideoCapture(index)

    while True:
        ret, frame = camera.read()
        if not ret:
            time.sleep(0.01)
            continue

        with Camera.queue_locks[index]:
            if index not in Camera.queues:
                del Camera.queue_locks[index]
                break

            for i, q in enumerate(Camera.queues[index]):
                if i == 0:
                    q.put(frame)  # don't create extra copy
                    continue

                q.put(frame.copy())


class Camera:
    queues: ClassVar[dict[int, list[FrameQueue]]] = {}
    queue_locks: ClassVar[dict[int, Lock]] = {}

    streams: ClassVar[dict[int, dict[str, FrameQueue]]] = {}
    stream_locks: ClassVar[dict[int, Lock]] = {}

    index: int
    queue: FrameQueue

    def __init__(self, index: int):
        self.index = index
        self.queue = Queue(maxsize=1)

        if not self.index in Camera.queue_locks:
            Camera.queue_locks[self.index] = Lock()
            Camera.stream_locks[self.index] = Lock()

        with Camera.queue_locks[self.index]:
            if self.index not in Camera.queues:
                Camera.queues[self.index] = []
                thread = Thread(target=read_camera, args=(self.index,))
                thread.start()

            Camera.queues[self.index].append(self.queue)

        with Camera.stream_locks[self.index]:
            Camera.streams[self.index] = {}

    def __del__(self):
        with Camera.queue_locks[self.index]:
            Camera.queues[self.index].remove(self.queue)

            if not Camera.queues[self.index]:
                del Camera.queues[self.index]

    def read(self) -> tuple[bool, Frame]:
        try:
            return True, self.queue.get_nowait()
        except Empty:
            return False, np.zeros((480, 640, 3), dtype=np.uint8)

    def stream(self, name: str):
        with Camera.stream_locks[self.index]:
            if name not in Camera.streams[self.index]:
                Camera.streams[self.index][name] = Queue(maxsize=1)

            return self.Stream(Camera.streams[self.index][name])

    @classmethod
    def stream_response(cls, index: int, name: str):
        camera = Camera(index)

        if name == "raw":
            stream = camera
        else:
            stream = camera.stream(name)

        def gen_frames():
            while True:
                ret, frame = stream.read()
                if not ret:
                    continue

                img = cv2.imencode(".jpg", frame)[1].tobytes()

                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + img)

        return Response(
            gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )

    class Stream:
        queue: FrameQueue

        def __init__(self, queue: FrameQueue):
            self.queue = queue

        def send(self, frame: Frame):
            self.queue.put(frame)

        def read(self) -> tuple[bool, Frame]:
            try:
                return True, self.queue.get_nowait()
            except Empty:
                return False, np.zeros((480, 640, 3), dtype=np.uint8)

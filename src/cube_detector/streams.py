from threading import Event, Lock
from typing import Any, ClassVar, Generator, overload
import weakref

import cv2
from cv2.typing import MatLike


class Stream:
    streams: ClassVar[dict[str, tuple[bool, MatLike]]] = {}

    _send_events: ClassVar[dict[str, Event]] = {}

    _num_instances: ClassVar[dict[str, int]] = {}
    _num_instances_lock: ClassVar[Lock] = Lock()

    route: str
    _finalizer: weakref.finalize

    def __init__(self, route: str):
        self.route = route

        if self.route not in Stream._send_events:
            Stream._send_events[self.route] = Event()

        with Stream._num_instances_lock:
            if self.route not in Stream._num_instances:
                Stream._num_instances[self.route] = 0

            Stream._num_instances[self.route] += 1

        def delete():
            with Stream._num_instances_lock:
                Stream._num_instances[self.route] -= 1

                if Stream._num_instances[self.route] <= 0:
                    del Stream.streams[self.route]
                    del Stream._send_events[self.route]
                    del Stream._num_instances[self.route]

        self._finalizer = weakref.finalize(self, delete)

    @overload
    def send(self, frame: MatLike) -> None:
        pass

    @overload
    def send(self, frame: tuple[bool, MatLike]) -> None:
        pass

    def send(self, frame: MatLike | tuple[bool, MatLike]):
        if not isinstance(frame, tuple):
            frame = (True, frame)

        Stream.streams[self.route] = frame
        Stream._send_events[self.route].set()

    def generate(self) -> Generator[bytes, Any, None]:
        while True:
            if self.route not in Stream.streams:
                return

            ret, frame = Stream.streams[self.route]
            if not ret:
                continue

            img = cv2.imencode(".jpg", frame)[1].tobytes()

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + img)

            Stream._send_events[self.route].wait()

    @staticmethod
    def exists(route: str) -> bool:
        return route in Stream.streams

import sys
from threading import Event, Thread
from typing import ClassVar, NoReturn

import casefy
import cv2
import networktables
from cv2.typing import MatLike
from cv2_enumerate_cameras import enumerate_cameras

from .config import config
from .streams import Stream


def get_api():
    match sys.platform:
        case "win32":
            return cv2.CAP_MSMF
        case "darwin":
            return cv2.CAP_AVFOUNDATION
        case _:
            return cv2.CAP_V4L2


def get_index_for_path(path: str) -> int | None:
    for camera in enumerate_cameras(get_api()):
        if camera.path == path:
            return camera.index


def get_route_name(name: str):
    return casefy.kebabcase(name)


def camera_loop(name: str, path: str, init_done: Event) -> NoReturn | None:
    index = get_index_for_path(path)
    if index is None:
        return

    camera = cv2.VideoCapture(index)
    stream = Stream(f"{get_route_name(name)}/raw")

    networktables.NetworkTables.initialize("localhost")
    table = networktables.NetworkTables.getTable("CameraPublisher").getSubTable(name)

    table.putString("mode", "0x0 Unknown")
    table.putStringArray("modes", [])
    table.putString("description", name)
    table.putString("source", config.cameras[name])
    table.putStringArray(
        "streams", [f"mjpg:http://localhost:5800/stream/{stream.route}"]
    )

    Camera.frames[name] = camera.read()
    stream.send(Camera.frames[name])

    init_done.set()

    while True:
        Camera.frames[name] = camera.read()
        stream.send(Camera.frames[name])

        table.putBoolean("connected", camera.isOpened())


class Camera:
    frames: ClassVar[dict[str, tuple[bool, MatLike]]] = {}
    name: str

    def __init__(self, name: str):
        if name not in Camera.frames:
            path = config.cameras[name]
            init_done = Event()

            Thread(target=camera_loop, args=(name, path, init_done), daemon=True).start()
            init_done.wait()

        self.name = name

    def read(self) -> tuple[bool, MatLike]:
        ret, frame = Camera.frames[self.name]
        return (ret, frame.copy())

    @property
    def route_name(self):
        return get_route_name(self.name)

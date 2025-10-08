import cv2
import numpy as np
from queue import Empty, Queue
from threading import Thread, Lock


def read_camera(index: int):
    camera = cv2.VideoCapture(index)

    while True:
        ret, frame = camera.read()
        if not ret:
            continue

        with Camera.queue_locks[index]:
            if index not in Camera.queues:
                del Camera.queue_locks[index]
                break

            for i, q in enumerate(Camera.queues[index]):
                if i == 0:
                    q.put(frame) # don't create extra copy
                    continue

                q.put(frame.copy())


class Camera:
    queues: dict[int, list[Queue]] = {}
    queue_locks: dict[int, Lock] = {}

    index: int
    queue: Queue[cv2.typing.MatLike]

    def __init__(self, index: int):
        if not index in Camera.queue_locks:
            Camera.queue_locks[index] = Lock()

        with Camera.queue_locks[index]:
            if index not in Camera.queues:
                Camera.queues[index] = []
                thread = Thread(target=read_camera, args=(index,))
                thread.start()

            self.index = index
            self.queue = Queue(maxsize=1)
            
            Camera.queues[index].append(self.queue)

    def __del__(self):
        with Camera.queue_locks[self.index]:
            Camera.queues[self.index].remove(self.queue)

            if not Camera.queues[self.index]:
                del Camera.queues[self.index]

    def read(self) -> tuple[bool, cv2.typing.MatLike]:
        try:
            return True, self.queue.get_nowait()
        except Empty:
            return False, np.zeros((480, 640, 3), dtype=np.uint8)

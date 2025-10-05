import cv2
from . import server


def main():
    httpd = server.start()

    camera = None

    try:
        camera = cv2.VideoCapture(0)

        while True:
            ret, frame = camera.read()
            if not ret:
                break

            cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        camera.release() if camera else None
        
        httpd.shutdown()

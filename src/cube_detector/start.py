import waitress

from .server import app


def start():
    waitress.serve(app, host="0.0.0.0", port=80)


if __name__ == "__main__":
    start()

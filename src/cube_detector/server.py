from threading import Event, Thread

from flask import Flask, Response, abort, jsonify, send_file

from .calibration import calibration_process
from .streams import Stream

app = Flask(__name__, static_url_path="/")


@app.route("/stream/<path:route>")
def stream(route: str):
    if not Stream.exists(route):
        abort(404)

    stream = Stream(route)

    return Response(
        stream.generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


run_calibration_event = Event()
save_frame_event = Event()


@app.route("/calibration/start/<string:path>/")
def start_calibration(path: str):
    Thread(
        target=lambda: calibration_process(
            path, 5, 7, 30, 15, save_frame_event, run_calibration_event
        ),
        daemon=True,
    ).start()

    return Response(status=200)


@app.route("/calibration/save")
def save_calibration_frame():
    save_frame_event.set()

    return Response(status=200)


@app.route("/calibration/run")
def run_calibration():
    run_calibration_event.set()

    return Response(status=200)


@app.route("/config")
def config():
    try:
        return send_file("./config.json")
    except FileNotFoundError:
        return jsonify({})


@app.route("/index.html")
def index_redirect():
    return app.redirect("/")


@app.route("/")
def index():
    return app.send_static_file("index.html")
    return app.send_static_file("index.html")

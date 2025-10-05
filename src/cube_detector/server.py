from wsgiref.simple_server import make_server
from threading import Thread
from flask import Flask

app = Flask(__name__, static_url_path="")


@app.route("/index.html")
def index_redirect():
    return app.redirect("/")


@app.route("/")
def index():
    return app.send_static_file("index.html")


def start():
    httpd = make_server("0.0.0.0", 80, app)
    Thread(target=httpd.serve_forever).start()

    return httpd

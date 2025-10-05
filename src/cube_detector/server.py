from flask import Flask

app = Flask(__name__, static_url_path="/")


@app.route("/index.html")
def index_redirect():
    return app.redirect("/")


@app.route("/")
def index():
    return app.send_static_file("index.html")

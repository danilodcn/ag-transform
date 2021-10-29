from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/2")
def hello_world2():
    return "<p>Hello, World!</p>"

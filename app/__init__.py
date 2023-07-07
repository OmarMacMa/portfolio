from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/experience")
def experience():
    return render_template("experience.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
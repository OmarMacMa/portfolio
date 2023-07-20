import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict


load_dotenv()


app = Flask(__name__)


mydb = MySQLDatabase(
    database=os.getenv("MYSQL_DB"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)
print(mydb)


class TimeLinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimeLinePost])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="404 | Not found"), 404


@app.route("/")
def index():
    return render_template("index.html", title="MLH Fellow")


@app.route("/experience")
def experience():
    return render_template("experience.html", title="Experience")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", title="Portfolio")


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline")


# API Endpoints
@app.route("/api/time_line_post", methods=["POST"])
def post_time_line_post():
    name = request.form["timeline-name"]
    email = request.form["timeline-email"]
    content = request.form["timeline-content"]
    time_line_post = TimeLinePost.create(
        name=name, email=email, content=content)
    return model_to_dict(time_line_post)


@app.route("/api/time_line_post", methods=["GET"])
def get_time_line_post():
    return {
        "time_line_posts": [
            model_to_dict(p)
            for p in TimeLinePost.select().order_by(TimeLinePost.created_at.desc())
        ]
    }


@app.route("/api/time_line_post", methods=["DELETE"])
def delete_time_line_post():
    post_id = request.form["id"]
    post = TimeLinePost.get_by_id(post_id)
    TimeLinePost.delete_by_id(post_id)
    return model_to_dict(post)

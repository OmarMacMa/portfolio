import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict


load_dotenv()


app = Flask(__name__)

#Set up im-memory SQLite Db for testing, otherwise use MySQL
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',uri=True)
else:
    mydb = MySQLDatabase(
        database=os.getenv("MYSQL_DATABASE"),
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
    return render_template("index.html", title="Me")


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
    #Validate name
    if not request.form.get('timeline-name') or request.form['timeline-name'] == "":         
        return {"error": "Invalid name"}, 400
    
    #Validate email
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9]+\.[A-Z|a-z]{2,}\b'
    if not request.form.get('timeline-email') or request.form['timeline-email'] == "" or not re.fullmatch(regex, request.form['timeline-email']):
        return {"error": "Invalid email"}, 400
    
    #Validate content
    if not request.form.get('timeline-content') or request.form['timeline-content'] == "":
        return {"error": "Invalid content"}, 400    
    
    name = request.form["timeline-name"]
    email = request.form["timeline-email"]
    content = request.form["timeline-content"]

    time_line_post = TimeLinePost.create(
        name=name, email=email, content=content)
    
    return model_to_dict(time_line_post)


@app.route("/api/time_line_post", methods=["GET"])
def get_time_line_post():
    time_line_posts =[]
    for post in TimeLinePost.select().order_by(TimeLinePost.created_at.desc()):
        time_line_posts.append(model_to_dict(post))
    return {"time_line_posts": time_line_posts}


@app.route("/api/time_line_post", methods=["DELETE"])
def delete_time_line_post():
    post_id = request.form["id"]
    post = TimeLinePost.get_by_id(post_id)
    TimeLinePost.delete_by_id(post_id)
    return model_to_dict(post)

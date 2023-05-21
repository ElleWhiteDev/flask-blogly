"""Blogly application."""

from flask import Flask, render_template, session, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    return redirect("/users")

@app.route("/users")
def list_users():
    return render_template("users.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]

    return render_template("new-user-form.html", first-name=first_name, last-name=last_name, img-url=img_url)

@app.route("/users/<user.id>")
def user_details():
    return render_template("user-detail.html")

@app.route("/users/<user.id>/edit", methods=["POST"])
def edit_user():
    return render_template("user-detail.html")

@app.route("/users/<user.id>/delete", methods=["POST"])
def delete_user():
    return redirect("/users")

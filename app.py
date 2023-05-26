"""Blogly application."""

from flask import Flask, render_template, session, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """Root redirect to /users"""
    return redirect("/users")

@app.route("/users", methods=["POST", "GET"])
def list_users():
    """List of all users"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template("users.html", users=users)

@app.route("/users/new", methods=["GET", "POST"])
def add_user():
    """Add new user form"""
    if request.method == "POST":
        first_name = request.form["first_name"].strip().capitalize()
        last_name = request.form["last_name"].strip().capitalize()
        img_url = (request.form.get("img_url") or "").strip()

        new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(f"Error adding new user to session: {e}")
            db.session.rollback()

        return redirect("/users")
    elif request.method == "GET":
        return render_template("new-user-form.html")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    """User detail page"""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user page"""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form["first_name"].strip().capitalize()
        user.last_name = request.form["last_name"].strip().capitalize()
        user.img_url = (request.form.get("image_url") or "").strip()

        print(user)
        
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error updating user: {e}")
            db.session.rollback()

        return redirect("/users")

    elif request.method == "GET":
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        print(user.img_url)

        return render_template("user-edit-form.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST", "DELETE"])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

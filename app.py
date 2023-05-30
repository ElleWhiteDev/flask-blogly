"""Blogly application."""

from flask import Flask, render_template, session, request, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import *

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



@app.route("/")
def home_page():
    """Recent posts"""
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", recent_posts=recent_posts)


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
            flash("User Added", "success")
        except Exception as e:
            print(f"Error adding new user to session: {e}")
            db.session.rollback()
            flash("Unable to add user at this time", "error")

        return redirect("/users")
    elif request.method == "GET":
        return render_template("new-user-form.html")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """User detail page"""
    user = User.query.get(user_id)

    if user is not None:
        posts = user.posts
        return render_template("user-detail.html", user=user, posts=posts)
    else:
        flash("Invalid user", "error")
        return redirect("/")


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user page"""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form["first_name"].strip().capitalize()
        user.last_name = request.form["last_name"].strip().capitalize()
        user.img_url = (request.form.get("image_url") or "").strip()
        
        try:
            db.session.commit()
            flash("Edits Saved", "success")
        except Exception as e:
            print(f"Error updating user: {e}")
            db.session.rollback()
            flash("Unable to update user at this time","error")

        return redirect("/users")
    elif request.method == "GET":
        return render_template("edit-user-form.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST", "DELETE"])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    flash("User Deleted", "success")
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=["POST", "GET"])
def post_form(user_id):
    """New post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"]

        post = Post(title=title, content=content, user_id=user.id)

        try:
            db.session.add(post)
            db.session.commit()
            flash("Post Added", "success")
        except Exception as e:
            print(f"Error adding new post to session: {e}")
            db.session.rollback()
            flash("Unable to add post at this time", "error")

        return redirect(url_for('user_details', user_id=user.id))
    elif request.method == "GET":
        return render_template("new-post-form.html", user=user, tags=tags)
    

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """View individual post"""
    post = Post.query.get(post_id)

    if post:
        user = post.user
        user_id = post.user_id
        tags = post.tags
        return render_template("show-post.html", post=post, user=user, user_id=user_id, tags=tags)
    else:
        flash("Post unavailable", "error")
        return redirect("/")


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == "POST":
        post.title = request.form["title"].strip()
        post.content = request.form["content"]
        post.tags = [Tag.query.get(int(tag)) for tag in request.form.getlist("tags")]

        try:
            db.session.commit()
            flash("Edits Saved", "success")
        except Exception as e:
            print(f"Error updating post: {e}")
            db.session.rollback()
            flash("Unable to update post at this time", "error")

        return redirect(url_for('user_details', user_id=post.user.id))
    elif request.method == "GET":
        return render_template("edit-post-form.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete user"""
    post = Post.query.get(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    flash("Post Deleted", "success")
    return redirect(url_for("user_details", user_id=user_id))


@app.route("/tags")
def list_tags():
    """List all tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/new", methods=["GET", "POST"])
def add_tag():
    """Add new tag form"""
    if request.method == "POST":
        name = request.form["name"].strip().capitalize()

        new_tag = Tag(name=name)

        try:
            db.session.add(new_tag)
            db.session.commit()
            flash("Tag Added", "success")
        except Exception as e:
            print(f"Error adding new tag to session: {e}")
            db.session.rollback()
            flash("Unable to add tag at this time", "error")

        return redirect("/tags")
    elif request.method == "GET":
        return render_template("new-tag-form.html")
    

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Tag detail page"""
    tag = Tag.query.get_or_404(tag_id)

    if tag:
        return render_template("tag-detail.html", tag=tag)
    else:
        flash("Tag unavailable", "error")
        return redirect("/")


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def edit_tag(tag_id):
    """Edit tag page"""
    tag = Tag.query.get_or_404(tag_id)

    if request.method == "POST":
        tag.name = request.form["name"].strip().capitalize()
        
        try:
            db.session.commit()
            flash("Edits Saved", "success")
        except Exception as e:
            print(f"Error updating tag: {e}")
            db.session.rollback()
            flash("Unable to update tag at this time", "error")

        return redirect("/tags")
    elif request.method == "GET":
        return render_template("edit-tag-form.html", tag=tag)


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash("Tag Deleted", "success")
    return redirect("/tags") 
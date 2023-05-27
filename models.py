from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String, default="https://img.freepik.com/free-vector/illustration-user-avatar-icon_53876-5907.jpg")

    posts = db.relationship("Post", cascade="all, delete", backref=db.backref("user"))

    __table_args__ = (UniqueConstraint('first_name', 'last_name', name='unique_full_name'),)

    def __repr__(self):
        return f"<User {self.id} | {self.first_name} {self.last_name} |{self.img_url}>"


class Post(db.Model):
    """User post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Post {self.id} | {self.title} | {self.content} | {self.created_at} | {self.user_id}>"
    
    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y, %I:%M %p")

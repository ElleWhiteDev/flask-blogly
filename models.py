from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, default="https://img.freepik.com/free-vector/illustration-user-avatar-icon_53876-5907.jpg")

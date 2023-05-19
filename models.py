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
    first_name = (db.Text, nullable=False)
    last_name = (db.Text, nullable=False)
    img_url = (db.Text, default="https://play-lh.googleusercontent.com/W1Rz_g5pu2i07INW9uqiD-Tj30e_F8HppnuE41WFfXWlKXzPDCL6_B52sJ2sCONkrA=w240-h480-rw")

from app.extension import db
from flask_login import UserMixin

class USLI(db.Model, UserMixin):
    __tablename__ = "uslis"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String)
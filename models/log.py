from app.extension import db


class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.String, primary_key=True)
    owner = db.Column(db.String(256))
    privacy = db.Column(db.String)
    description = db.Column(db.String)
    is_success = db.Column(db.Boolean)
    created_date = db.Column(db.String)
    created_timestamp = db.Column(db.String)
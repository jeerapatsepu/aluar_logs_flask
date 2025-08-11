from app.extension import db

class Boardway(db.Model):
    __tablename__ = "boardways"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    path = db.Column(db.String)
    created_date = db.Column(db.String)
    created_timestamp = db.Column(db.String)
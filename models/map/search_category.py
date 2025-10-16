from app.shared import db

class MapSearchCategory(db.Model):
    __tablename__ = "map_search_categories"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String)
    title = db.Column(db.String)
    image_url = db.Column(db.String)
    slug = db.Column(db.String)
    created_date = db.Column(db.String)
    created_timestamp = db.Column(db.String)
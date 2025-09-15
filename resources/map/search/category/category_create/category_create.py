from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
from datetime import datetime, timezone
from app.extension import db, uid
from models.map.search_category import MapSearchCategory
from resources.map.search.category.category_create.category_create_request_schema import CategoryCreateDataResponseSchema, CategoryCreateRequestSchema, CategoryCreateResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema

blp = Blueprint("CategoryCreate", __name__, description="Category Create")

@blp.route("/map/category/create")
class CategoryCreate(MethodView):
    @jwt_required()
    @blp.arguments(CategoryCreateRequestSchema)
    @blp.response(200, CategoryCreateResponseSchema)
    def post(self, request):
        title = request["title"]
        image_url = request["image_url"]

        category = MapSearchCategory.query.filter_by(title=title).first()
        if category:
            return getCategoryCreateFailResponse(5000)
        else:
            time = datetime.now(timezone.utc)
            new_category = MapSearchCategory(title=title,
                                    image_url=image_url,
                                    created_date=str(time),
                                    created_timestamp=str(time.timestamp()))
            db.session.add(new_category)
            db.session.commit()
            return getCategoryCreateSuccessResponse(1000, new_category)

def getCategoryCreateSuccessResponse(response_code, boardway):
    time = datetime.now(timezone.utc)

    data = CategoryCreateDataResponseSchema()
    data.title = boardway.title
    data.image_url = boardway.image_url
    data.created_date = boardway.created_date
    data.created_timestamp = boardway.created_timestamp

    meta = MetaSchema()
    meta.response_id = uid.hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = None

    response = CategoryCreateResponseSchema()
    response.meta = meta
    response.data = data
    return response

def getCategoryCreateFailResponse(response_code):
    time = datetime.now(timezone.utc)

    error = ErrorSchema()
    error.title = "Service can not answer"
    error.message = "Category is not unique"

    meta = MetaSchema()
    meta.response_id = uid.hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error

    response = CategoryCreateResponseSchema()
    response.meta = meta
    response.data = None
    return response
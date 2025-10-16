from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
from datetime import datetime, timezone
from app.shared import db, uid
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
        category_id = request["category_id"]
        title = request["title"]
        image_url = request["image_url"]
        slug = request["slug"]

        category = MapSearchCategory.query.filter_by(title=title).first()
        if category:
            return self.getCategoryCreateFailResponse(5000)
        else:
            time = datetime.now(timezone.utc)
            new_category = MapSearchCategory(category_id=category_id,
                                             title=title,
                                             image_url=image_url,
                                             slug=slug,
                                             created_date=str(time),
                                             created_timestamp=str(time.timestamp()))
            db.session.add(new_category)
            db.session.commit()
            return self.getCategoryCreateSuccessResponse(1000, new_category)

    def getCategoryCreateSuccessResponse(self, response_code, category):
        time = datetime.now(timezone.utc)

        data = CategoryCreateDataResponseSchema()
        data.category_id = category.category_id
        data.title = category.title
        data.image_url = category.image_url
        data.slug = category.slug
        data.created_date = category.created_date
        data.created_timestamp = category.created_timestamp

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

    def getCategoryCreateFailResponse(self, response_code):
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
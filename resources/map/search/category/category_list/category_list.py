from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timezone

from sqlalchemy import Integer
from models import MapSearchCategory
from app.shared import uid
from resources.map.search.category.category_list.category_list_response import CategoryListResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema

blp = Blueprint("CategoryList", __name__, description="Category List")

@blp.route("/map/category/list")
class CategoryList(MethodView):
    @blp.response(200, CategoryListResponseSchema)
    def get(self):
        boardway_list = MapSearchCategory.query.all()
        boardway_list.sort(key=self.sortBoardwayList)
        
        return self.getCategoryListSuccessResponse(1000, boardway_list)

    def sortBoardwayList(self, e):
        return e.id
    
    def getCategoryListSuccessResponse(self, response_code: Integer, boardway_list):
        time = datetime.now(timezone.utc)

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = CategoryListResponseSchema()
        response.meta = meta
        response.data = boardway_list
        return response
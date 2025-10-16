from flask.views import MethodView
from flask_smorest import Blueprint
from models import MapSearchCategory
from resources.map.search.category.category_list.category_list_response import CategoryListResponseSchema
from resources.shared.shared_meta import get_meta_response

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

    def getCategoryListSuccessResponse(self, response_code: int, boardway_list):
        response = CategoryListResponseSchema()
        response.meta = get_meta_response(response_code)
        response.data = boardway_list
        return response
from flask_smorest import Api
from resources.auth.auth_create.auth_create import blp as AuthCreateBlueprint
from resources.auth.auth_login import blp as AuthLoginBlueprint
from resources.log.log_create import blp as LogCreateBlueprint
from resources.log.log_list import blp as LogListBlueprint
from resources.home.boardway.boardway_create.boardway_create import blp as BoardwayCreateBlueprint
from resources.home.boardway.boardway_list.boardway_list import blp as BoardwayListBlueprint
from resources.map.search.category.category_create.category_create import blp as CategoryCreateBlueprint
from resources.map.search.category.category_list.category_list import blp as CategoryListBlueprint
from resources.map.search.category.category_search.category_search import blp as CategorySearchBlueprint
# from resources.map.search.nearby.nearby_search.nearby_search import blp as NearBySearchBlueprint

def register_blueprint(app):
    api = Api(app)
    api.register_blueprint(AuthCreateBlueprint)
    api.register_blueprint(AuthLoginBlueprint)
    api.register_blueprint(LogCreateBlueprint)
    api.register_blueprint(LogListBlueprint)
    api.register_blueprint(BoardwayCreateBlueprint)
    api.register_blueprint(BoardwayListBlueprint)
    api.register_blueprint(CategoryCreateBlueprint)
    api.register_blueprint(CategoryListBlueprint)
    api.register_blueprint(CategorySearchBlueprint)
    # api.register_blueprint(NearBySearchBlueprint)
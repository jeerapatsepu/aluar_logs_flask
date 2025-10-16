from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
from datetime import datetime, timezone
from models import Boardway
from app.shared import db, uid
from resources.home.boardway.boardway_list.boardway_list_response import BoardwayListResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema

blp = Blueprint("BoardwayList", __name__, description="Boardway List")

@blp.route("/boardway/list")
class BoardwayList(MethodView):
    @blp.response(200, BoardwayListResponseSchema)
    def get(self):
        boardway_list = Boardway.query.all()
        return getBoardwayListSuccessResponse(1000, boardway_list)

def getBoardwayListSuccessResponse(response_code, boardway_list):
    time = datetime.now(timezone.utc)

    meta = MetaSchema()
    meta.response_id = uid.hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = None

    response = BoardwayListResponseSchema()
    response.meta = meta
    response.data = boardway_list
    return response
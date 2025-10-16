from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
from datetime import datetime, timezone
from models import Boardway
from app.shared import db, uid
from resources.home.boardway.boardway_create.boardway_create_request_schema import BoardwayCreateDataResponseSchema, BoardwayCreateRequestSchema, BoardwayCreateResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema

blp = Blueprint("BoardwayCreate", __name__, description="Boardway Create")

@blp.route("/boardway/create")
class BoardwayCreate(MethodView):
    @jwt_required()
    @blp.arguments(BoardwayCreateRequestSchema)
    @blp.response(200, BoardwayCreateResponseSchema)
    def post(self, request):
        title = request["title"]
        description = request["description"]
        image_url = request["image_url"]
        path = request["path"]

        boardway = Boardway.query.filter_by(title=title).first()
        if boardway:
            return self.getBoardwayCreateFailResponse(5000)
        else:
            time = datetime.now(timezone.utc)
            new_boardway = Boardway(title=title,
                                    description=description,
                                    image_url=image_url,
                                    path=path,
                                    created_date=str(time),
                                    created_timestamp=str(time.timestamp()))
            db.session.add(new_boardway)
            db.session.commit()
            return self.getBoardwayCreateSuccessResponse(1000, new_boardway)

    def getBoardwayCreateSuccessResponse(self, response_code, boardway):
        time = datetime.now(timezone.utc)

        data = BoardwayCreateDataResponseSchema()
        data.title = boardway.title
        data.description = boardway.description
        data.image_url = boardway.image_url
        data.path = boardway.path
        data.created_date = boardway.created_date
        data.created_timestamp = boardway.created_timestamp

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = None

        response = BoardwayCreateResponseSchema()
        response.meta = meta
        response.data = data
        return response

    def getBoardwayCreateFailResponse(self, response_code):
        time = datetime.now(timezone.utc)

        error = ErrorSchema()
        error.title = "Service can not answer"
        error.message = "Boardway is not unique"

        meta = MetaSchema()
        meta.response_id = uid.hex
        meta.response_code = response_code
        meta.response_date = str(time)
        meta.response_timestamp = str(time.timestamp())
        meta.error = error

        response = BoardwayCreateResponseSchema()
        response.meta = meta
        response.data = None
        return response
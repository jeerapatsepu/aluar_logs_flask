import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    get_jwt,
    jwt_required
)
from datetime import datetime, timezone
from uuid import uuid4
from models.log import Log
from schemas.log.log_create import LogCreateDataResponseSchema, LogCreateRequestSchema, LogCreateResponseSchema
from app.extension import db
from schemas.meta import MetaSchema
from shared import getError

blp = Blueprint("LogCreate", __name__, description="Log Create")

@blp.route("/log/create")
class LogCreate(MethodView):
    @jwt_required()
    @blp.arguments(LogCreateRequestSchema)
    @blp.response(200, LogCreateResponseSchema)
    def post(self, request):
        sub = get_jwt()["sub"]
        privacy = request["privacy"]
        description = request["description"]
        is_success = request["is_success"]
        time = datetime.now(timezone.utc)
        try:
            uid = uuid4().hex
            log = Log(id=uid,
                      owner=sub,
                      privacy=privacy,
                      description=description,
                      is_success=is_success,
                      created_date=str(time),
                      created_timestamp=str(time.timestamp()))
            db.session.add(log)
            db.session.commit()
            data = LogCreateDataResponseSchema()
            data.id = log.id
            data.owner = log.owner
            data.privacy = log.privacy
            data.description = log.description
            data.is_success = log.is_success
            data.created_date = log.created_date
            data.created_timestamp = log.created_timestamp
            return getResponse(time, 1000, data, error=None)
        except Exception as e:
            logging.exception("LogCreate")
            error = getError("Service can not answer", "Exeption has occured")
            return getResponse(time, 5000, None, error=error)

def getResponse(time, response_code, data, error):
    response = LogCreateResponseSchema()
    meta = MetaSchema()
    meta.response_id = uuid4().hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    response.meta = meta
    response.data = data
    return response
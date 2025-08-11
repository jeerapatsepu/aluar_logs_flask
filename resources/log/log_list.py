import logging
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    get_jwt,
    jwt_required
)
from datetime import datetime, timezone
from uuid import uuid4
from models.log import Log
from schemas.log.log_list import LogListRequestSchema, LogListResponseSchema
from app.extension import db
from schemas.meta import MetaSchema
from shared import getError

blp = Blueprint("LogList", __name__, description="Log List")

@blp.route("/log/list")
class LogList(MethodView):
    @jwt_required()
    @blp.arguments(LogListRequestSchema)
    @blp.response(200, LogListResponseSchema)
    def post(self, request):
        sub = get_jwt()["sub"]
        offset = request["offset"]
        limit = request["limit"]
        owner = request["owner"]
        logs = Log.query.filter_by(owner=owner)
        return getResponse(1000, logs[offset : offset + limit], error=None)

def getResponse(response_code, data, error):
    time = datetime.now(timezone.utc)
    response = LogListResponseSchema()
    meta = MetaSchema()
    meta.response_id = uuid4().hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    response.meta = meta
    response.data = data
    return response
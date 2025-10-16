
import os
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required
)
import requests
from flask import Flask, jsonify, request as dd
from datetime import datetime, timezone
from app.shared import db, uid
from models.map.search_category import MapSearchCategory
from resources.map.search.nearby.nearby_search.nearby_search_request_schema import NearBySearchRequestSchema, NearBySearchResponseSchema
from schemas.error import ErrorSchema
from schemas.meta import MetaSchema

blp = Blueprint("NearBySearch", __name__, description="NearBy Search")

@blp.route("/map/nearby/search")
class NearBySearch(MethodView):
    @blp.arguments(NearBySearchRequestSchema)
    @blp.response(200, NearBySearchResponseSchema)
    def post(self, request):
        lat = request["lat"]
        lon = request["lon"]
        offset = request["offset"]
        limit = request["limit"]
        language = request["language"]

        tom_tom_key = os.getenv("TOM_TOM_KEY")
        
        url = "https://api.tomtom.com/search/2/nearbySearch/" + ".json?key=" + str(tom_tom_key) + "&ofs=" + str(offset) + "&limit=" + str(limit) + "&language=" + str(language) + "&lat=" + str(lat) + "&lon=" + str(lon)
        ttt = requests.get(url)

        if ttt.status_code == 200:
            time = datetime.now(timezone.utc)
            meta = MetaSchema()
            meta.response_id = uid.hex
            meta.response_code = 1000
            meta.response_date = str(time)
            meta.response_timestamp = str(time.timestamp())
            meta.error = None
            response = NearBySearchResponseSchema()
            response.meta = meta
            response.data = ttt.json()
            return response

# def getCategoryCreateSuccessResponse(response_code, boardway):
#     time = datetime.now(timezone.utc)

#     data = CategorySearchDataResponseSchema()
#     data.title = boardway.title
#     data.image_url = boardway.image_url
#     data.created_date = boardway.created_date
#     data.created_timestamp = boardway.created_timestamp

#     meta = MetaSchema()
#     meta.response_id = uid.hex
#     meta.response_code = response_code
#     meta.response_date = str(time)
#     meta.response_timestamp = str(time.timestamp())
#     meta.error = None

#     response = CategorySearchResponseSchema()
#     response.meta = meta
#     response.data = data
#     return response

# def getCategoryCreateFailResponse(response_code):
#     time = datetime.now(timezone.utc)

#     error = ErrorSchema()
#     error.title = "Service can not answer"
#     error.message = "Category is not unique"

#     meta = MetaSchema()
#     meta.response_id = uid.hex
#     meta.response_code = response_code
#     meta.response_date = str(time)
#     meta.response_timestamp = str(time.timestamp())
#     meta.error = error

#     response = CategoryCreateResponseSchema()
#     response.meta = meta
#     response.data = None
#     return response
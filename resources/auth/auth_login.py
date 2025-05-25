import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone
from models.usli import USLI
from schemas.auth.auth_create import AuthCreateRequestSchema, AuthLoginDataResponseSchema, AuthLoginResponseSchema
from uuid import uuid4
from shared import db
from schemas.meta import MetaSchema
from shared import getError

blp = Blueprint("AuthLogin", __name__, description="Auth Login")

@blp.route("/auth/login")
class AuthLogin(MethodView):
    @blp.arguments(AuthCreateRequestSchema)
    @blp.response(200, AuthLoginResponseSchema)
    def post(self, request):
        email = request["email"]
        password = request["password"]
        usli = USLI.query.filter_by(email=email).first()
        bcrypt = Bcrypt()
        if usli and bcrypt.check_password_hash(pw_hash=usli.password, password=password):
            access_token = create_access_token(identity=str(usli.uid), fresh=True)
            refresh_token = create_refresh_token(identity=str(usli.uid))
            data = AuthLoginDataResponseSchema()
            data.access_token = access_token
            data.refresh_token = refresh_token
            data.uid = usli.uid
            return getResponse(1000, data, error=None)
        else:
            logging.exception("AuthLogin")
            error = getError("Service can not answer", "Can not authen the user")
            return getResponse(5000, None, error=error)

def getResponse(response_code, data, error):
    time = datetime.now(timezone.utc)
    response = AuthLoginResponseSchema()
    meta = MetaSchema()
    meta.response_id = uuid4().hex
    meta.response_code = response_code
    meta.response_date = str(time)
    meta.response_timestamp = str(time.timestamp())
    meta.error = error
    response.meta = meta
    response.data = data
    return response
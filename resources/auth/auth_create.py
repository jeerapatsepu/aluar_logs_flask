import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone
from models import USLI
from schemas.auth.auth_create import AuthCreateRequestSchema, AuthLoginDataResponseSchema, AuthLoginResponseSchema
from uuid import uuid4
from shared import db
from schemas.meta import MetaSchema
from shared import getError

blp = Blueprint("AuthCreate", __name__, description="Auth Create")

@blp.route("/auth/create")
class AuthCreate(MethodView):
    @blp.arguments(AuthCreateRequestSchema)
    @blp.response(200, AuthLoginResponseSchema)
    def post(self, request):
        email = request["email"]
        password = request["password"]
        usli = USLI.query.filter_by(email=email).first()
        if usli:
            logging.exception("AuthCreate")
            error = getError("Service can not answer", "Email has duplicated")
            return getResponse(5000, None, error=error)
        try:
            bcrypt = Bcrypt()
            uid = uuid4().hex
            new_user = USLI(uid=uid,
                            email=email,
                            password=bcrypt.generate_password_hash(password).decode('utf-8'))
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=str(uid), fresh=True)
            refresh_token = create_refresh_token(identity=str(uid))
            data = AuthLoginDataResponseSchema()
            data.access_token = access_token
            data.refresh_token = refresh_token
            data.uid = uid
            return getResponse(1000, data, error=None)
        except Exception as e:
            logging.exception("AuthCreate")
            error = getError("Service can not answer", "Exeption has occured")
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
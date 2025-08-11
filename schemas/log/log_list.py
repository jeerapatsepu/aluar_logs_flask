from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow_enum import EnumField
from schemas.log.log_create import LogCreateDataResponseSchema, LogPrivacyType
from schemas.meta import MetaSchema

class LogListRequestSchema(Schema):
    offset = fields.Int()
    limit = fields.Int()
    owner = fields.Str()

class LogListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(LogCreateDataResponseSchema, dump_only=True, many=True)
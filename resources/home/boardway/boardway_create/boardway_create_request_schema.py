from marshmallow import Schema, ValidationError, fields, validates_schema
from schemas.meta import MetaSchema

class BoardwayCreateRequestSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    image_url = fields.Str(required=True)
    path = fields.Str(required=False)

class BoardwayCreateDataResponseSchema(Schema):
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=False)
    image_url = fields.Str(dump_only=True)
    path = fields.Str(dump_only=False)
    created_date = fields.Str(dump_only=False)
    created_timestamp = fields.Str(dump_only=False)

class BoardwayCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema(), dump_only=True)
    data = fields.Nested(BoardwayCreateDataResponseSchema(), dump_only=True)
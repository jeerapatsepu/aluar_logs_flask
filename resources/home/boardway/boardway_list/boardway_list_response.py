from marshmallow import Schema, fields
from schemas.meta import MetaSchema

class BoardwayListDataResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)
    description = fields.String(dump_only=True)
    image_url = fields.String(dump_only=True)
    path = fields.String(dump_only=True)
    created_date = fields.String(dump_only=True)
    created_timestamp = fields.String(dump_only=True)

class BoardwayListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(BoardwayListDataResponseSchema, dump_only=True, many=True)
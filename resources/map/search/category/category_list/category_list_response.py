from marshmallow import Schema, fields
from schemas.meta import MetaSchema

class CategoryListDataResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)
    image_url = fields.String(dump_only=True)
    created_date = fields.String(dump_only=True)
    created_timestamp = fields.String(dump_only=True)

class CategoryListResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(CategoryListDataResponseSchema, dump_only=True, many=True)
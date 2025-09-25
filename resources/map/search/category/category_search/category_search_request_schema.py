from marshmallow import Schema, ValidationError, fields, validates_schema
from schemas.meta import MetaSchema

class CategorySearchRequestSchema(Schema):
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    category = fields.Str(required=True)

class CategorySearchDataResponseSchema(Schema):
    title = fields.Str(dump_only=True)
    image_url = fields.Str(dump_only=True)
    created_date = fields.Str(dump_only=False)
    created_timestamp = fields.Str(dump_only=False)

class CategorySearchResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(CategorySearchDataResponseSchema, dump_only=True)
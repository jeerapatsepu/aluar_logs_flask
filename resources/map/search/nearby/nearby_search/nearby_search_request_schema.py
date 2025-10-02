from typing import Any
from marshmallow import Schema, ValidationError, fields, validates_schema
from schemas.meta import MetaSchema

class NearBySearchRequestSchema(Schema):
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    language = fields.Str(required=True)

# class CategorySearchDataResponseSchema(Schema):
#     title = fields.Str(dump_only=True)
#     image_url = fields.Str(dump_only=True)
#     slug = fields.Str(dump_only=True)
#     created_date = fields.Str(dump_only=False)
#     created_timestamp = fields.Str(dump_only=False)

class NearBySearchResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Raw()
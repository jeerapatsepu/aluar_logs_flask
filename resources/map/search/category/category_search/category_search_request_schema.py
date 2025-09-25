from typing import Any
from marshmallow import Schema, ValidationError, fields, validates_schema
from schemas.meta import MetaSchema

class CategorySearchRequestSchema(Schema):
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    category = fields.Str(required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    language = fields.Str(required=True)

class CategorySearchResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Dict()
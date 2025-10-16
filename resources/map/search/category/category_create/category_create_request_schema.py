from marshmallow import Schema, fields
from schemas.meta import MetaSchema

class CategoryCreateRequestSchema(Schema):
    title = fields.Str(required=True)
    image_url = fields.Str(required=True)
    slug = fields.Str(required=True)
    category_id = fields.Str(required=True)

class CategoryCreateDataResponseSchema(Schema):
    category_id = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    image_url = fields.Str(dump_only=True)
    slug = fields.Str(dump_only=True)
    created_date = fields.Str(dump_only=False)
    created_timestamp = fields.Str(dump_only=False)

class CategoryCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema, dump_only=True)
    data = fields.Nested(CategoryCreateDataResponseSchema, dump_only=True)
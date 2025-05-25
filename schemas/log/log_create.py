from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow_enum import EnumField
from schemas.meta import MetaSchema

class LogPrivacyType(EnumField):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

class LogCreateRequestSchema(Schema):
    privacy = EnumField(LogPrivacyType, required=True)
    description = fields.Str(required=True)
    is_success = fields.Bool(required=True)

    @validates_schema
    def validate_description(self, data, **kwargs):
        lenght = len(data["description"])
        if lenght > 500:
            raise ValidationError("Description must be less than 500 characters", "description")
        elif lenght <= 0:
            raise ValidationError("Description must be more than 0 characters", "description")

class LogCreateDataResponseSchema(Schema):
    id = fields.Str(dump_only=True)
    owner = fields.Str(dump_only=True)
    privacy = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    is_success = fields.Bool(dump_only=True)
    created_date = fields.Str(dump_only=True)
    created_timestamp = fields.Str(dump_only=True)

class LogCreateResponseSchema(Schema):
    meta = fields.Nested(MetaSchema(), dump_only=True)
    data = fields.Nested(LogCreateDataResponseSchema(), dump_only=True)
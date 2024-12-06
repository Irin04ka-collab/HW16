import typing

from marshmallow import Schema, fields, types, ValidationError
from sqlalchemy.orm import validates


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    age = fields.Int(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)
    phone = fields.Str(required=True)

    @validates('age')
    def validate_age(self, value):
        if value <= 0:
            raise ValidationError("Возраст должен быть больше 0")

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    start_date = fields.Date(format="%m/%d/%Y", required=True)
    end_date = fields.Date(format="%m/%d/%Y", required=True)
    address = fields.Str(required=True)
    price = fields.Float(required=True)
    customer_id = fields.Int(required=True)
    executor_id = fields.Int(required=True)

class OfferSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    executor_id = fields.Int(required=True)

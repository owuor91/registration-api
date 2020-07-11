from marshmallow import fields, Schema


class StudentSchema(Schema):
    """
    Student schema
    """
    student_id = fields.UUID(dump_only=True)
    first_name = fields.String(required=True, error_messages={"required": "first name is required"})
    last_name = fields.String(required=True, error_messages={"required": "last name is required"})
    email = fields.String(required=True, error_messages={"required": "email is required"})
    phone_number = fields.String(required=True, error_messages={"required": "phone number is required"})
    date_of_birth = fields.Date(required=True, error_messages={"required": "date of birth is required"})
    sex = fields.String(required=True, error_messages={"required": "sex is required"})

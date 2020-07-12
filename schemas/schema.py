from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length

from models.models import StudentModel, CourseModel, StudentCourseModel


class StudentSchema(Schema):
    """
    Student schema
    """
    student_id = fields.UUID(dump_only=True)
    first_name = fields.String(required=True, validate=Length(min=3),
                               error_messages={"required": "first name is required"})
    last_name = fields.String(required=True, validate=Length(min=3),
                              error_messages={"required": "last name is required"})
    email = fields.Email(required=True, error_messages={"required": "email is required"})
    phone_number = fields.String(required=True, validate=Length(min=10),
                                 error_messages={"required": "phone number is required"})
    date_of_birth = fields.Date(required=True, error_messages={"required": "date of birth is required"})
    sex = fields.String(required=True, error_messages={"required": "sex is required"})
    image_url = fields.String(allow_none=True)
    password = fields.String(required=True, error_messages={"required": "password is required"})

    @post_load
    def deserialize_student(self, data, **kwargs):
        return StudentModel(**data)


class CourseSchema(Schema):
    """
    Course Schema
    """

    course_id = fields.UUID(dump_only=True)
    course_name = fields.String(required=True, allow_blank=False,
                                error_messages={"required": "course name is required"})
    course_code = fields.String(required=True, error_messages={"required": "course code is required"})
    description = fields.String(required=True, error_messages={"required": "description is required"})
    instructor = fields.String(required=True, error_messages={"required": "instructor is required"})

    @post_load
    def deserialize_course(self, data, **kwargs):
        return CourseModel(**data)


class StudentCourseSchema(Schema):
    """
    Student Course Schema
    """
    student_id = fields.UUID(required=True, error_messages={"required": "student id is required"})
    course_id = fields.UUID(required=True, error_messages={"required": "course id is required"})

    @post_load
    def deserialize_student_course(self, data, **kwargs):
        return StudentCourseModel(**data)

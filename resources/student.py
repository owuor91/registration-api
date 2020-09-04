import datetime

import boto3
from flask import request
from flask_jwt_extended import (create_access_token, jwt_required)
from flask_restful import Resource
from werkzeug.utils import secure_filename

from config import Config
from models.models import StudentModel
from schemas.schema import StudentSchema
from utils.util import get_value


class Student(Resource):

    @jwt_required
    def get(self, student_id=None):
        student = students = None
        if student_id:
            student = StudentModel.find_student_by_id(student_id)
        else:
            students = StudentModel.return_all()

        student_schema = StudentSchema(exclude=['password', 'sex', 'date_of_birth'])
        if student:
            return {'student': student_schema.dump(student)}
        elif students:
            return {'students': [student_schema.dump(s) for s in students]}
        return {'message': 'student not found'}, 404

    @jwt_required
    def put(self, student_id):
        student = StudentModel.find_student_by_id(student_id)

        if not student:
            return {'error': 'Student with id {} not found'.format(student_id)}

        if get_value('first_name'):
            student.first_name = get_value('first_name')

        if get_value('last_name'):
            student.last_name = get_value('last_name')

        if get_value('email'):
            student.email = get_value('email')

        if get_value('phone_number'):
            if not student.find_student_by_phone_number(get_value('phone_number')):
                student.phone_number = get_value('phone_number')
            else:
                return {'message': 'a student with the number {} already exists'.format(
                    get_value('phone_number'))}, 400

        student.save_to_db()
        student_schema = StudentSchema()
        return {'message': 'student updated successfully',
                'student': student_schema.dump(student)}

    @jwt_required
    def delete(self, student_id):
        student = StudentModel.find_student_by_id(student_id)
        if student:
            student.active = False
            student.save_to_db()
            return {'message': 'student deleted successfully'}, 204
        else:
            return {'message': 'student with id {} doesn\'t exist'.format(student_id)}


class StudentLogin(Resource):
    def post(self):
        try:
            student = StudentModel.find_student_by_email(get_value('email'))
            if student and student.password_is_valid(get_value('password')):
                access_token = create_access_token(student.student_id, expires_delta=datetime.timedelta(seconds=86400))
                if access_token:
                    response = {
                        'message': 'login successful',
                        'access_token': access_token,
                        'student_id': str(student.student_id)
                    }
                    return response, 200
            else:
                return {"error": "invalid credentials"}, 401
        except Exception as e:
            return {'error': str(e)}, 500


class StudentRegistration(Resource):
    def post(self, image=None, sex=None, date_of_birth=None):
        data = request.form.to_dict(flat=True)
        student_schema = StudentSchema()
        errors = student_schema.validate(data)
        if errors:
            return {'error': True, 'errors': str(errors)}, 400

        data["image_url"] = ""
        if sex is None:
            data["sex"] = ""

        if date_of_birth is None:
            data["date_of_birth"] = datetime.date.today().strftime("%m-%d-%Y")

        new_student = student_schema.load(data)

        request_phone_number = new_student.phone_number

        if StudentModel.find_student_by_phone_number(request_phone_number):
            return {'message': 'a student with the number {} already exists'.format(request_phone_number)}, 400
        else:
            image_file = request.files.get('image')
            if image_file:
                try:
                    image_url = self.upload_image_to_s3(image_file)
                    new_student.image_url = image_url
                except Exception as e:
                    return {'error': True, 'errors': e.args}, 400

            try:
                new_student.save_to_db()
                saved_student = StudentModel.find_student_by_phone_number(request_phone_number)
                student_schema = StudentSchema(exclude=['password', 'sex', 'date_of_birth'])
                return {'message': 'student registration, successful',
                        'student': student_schema.dump(saved_student)}, 201
            except Exception as e:
                return {'error': e.args}, 500

    def upload_image_to_s3(self, image_file):
        img_file_name = secure_filename(image_file.filename)

        image_errors = dict()

        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        if '.' not in img_file_name or img_file_name.split('.')[1].lower() not in allowed_extensions:
            image_errors['message'] = 'image file format is not supported'
            raise Exception(image_errors)

        s3 = boto3.client("s3", aws_access_key_id=Config.S3_ACCESS_KEY,
                          aws_secret_access_key=Config.S3_SECRET_ACCESS_KEY)
        try:
            file_path = '{}{}'.format('pictures/', img_file_name)
            s3.upload_fileobj(image_file, Config.S3_BUCKET_NAME, file_path)
            return '{}{}'.format(Config.S3_BASE_URL, img_file_name)
        except Exception as e:
            image_errors['message'] = str(e.args)
            raise Exception(image_errors)

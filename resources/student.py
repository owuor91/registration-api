import datetime

import boto3
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from config import Config
from models.student_model import StudentModel
from utils.util import get_value


class Student(Resource):
    def post(self, image=None):
        errors = self.validate_post_student()
        if (len(errors) != 0):
            return {'error': True, 'errors': errors}, 400
        request_phone_number = get_value('phone_number')

        if StudentModel.find_student_by_phone_number(request_phone_number):
            return {'message': 'a student with the number {} already exists'.format(request_phone_number)}, 400
        else:
            image_file = request.files.get('image')
            image_url = ""
            if image_file:
                try:
                    image_url = self.upload_image_to_s3(image_file)
                except Exception as e:
                    return {'error': True, 'errors': e.args}, 400

            new_student = StudentModel(first_name=get_value('first_name'),
                                       last_name=get_value('last_name'),
                                       email=get_value('email'),
                                       phone_number=get_value('phone_number'),
                                       date_of_birth=datetime.datetime.strptime(get_value('date_of_birth'),
                                                                                '%Y-%m-%d'),
                                       sex=get_value('sex'),
                                       image_url=image_url)
            try:
                new_student.save_to_db()
                saved_student = StudentModel.find_student_by_phone_number(request_phone_number)
                return {'message': 'student registration, successful',
                        'student': saved_student.to_json()}, 201
            except Exception as e:
                return {'error': e.message}, 500

    def validate_post_student(self):
        errors = dict()
        if not get_value('first_name'):
            errors['first_name'] = 'First name is required'

        if not get_value('last_name'):
            errors['last_name'] = 'Last name is required'

        if not get_value('date_of_birth'):
            errors['date_of_birth'] = 'date_of_birth is required'

        if not get_value('email'):
            errors['email'] = 'email is required'

        if not get_value('phone_number'):
            errors['phone_number'] = 'phone_number is required'

        if not get_value('sex'):
            errors['sex'] = 'sex is required'

        return errors

    def get(self, student_id=None):
        student = students = None
        if student_id:
            student = StudentModel.find_student_by_id(student_id)
        else:
            students = StudentModel.return_all()

        if student:
            return {'student': student.to_json()}
        elif students:
            return {'students': [s.to_json() for s in students]}
        return {'message': 'student not found'}, 404

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
        return {'message': 'student updated successfully',
                'student': student.to_json()}

    def delete(self, student_id):
        student = StudentModel.find_student_by_id(student_id)
        if student:
            student.active = False
            student.save_to_db()
            return {'message': 'student deleted successfully'}, 204
        else:
            return {'message': 'student with id {} doesn\'t exist'.format(student_id)}

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

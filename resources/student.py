import datetime

from flask import request
from flask_restful import Resource

from models.student_model import StudentModel


class Student(Resource):
    def post(self):
        request_phone_number = self.get_value('phone_number')

        if StudentModel.find_student_by_phone_number(request_phone_number):
            return {'message': 'a student with the number {} already exists'.format(request_phone_number)}, 400
        else:
            new_student = StudentModel(first_name=self.get_value('first_name'),
                                       last_name=self.get_value('last_name'),
                                       email=self.get_value('email'),
                                       phone_number=self.get_value('phone_number'),
                                       date_of_birth=datetime.datetime.strptime(self.get_value('date_of_birth'),
                                                                                '%Y-%m-%d'),
                                       sex=self.get_value('sex'))
            new_student.save_to_db()
            return {'message': 'student registration, successful'}, 201

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

    def get_value(self, string):
        return request.form.get(string)

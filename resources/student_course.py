from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.models import CourseModel, StudentCourseModel, StudentModel
from schemas.schema import StudentCourseSchema, CourseSchema, StudentSchema
from utils.util import get_value


class StudentCourse(Resource):
    @jwt_required
    def post(self):
        data = request.form.to_dict(flat=True)
        student_course_schema = StudentCourseSchema()
        errors = student_course_schema.validate(data)
        if errors:
            return {'error': True, 'errors': str(errors)}, 400

        new_student_id = get_value('student_id')
        new_course_id = get_value('course_id')

        new_student_course = student_course_schema.load(data)
        try:
            new_student_course.save_to_db()
            saved_student_course = StudentCourseModel.find_record(new_student_id, new_course_id)
            return {'message': 'success',
                    'registration': student_course_schema.dump(saved_student_course)}, 201
        except Exception as e:
            return {'error': e.args}, 500

    @jwt_required
    def get(self, student_id=None, course_id=None):
        course_schema = CourseSchema()
        student_schema = StudentSchema()
        student_course_ids = StudentCourseModel.find_student_courses(student_id, course_id)
        if student_id:
            student_courses = []
            for course_id in student_course_ids:
                student_courses.append(CourseModel.find_course_by_id(course_id.course_id))

            return {'student_courses': [course_schema.dump(x) for x in student_courses]}

        if course_id:
            course_students = []
            for x in student_course_ids:
                course_students.append(StudentModel.find_student_by_id(x.student_id))

            return {'course_students': [student_schema.dump(y) for y in course_students]}

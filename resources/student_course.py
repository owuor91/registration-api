from flask_restful import Resource

from models.models import CourseModel, StudentCourseModel, StudentModel
from utils.util import get_value


class StudentCourse(Resource):
    def post(self):
        errors = self.validate()
        if (len(errors) != 0):
            return {'error': True, 'errors': errors}, 400

        new_student_id = get_value('student_id')
        new_course_id = get_value('course_id')

        new_student_course = StudentCourseModel(student_id=new_student_id, course_id=new_course_id)
        try:
            new_student_course.save_to_db()
            saved_student_course = StudentCourseModel.find_record(new_student_id, new_course_id)
            return {'message': 'success',
                    'reegistration': saved_student_course.to_json()}, 201
        except Exception as e:
            return {'error': e.message}, 500

    def validate(self):
        errors = dict()
        if not get_value('student_id'):
            errors['student_id'] = 'student_id is required'

        if not get_value('course_id'):
            errors['course_id'] = 'course_id is required'
        return errors

    def get(self, student_id=None, course_id=None):
        student_course_ids = StudentCourseModel.find_student_courses(student_id, course_id)
        if student_id:
            student_courses = []
            for course_id in student_course_ids:
                student_courses.append(CourseModel.find_course_by_id(course_id.course_id))

            return {'student_courses': [x.to_json() for x in student_courses]}

        if course_id:
            course_students = []
            for x in student_course_ids:
                course_students.append(StudentModel.find_student_by_id(x.student_id))

            return {'course_students': [y.to_json() for y in course_students]}

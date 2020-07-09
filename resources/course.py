from flask_restful import Resource

from models.models import CourseModel
from utils.util import get_value


class Course(Resource):
    def validate_post_course(self):
        errors = dict()
        if not get_value('course_name'):
            errors['course_name'] = 'course_name is required'
        if not get_value('course_code'):
            errors['course_code'] = 'course_code is required'
        if not get_value('description'):
            errors['description'] = 'description is required'
        if not get_value('instructor'):
            errors['instructor'] = 'instructor is required'

        return errors

    def post(self):
        errors = self.validate_post_course()
        if (len(errors) != 0):
            return {'error': True, 'errors': errors}, 400

        if CourseModel.find_course_by_code(get_value('course_code')):
            return {'message': 'a course with the code {} already exists'.format(get_value('course_code'))}, 400
        else:
            new_course = CourseModel(course_name=get_value('course_name'), course_code=get_value('course_code'),
                                     description=get_value('description'), instructor=get_value('instructor'))
            try:
                new_course.save_to_db()
                saved_course = CourseModel.find_course_by_code(get_value('course_code'))
                return {'message': 'course added successfully',
                        'course': saved_course.to_json()}, 201
            except Exception as e:
                return {'error': e.args}, 500

    def get(self, course_id=None):
        course = courses = None
        if course_id:
            course = CourseModel.find_course_by_id(course_id)
        else:
            courses = CourseModel.find_all()

        if course:
            return {'course': course.to_json()}
        elif courses:
            return {'courses': [c.to_json() for c in courses]}
        return {'message': 'course not found'}, 404

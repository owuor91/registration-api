from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.models import CourseModel
from schemas.schema import CourseSchema
from utils.util import get_value


class Course(Resource):
    @jwt_required
    def post(self):
        data = request.form.to_dict(flat=True)
        course_schema = CourseSchema()
        errors = course_schema.validate(data)
        if errors:
            return {'error': True, 'errors': str(errors)}, 400

        new_course = course_schema.load(data)

        if CourseModel.find_course_by_code(new_course.course_code):
            return {'message': 'a course with the code {} already exists'.format(get_value('course_code'))}, 400
        else:
            try:
                new_course.save_to_db()
                saved_course = CourseModel.find_course_by_code(new_course.course_code)
                return {'message': 'course added successfully',
                        'course': course_schema.dump(saved_course)}, 201
            except Exception as e:
                return {'error': e.args}, 500

    @jwt_required
    def get(self, course_id=None):
        course = courses = None
        if course_id:
            course = CourseModel.find_course_by_id(course_id)
        else:
            courses = CourseModel.find_all()

        course_schema = CourseSchema()
        if course:
            return {'course': course_schema.dump(course)}
        elif courses:
            return {'courses': [course_schema.dump(c) for c in courses]}
        return {'message': 'course not found'}, 404

from flask import Flask
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import DevelopmentConfig
from db import db
from gql import schema
from resources.course import Course
from resources.student import Student, StudentLogin
from resources.student_course import StudentCourse


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'reallynicee38y72piebird'
    jwt = JWTManager(app)

    api = Api(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api.add_resource(Student, '/students', '/students/<uuid:student_id>')
    api.add_resource(Course, '/courses', '/courses/<uuid:course_id>')
    api.add_resource(StudentCourse, '/register-course', '/students/<uuid:student_id>/courses',
                     '/courses/<uuid:course_id>/students')
    api.add_resource(StudentLogin, '/login')

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True,
                                                               get_context=lambda: {'session': db.session}))
    return app


if __name__ == '__main__':
    create_app(DevelopmentConfig).run(port=5000, debug=True)

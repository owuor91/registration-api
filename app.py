import sentry_sdk
from flask import Flask
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sentry_sdk.integrations.flask import FlaskIntegration

from config import DevelopmentConfig
from db import db
from gql import schema
from resources.course import Course
from resources.student import Student, StudentLogin, StudentRegistration
from resources.student_course import StudentCourse


def create_app(config):
    sentry_sdk.init(
        dsn=config.SENTRY_DSN_KEY,
        integrations=[FlaskIntegration()]
    )
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'reallynicee38y72piebird'
    app.config['PROPAGATE_EXCEPTIONS'] = True
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
    api.add_resource(StudentRegistration, '/register')

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True,
                                                               get_context=lambda: {'session': db.session}))

    return app


if __name__ == '__main__':
    create_app(DevelopmentConfig).run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask
from flask_restful import Api

from config import DevelopmentConfig
from db import db
from resources.course import Course
from resources.student import Student


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api = Api(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api.add_resource(Student, '/students', '/students/<uuid:student_id>')
    api.add_resource(Course, '/courses', '/courses/<uuid:course_id>')
    return app

if __name__ == '__main__':
    create_app(DevelopmentConfig).run(port=5000, debug=True)

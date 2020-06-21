from flask import Flask
from flask_restful import Api

from config import DevelopmentConfig
from db import db
from resources.course import Course
from resources.student import Student

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Student, '/students', '/students/<int:student_id>')
api.add_resource(Course, '/courses', '/courses/<uuid:course_id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

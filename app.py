import graphene
from flask import Flask
from flask_graphql import GraphQLView
from flask_restful import Api
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from config import DevelopmentConfig
from db import db
from models.models import StudentModel, CourseModel
from resources.course import Course
from resources.student import Student
from resources.student_course import StudentCourse


class StudentObject(SQLAlchemyObjectType):
    class Meta:
        model = StudentModel
        interfaces = (graphene.relay.Node,)


class CourseObject(SQLAlchemyObjectType):
    class Meta:
        model = CourseModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    students = SQLAlchemyConnectionField(StudentObject)
    courses = SQLAlchemyConnectionField(CourseObject)


schema = graphene.Schema(query=Query, auto_camelcase=False)


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
    api.add_resource(StudentCourse, '/register-course', '/students/<uuid:student_id>/courses',
                     '/courses/<uuid:course_id>/students')

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True,
                                                               get_context=lambda: {'session': db.session}))
    return app


if __name__ == '__main__':
    create_app(DevelopmentConfig).run(port=5000, debug=True)

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models.models import StudentModel, CourseModel


class StudentGQL(SQLAlchemyObjectType):
    class Meta:
        model = StudentModel
        interfaces = (graphene.relay.Node,)


class CourseGQL(SQLAlchemyObjectType):
    class Meta:
        model = CourseModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    students = SQLAlchemyConnectionField(StudentGQL)
    courses = SQLAlchemyConnectionField(CourseGQL)


schema = graphene.Schema(query=Query, auto_camelcase=False)

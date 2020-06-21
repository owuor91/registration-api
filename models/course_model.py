import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from db import db

Base = declarative_base()


class CourseModel(Base):
    __tablename__ = 'courses'
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(256))
    instructor = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, code, description, instructor):
        self.name = name
        self.code = code
        self.description = description
        self.instructor = instructor

    @classmethod
    def find_course_by_id(cls, course_id):
        return db.session.query(CourseModel).filter(CourseModel.id == course_id).filter(
            CourseModel.active == True).first()

    @classmethod
    def find_course_by_code(cls, course_code):
        return db.session.query(CourseModel).filter(CourseModel.code == course_code).filter(
            CourseModel.active == True).first()

    @classmethod
    def find_all(cls):
        return db.session.query(CourseModel).filter(CourseModel.active == True).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'instructor': self.instructor
        }

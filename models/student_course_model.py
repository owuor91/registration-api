import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from db import db
from models.course_model import CourseModel
from models.student_model import StudentModel

Base = declarative_base()


class StudentCourseModel(Base):
    __tablename__ = 'student_courses'
    student_course_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey(StudentModel.student_id))
    course_id = Column(UUID(as_uuid=True), ForeignKey(CourseModel.course_id))
    student = relationship(StudentModel, backref=backref('student_courses', cascade='all, delete-orphan'))
    course = relationship(CourseModel, backref=backref('student_courses', cascade='all, delete-orphan'))

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'student_course_id': str(self.student_course_id),
            'student_id': str(self.student_id),
            'course_id': str(self.course_id)
        }

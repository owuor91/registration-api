import uuid
from datetime import datetime, timedelta

import jwt
from flask import current_app
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db import db

Base = declarative_base()


class StudentModel(Base):
    __tablename__ = 'students'

    student_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(256))
    password = db.Column(db.String(256), nullable=False)
    courses = relationship('CourseModel', secondary='student_courses', back_populates='students')

    def __init__(self, first_name, last_name, email, phone_number, date_of_birth, sex, image_url, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.image_url = image_url
        self.password = Bcrypt().generate_password_hash(password).decode()

    @classmethod
    def find_student_by_id(cls, student_id):
        return db.session.query(StudentModel).filter(StudentModel.student_id == student_id).filter(
            StudentModel.active == True).first()

    @classmethod
    def return_all(cls):
        return db.session.query(StudentModel).filter(StudentModel.active == True).all()

    @classmethod
    def find_student_by_phone_number(cls, _phone_number):
        return db.session.query(StudentModel).filter(StudentModel.phone_number == _phone_number).first()

    @classmethod
    def find_student_by_email(cls, email):
        return db.session.query(StudentModel).filter(StudentModel.email == email).first()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, student_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': str(student_id)
            }
            return jwt.encode(payload=payload, key=current_app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Token expired, sign in again"
        except jwt.InvalidTokenError:
            return "Invalid token, register or login"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class CourseModel(Base):
    __tablename__ = 'courses'
    course_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_code = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(256))
    instructor = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)
    students = relationship('StudentModel', secondary='student_courses', back_populates='courses')

    def __init__(self, course_name, course_code, description, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.description = description
        self.instructor = instructor

    @classmethod
    def find_course_by_id(cls, course_id):
        return db.session.query(CourseModel).filter(CourseModel.course_id == course_id).filter(
            CourseModel.active == True).first()

    @classmethod
    def find_course_by_code(cls, course_code):
        return db.session.query(CourseModel).filter(CourseModel.course_code == course_code).filter(
            CourseModel.active == True).first()

    @classmethod
    def find_all(cls):
        return db.session.query(CourseModel).filter(CourseModel.active == True).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class StudentCourseModel(Base):
    __tablename__ = 'student_courses'
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('students.student_id'), primary_key=True)
    course_id = db.Column(UUID(as_uuid=True), db.ForeignKey('courses.course_id'), primary_key=True)

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_student_courses(cls, student_id=None, course_id=None):
        return db.session.query(StudentCourseModel).filter(
            or_(StudentCourseModel.student_id == student_id, StudentCourseModel.course_id == course_id)).all()

    @classmethod
    def find_record(cls, student_id, course_id):
        return db.session.query(StudentCourseModel).filter(StudentCourseModel.student_id == student_id).filter(
            StudentCourseModel.course_id == course_id).filter(
            CourseModel.active == True).first()

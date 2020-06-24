import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from db import db

Base = declarative_base()


class StudentModel(Base):
    __tablename__ = 'students'

    student_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(256))

    def __init__(self, first_name, last_name, email, phone_number, date_of_birth, sex, image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.image_url = image_url

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {"student_id": str(self.student_id),
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "date_of_birth": datetime.datetime.strftime(self.date_of_birth, '%Y-%m-%d'),
                "sex": self.sex,
                "image_url": self.image_url}

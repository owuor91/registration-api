import datetime

from sqlalchemy.ext.declarative import declarative_base

from db import db

Base = declarative_base()


class StudentModel(Base):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, first_name, last_name, email, phone_number, date_of_birth, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.sex = sex

    @classmethod
    def find_student_by_id(cls, student_id):
        return cls.query.filter_by(id=student_id).first()

    @classmethod
    def return_all(cls):
        return cls.query.all()

    @classmethod
    def find_student_by_phone_number(cls, _phone_number):
        return cls.query.filter_by(phone_number=_phone_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "date_of_birth": datetime.datetime.strftime(self.date_of_birth, '%Y-%m-%d'),
                "sex": self.sex}

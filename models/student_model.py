from db import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Columns(db.String(50), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(20), nullable=False)

    def __init__(self, first_name, last_name, email, phone_number, date_of_birth, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.sex = sex

    @classmethod
    def find_user_by_id(cls, student_id):
        return cls.query.filter_by(id=student_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "date_of_birth": self.date_of_birth,
                "sex": self.sex}

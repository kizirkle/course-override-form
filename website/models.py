from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    coursereqs = db.relationship('CourseReq')

class CourseReq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    student_name = db.Column(db.String(150))
    course_name = db.Column(db.String(150))
    course_num = db.Column(db.String(150))
    justification = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
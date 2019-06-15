from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask import Flask

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


class Grp(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    id_plan = db.Column(db.Integer)
    name = db.Column(db.String(100))
    students = db.relationship('Student', backref='grp', lazy='dynamic', cascade_backrefs='False')


class Student(db.Model):
    __searchable__ = ['name', 'patronymic']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    patronymic = db.Column(db.String(100))
    birth_date = db.Column(db.Date(),nullable=True)
    birth_place = db.Column(db.String(100))
    image = db.Column(db.String(100))
    grp_id = db.Column(db.Integer, db.ForeignKey('grp.id'))
    id_people = db.Column(db.Integer)
    social_web_profile = db.Column(db.String(100))
    thesis_topic = db.Column(db.String(100))
    advisor = db.Column(db.String(100))
    date_of_defense = db.Column(db.Date(),nullable=True)
    date_of_discharge = db.Column(db.Date(),nullable=True)
    reason_of_discharge = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    id_nationality = db.Column(db.String(100))
    old_surname = db.Column(db.String(100))
    old_name = db.Column(db.String(100))
    old_patronymic = db.Column(db.String(100))
    date_in = db.Column(db.Date())


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

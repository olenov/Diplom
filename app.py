from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
import datetime, re
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sql:1@localhost/Students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE'] = 'whoosh'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

def slugify(s):
    return re.sub('[^\w]+','-',s).lower()

class Student(db.Model):
    __searchable__ = ['name', 'second_name', 'patronymic']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    patronymic = db.Column(db.String(100))
    birth_date = db.Column(db.String(100))
    birth_place = db.Column(db.String(100))
    registration_adress = db.Column(db.String(100))
    basic_education = db.Column(db.String(100))
    full_names_of_parents_work_place_phone_number = db.Column(db.String(200))
    financial_situation = db.Column(db.String(100))
    temporary_adress = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    hobbies_and_interests = db.Column(db.String(100))
    work_place = db.Column(db.String(100))
    INN =db.Column(db.String(100))
    passport_data = db.Column(db.String(100))
    SNILS = db.Column(db.String(100))

    def __init__(self, name, second_name, patronymic, birth_place, birth_date, registration_adress, basic_education,
                 full_names_of_parents_work_place_phone_number, financial_situation, temporary_adress, phone_number, hobbies_and_interests,
                 work_place, INN, passport_data, SNILS):
        self.name=name
        self.second_name=second_name
        self.patronymic=patronymic
        self.birth_place=birth_place
        self.birth_date=birth_date
        self.registration_adress=registration_adress
        self.basic_education=basic_education
        self.full_names_of_parents_work_place_phone_number = full_names_of_parents_work_place_phone_number
        self.financial_situation = financial_situation
        self.temporary_adress = temporary_adress
        self.phone_number = phone_number
        self.hobbies_and_interests = hobbies_and_interests
        self.work_place = work_place
        self.INN = INN
        self.passport_data = passport_data
        self.SNILS = SNILS


class auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))
    hesh = db.Column(db.String(100))

    def __init__(self, login, password, hesh):
        self.login = login
        self.password = password
        self.hesh = hesh

students = Student.query
pages = students.paginate()

wa.whoosh_index(app, Student)

#class Student(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    Name = db.Column(db.String(32), nullable=False)
#    Second_name = db.Column(db.String(32), nullable=False)
#
#    Student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
#    student = db.relationship('Student', backref=db.backref())

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
import re
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager, UserMixin
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sql:1@localhost/Students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE'] = 'whoosh'
app.config['MAIL_SERVER'] =  'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'olenov1994@gmail.com'
app.config['MAIL_PASSWORD'] = 'soslow1994'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def slugify(s):
    return re.sub('[^\w]+','-',s).lower()


class Grp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_plan = db.Column(db.Integer)
    name = db.Column(db.String(100))
    students = db.relationship('Student', backref='grp', lazy='dynamic')

    def __init__(self, id_plan, name):
        self.id_plan = id_plan
        self.name = name


class Student(db.Model):
    __searchable__ = ['name', 'patronymic']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
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
    year_of_issue = db.Column(db.String(100))
    diploma_with_distinction = db.Column(db.String(100))
    diploma_number = db.Column(db.String(100))
    image = db.Column(db.String(100))
    grp_id = db.Column(db.Integer, db.ForeignKey('grp.id'))
    id_People = db.Column(db.Integer)

    def __init__(self, name, surname, patronymic, birth_place, birth_date, registration_adress, basic_education,
                 full_names_of_parents_work_place_phone_number, financial_situation, temporary_adress, phone_number, hobbies_and_interests,
                 work_place, INN, passport_data, SNILS, year_of_issue, diploma_with_distinction, diploma_number, image, grp_id, id_People):
        self.name=name
        self.surname=surname
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
        self.year_of_issue = year_of_issue
        self.diploma_with_distinction = diploma_with_distinction
        self.diploma_number = diploma_number
        self.image = image
        self.grp_id = grp_id
        self.id_People = id_People


wa.whoosh_index(app, Student)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))




#students = Student.query
#pages = students.paginate()

#wa.whoosh_index(app, Student)

#class Student(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    Name = db.Column(db.String(32), nullable=False)
#    Second_name = db.Column(db.String(32), nullable=False)
#
#    Student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
#    student = db.relationship('Student', backref=db.backref())

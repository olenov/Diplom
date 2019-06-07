from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()


class Grp(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    id_plan = db.Column(db.Integer)
    name = db.Column(db.String(100))
    students = db.relationship('Student', backref='grp', lazy='dynamic', cascade_backrefs='False')

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
    social_web_profile = db.Column(db.String(100))

    def __init__(self, name, surname, patronymic, birth_place, birth_date, registration_adress, basic_education,
                 full_names_of_parents_work_place_phone_number, financial_situation, temporary_adress, phone_number, hobbies_and_interests,
                 work_place, INN, passport_data, SNILS, year_of_issue, diploma_with_distinction, diploma_number, image, grp_id, id_People, social_web_profile):
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
        self.social_web_profile = social_web_profile


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

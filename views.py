from flask import Flask, render_template, request, redirect, url_for, session, flash
from app import *
from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from urllib.parse import urlparse, urljoin
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine('postgres://sql:1@localhost/Students', echo=True)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from openpyxl import load_workbook



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=4,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('main'))

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('main'))
        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    print(form)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Admin(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)

@app.route('/secretpage')
def homepage1():
    py=Student(title='xaxaxexe')
    return py.title

@app.route('/main', methods=['GET'])
@login_required
def main():
    page =  request.args.get('page')
    if page and page.isdigit():
        page =  int(page)
    else:
        page = 1
    students = Student.query
    pages = students.paginate(page=page, per_page=3)
    return render_template('main.html', students=Student.query.all(), pages=pages, name=current_user.username)


@app.route('/save', methods=['POST'])
@login_required
def save():
    if 'id' in request.form:
        id = request.form['id']
        student = Student.query.get(id)
    else:
        student = Student(request.form['name'], request.form['second_name'], request.form['patronymic'],request.form['birth_place'],request.form['birth_place'],
                          request.form['registration_adress'],request.form['basic_education'],request.form['full_names_of_parents_work_place_phone_number'],
                          request.form['financial_situation'],request.form['temporary_adress'], request.form['phone_number'], request.form['work_place'],
                          request.form['INN'],request.form['passport_data'], request.form['SNILS'], request.form['SNILS'])
        print(student)

    student.name = request.form['name']
    student.second_name = request.form['second_name']
    student.patronymic = request.form['patronymic']
    student.birth_place = request.form['birth_place']
    student.birth_date = request.form['birth_date']
    student.registration_adress = request.form['registration_adress']
    student.basic_education = request.form['basic_education']
    student.full_names_of_parents_work_place_phone_number = request.form['full_names_of_parents_work_place_phone_number']
    student.financial_situation = request.form['financial_situation']
    student.temporary_adress = request.form['temporary_adress']
    student.phone_number = request.form['phone_number']
    student.hobbies_and_interests = request.form['hobbies_and_interests']
    student.work_place = request.form['work_place']
    student.INN = request.form['INN']
    student.passport_data = request.form['passport_data']
    student.SNILS = request.form['SNILS']

    db.session.add(student)
    db.session.commit()

    return redirect(url_for('main'))


@app.route('/add')
@login_required
def adding():
    return render_template('student_form.html')

@app.route('/deleta',methods=['POST'])
def delete():
    id = request.form['id']
    student = Student.query.get(id)
    return render_template('deleta.html', student=student)

@app.route('/del_yes',methods=['POST'])
def delet():
    id = request.form['id']
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/edit/<id>')
@login_required
def edit(id):
    student = Student.query.get(id)
    return render_template('student_form.html', student=student)

@app.route('/search_results',methods=['POST'])
def show_results():
    search_word = request.form['word']
    students = Student.query.whoosh_search(search_word).all()
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    return render_template('serchres.html',students=students, pages=pages, name=current_user.username)

@app.route('/registration',methods=['POST'])
def reg():
    return render_template('registration.html')

@app.route('/openfiledialog')
def ofd():
    root = Tk()
    ftypes = [('excel file',"*.xlsx")]
    ttl  = "Title"
    dir1 = 'C:\\'
    root.fileName = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
    if not root.fileName:
        return redirect(url_for('main'))
    else:
        wb_val = load_workbook(filename = root.fileName)
        sheet_val = wb_val['Лист1']
        A1_val = sheet_val['A1'].value
        values = []
        for i in range(1,16):
            values.append(sheet_val['A' + str(i)].value)
        s=''
        for i in values:
            s = s + " " + i

        return s









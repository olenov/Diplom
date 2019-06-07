from main import *
from models import *

from flask import render_template, request, redirect, url_for, session, send_from_directory, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from urllib.parse import urlparse, urljoin
import os, xlsxwriter, string, random
from flask_login import login_user, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from openpyxl import load_workbook
from flask_mail import Message

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Пароль',validators=[InputRequired(),Length(min=4, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        error = 'Неверное имя пользователя или пароль'
        user = Admin.query.filter_by(username=form.username.data).first()
        if user:
            print(user)
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main'))
    return render_template('login.html', form=form, error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Admin(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main'))
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


@app.route('/', methods=['GET'])
@login_required
def main():
    page =  request.args.get('page')
    if page and page.isdigit():
        page =  int(page)
    else:
        page = 1
    students = Student.query

    pages = students.paginate(page=page, per_page=5)
    return render_template('main.html', students=students.all(), pages=pages, name=current_user.username)


@app.route('/save', methods=['POST'])
@login_required
def save():
    target = os.path.join(APP_ROOT, 'static/')
    if request.files.getlist("file"):
        z = request.files.getlist("file")[0]
        z.filename = request.form['name'] +' ' + request.form['surname']
        filename = z.filename
        destination = "/".join([target, filename])
        z.save(destination)
    else:
        filename = ''
    if 'id' in request.form:
        id = request.form['id']
        student = Student.query.get(id)
    else:
        student = Student(request.form['name'], request.form['surname'], request.form['patronymic'],request.form['birth_place'],request.form['birth_place'],
                          request.form['registration_adress'],request.form['basic_education'],request.form['full_names_of_parents_work_place_phone_number'],
                          request.form['financial_situation'],request.form['temporary_adress'], request.form['phone_number'], request.form['work_place'],
                          request.form['INN'],request.form['passport_data'], request.form['SNILS'], request.form['SNILS'], request.form['year_of_issue'],
                          request.form['diploma_with_distinction'] , request.form['diploma_number'], '/static/' + filename, request.form['grp_id'], request.form['id_People'], request.form['social_web_profile'])
        print(student)

    student.name = request.form['name']
    student.surname = request.form['surname']
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
    student.year_of_issue = request.form['year_of_issue']
    student.diploma_with_distinction = request.form['diploma_with_distinction']
    student.diploma_number = request.form['diploma_number']
    student.image = '/static/' + filename
    if request.form['grp_id']:
        student.grp_id = request.form['grp_id']
    else:
        student.grp_id = None
    if request.form['id_People']:
        student.id_People = request.form['id_People']
    else:
        student.id_People = None
    student.social_web_profile = request.form['social_web_profile']

    db.session.add(student)
    db.session.commit()

    return redirect(url_for('main'))


@app.route('/add')
@login_required
def adding():
    return render_template('student_form.html', name=current_user.username)

@app.route('/deleta',methods=['POST'])
def delete():
    id = request.form['id']
    student = Student.query.get(id)
    return render_template('deleta.html', student=student, name=current_user.username)

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
    group = Grp.query.all()
    return render_template('student_form.html', student=student, group=group, name=current_user.username)

@app.route('/search_results',methods=['POST'])
def show_results():
    search_word = request.form['word']
    students = Student.query.whoosh_search(search_word).all()
    groups = Grp.query.whoosh_search(search_word).all()
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = students.paginate(page=page, per_page=5)
    return render_template('serchres.html', students=students, pages=pages, name=current_user.username, groups=groups)

@app.route('/stud_in_grp/<id>')
def ssig(id):
    grp = Grp.query.get(id)
    students = grp.students.all()
    return render_template('stofgrp.html', students=students, name=current_user.username)

@app.route('/registration',methods=['POST'])
def reg():
    return render_template('registration.html')

@app.route('/openfiledialog', methods=['POST','GET'])
def ofd():
    target = os.path.join(APP_ROOT, 'static/')
    if request.files.getlist("file"):
        z = request.files.getlist("file")[0]
        filename = z.filename
        destination = "/".join([target, filename])
        z.save(destination)
    else:
        filename = ''
    if filename == '':
        return redirect(url_for('main'))
    else:
        wb_val = load_workbook(filename = destination)
        sheet_val = wb_val['students']
        for i in range(1,20):
            student = Student(sheet_val['F'+str(i)].value, sheet_val['E'+str(i)].value, sheet_val['G'+str(i)].value, '', '', '','','','','','','','','','','','','','','',None,0,'')
            db.session.add(student)
            db.session.commit()
        return redirect(url_for('main'))


@app.route("/openfiledialogpage", methods=['GET', 'POST'])
def ofdp():
    return render_template('openfiledialogpage.html')

@app.route('/report_generation')
def generation():
    return render_template('report_generation.html', name=current_user.username)



@app.route('/report_generate',methods=['POST','GET'])
def generate():
    workbook = xlsxwriter.Workbook('Отчет о выпускниках.xlsx')
    count = 0
    students = Student.query.all()
    worksheet = workbook.add_worksheet()
    if count == 0 and request.form.get('2001'):
        students = Student.query.filter_by(year_of_issue='2001')
        count += 1

    if count == 0 and request.form.get('2013'):
        students = Student.query.filter_by(year_of_issue='2013')
        count += 1
    if count > 0 and request.form.get('2013'):
        students = students.union(Student.query.filter_by(year_of_issue='2013'))

    if count == 0 and request.form.get('2002'):
        students = Student.query.filter_by(year_of_issue='2002')
        count += 1
    if count > 0 and request.form.get('2002'):
        students = students.union(Student.query.filter_by(year_of_issue='2002'))

    count = [1]*100
    letter = [65]*100
    Letter = 64
    for i in students:
        if request.form.get('1'):
            worksheet.write_column(chr(letter[0]) + str(count[0]),[i.surname, ])
            count[0] += 1
            if count[0] == 2:
                Letter += 1
                letter[0] = Letter
        if request.form.get('2'):
            worksheet.write_column(chr(letter[1]) + str(count[1]),[i.name, ])
            count[1] += 1
            if count[1] == 2:
                Letter += 1
                letter[1] = Letter
        if request.form.get('3'):
            worksheet.write_column(chr(letter[2]) + str(count[2]),[i.patronymic, ])
            count[2] += 1
            if count[2] == 2:
                Letter += 1
                letter[2] = Letter
        if request.form.get('4'):
            worksheet.write_column(chr(letter[3]) + str(count[3]),[i.year_of_issue, ])
            count[3] += 1
            if count[3] == 2:
                Letter += 1
                letter[3] = Letter
    workbook.close()
    return send_from_directory('C:\\Users\\Константин\\PycharmProjects\\blog','Отчет о выпускниках.xlsx')#redirect(url_for('main'))

@app.route('/change_password')
def change_pass():
    user = current_user
    return render_template('change_password.html', user=user, name=user.username, b=current_user.password)

@app.route('/new_pass', methods=['POST','GET'])
def new_pass():
    if check_password_hash(current_user.password, request.form['old_password']) :
        current_user.password = generate_password_hash(request.form['new_password'], method='sha256')
    db.session.commit()
    return render_template('change_password.html', user=current_user,a=generate_password_hash (request.form['old_password']))

@app.route('/forgot_password')
def forgot_pass():
    user = Admin.query.filter_by(username='spider-man').first()
    return render_template('forgot_password.html', user=user)

@app.route('/send_new_pass', methods=['POST','GET'])
def send_pass():
    user = Admin.query.filter_by(username=request.form['username']).first()
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    user.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    msg = Message('hello!', sender='olenov1994@gmail.com', recipients=['olenov1994@gmail.com'])
    msg.body = 'vash noviy password -' + password
    mail.send(msg)
    return render_template('forgot_password.html', user=user)


@app.route('/groups', methods=['GET'])
def groups():
    groups = Grp.query.all()
    return render_template('groups.html', groups=groups, name=current_user.username)

@app.route('/save_group', methods=['POST'])
def sg():
    if 'id' in request.form:
        id = request.form['id']
        group = Grp.query.get(id)
    else:
        group = Grp(request.form['id_plan'],request.form['name'])

    group.name = request.form['name']
    group.id_plan = request.form['id_plan']

    db.session.add(group)
    db.session.commit()

    return redirect(url_for('groups'))


@app.route('/edit_group/<id>')
@login_required
def eg(id):
    student = Student.query.all()
    group = Grp.query.get(id)
    return render_template('group_form.html', student=student, group=group, name=current_user.username)


@app.route('/add_grp')
@login_required
def ag():
    return render_template('group_form.html', name=current_user.username)


@app.route('/del_group',methods=['POST'])
def delg():
    id = request.form['id']
    group = Grp.query.get(id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('groups'))


print('VIEWS:', app.root_path)
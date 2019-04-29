from flask import Flask, render_template, request, redirect, url_for
from app import app
from app import Student
from app import db


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getvalue():
    kek=Student()
    kek.body = request.form['name']
    kek.slug = request.form['name1']
    kek.title = request.form['name2']
    return render_template('pass.html', b=kek.body, s=kek.slug, t=kek.title, students=Student.query.all())


@app.route('/secretpage')
def homepage1():
    py=Student(title='xaxaxexe')
    return py.title

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', students=Student.query.all())

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    second_name = request.form['second_name']
    patronymic = request.form['patronymic']
    birth_place = request.form['birth_place']
    birth_date = request.form['birth_date']
    registration_adress = request.form['registration_adress']
    basic_education = request.form['basic_education']
    full_names_of_parents_work_place_phone_number = request.form['full_names_of_parents_work_place_phone_number']
    financial_situation = request.form['financial_situation']
    temporary_adress = request.form['temporary_adress']
    phone_number = request.form['phone_number']
    hobbies_and_interests = request.form['hobbies_and_interests']
    work_place = request.form['work_place']
    INN = request.form['INN']
    passport_data = request.form['passport_data']
    SNILS = request.form['SNILS']

    db.session.add(Student(name, second_name, patronymic,birth_place, birth_date, registration_adress, basic_education,
                           full_names_of_parents_work_place_phone_number, financial_situation, temporary_adress,
                           phone_number, hobbies_and_interests, work_place, INN, passport_data, SNILS))
    db.session.commit()

    return redirect(url_for('main'))

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
def edit(id):
    student = Student.query.get(id)
    return render_template('edit.html', student=student)

@app.route('/editing',methods=['POST'])
def editing():
    name = request.form['name']
    second_name = request.form['second_name']
    patronymic = request.form['patronymic']
    birth_place = request.form['birth_place']
    birth_date = request.form['birth_date']
    registration_adress = request.form['registration_adress']
    basic_education = request.form['basic_education']
    full_names_of_parents_work_place_phone_number = request.form['full_names_of_parents_work_place_phone_number']
    financial_situation = request.form['financial_situation']
    temporary_adress = request.form['temporary_adress']
    phone_number = request.form['phone_number']
    hobbies_and_interests = request.form['hobbies_and_interests']
    work_place = request.form['work_place']
    INN = request.form['INN']
    passport_data = request.form['passport_data']
    SNILS = request.form['SNILS']
    id = request.form['id']
    student = Student.query.get(id)
    student.name = name
    student.second_name = second_name
    student.patronymic = patronymic
    student.birth_place = birth_place
    student.birth_date = birth_date
    student.registration_adress = registration_adress
    student.basic_education = basic_education
    student.full_names_of_parents_work_place_phone_number = full_names_of_parents_work_place_phone_number
    student.financial_situation = financial_situation
    student.temporary_adress = temporary_adress
    student.phone_number =phone_number
    student.hobbies_and_interests = hobbies_and_interests
    student.work_place =work_place
    student.INN = INN
    student.passport_data = passport_data
    student.SNILS = SNILS
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/search_results',methods=['POST'])
def show_results():
    search_word = request.form['word']
    students = Student.query.whoosh_search(search_word).all()
    return render_template('search_results.html',result=students)





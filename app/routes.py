# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Comment, Homework, Task, Answers
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
import helpers


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    else:
        return render_template('index.html', title='Домашняя страница')


@app.route('/homework/<hw_task>')
@login_required
def homework(hw_task):
    # print('>>>', hw_task)
    task = Task.query.filter_by(id=hw_task).first_or_404()
    subtasks = Subtask.query.filter_by(task_id=hw_task).all()
    return render_template('homework.html', title='Домашка', task=task, subtasks=subtasks)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    subt_box = helpers.Box()
    notification = ''
    if request.method == 'POST':
        subt_box.import_request(request.form)
        if ('save' in request.form) and (len(subt_box.export_dict()['errors']) != []):
            print('>>> Saved!')
            new_task = Task(
                level=subt_box.export_json()['level'],
                theme=subt_box.export_json()['theme'],
                name=subt_box.export_json()['name'],
                course=subt_box.export_json()['course'],
                body=subt_box.export_json()['subs'])
            # print(new_task)
            db.session.add(new_task)
            db.session.commit()
            notification = 'Вы создали новое задание!'
            # print(subt_box.export_json())
    # print(subt_box.export_dict())
    return render_template('add_task.html', title='Добавить задание', subtasks=subt_box.export_dict(), notification=notification)


@app.route('/cabinet')
@login_required
def cabinet():
    if current_user.is_authenticated:
        homeworks = Homework.query.filter_by(user_id=current_user.id).join(Task, Homework.task_id==Task.id).all()
        unfinished = len([x.finished for x in homeworks if x.finished==False])
        return render_template('cabinet.html', title='Ваш дневник', homeworks=homeworks, unfinished=unfinished)
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Теперь вы готовы идти на занятия!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Записаться в журнал', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Изменить профиль', form=form)


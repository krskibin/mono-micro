from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required, login_user, logout_user
from mono import app, db
from mono.forms import LoginForm, TaskForm, RegistrationForm, UpdateTaskForm
from mono.models import Task, User


@app.route('/')
@app.route('/index')
def index():
    data = {
        'seen': False
    }
    return render_template('index.html', data=data)


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        db_task = Task(header=form.body.data, body=form.header.data, author=current_user)
        db.session.add(db_task)
        db.session.commit()
        flash('Task submitted')
        return redirect(url_for('index'))

    is_done = request.args.get('isDone', '')
    if is_done != '':
        if is_done.lower() == 'false':
            db_tasks = Task.query.filter_by(user_id=current_user.id, is_done=False).all()
        else:
            db_tasks = Task.query.filter_by(user_id=current_user.id, is_done=True).all()
    else:
        db_tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template('tasks.html', form=form, tasks=db_tasks, user=current_user)


@app.route('/task-delete/<int:id>')
@login_required
def delete_task(id):
    db_task = Task.query.filter_by(user_id=current_user.id, id=id).first()
    db.session.delete(db_task)
    db.session.commit()
    return redirect(url_for('tasks'))


@app.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def task(id):
    form = UpdateTaskForm()
    if form.validate_on_submit():
        db_task = Task.query.filter_by(user_id=current_user.id, id=id).first()
        db_task.header = form.header.data
        db_task.body = form.body.data
        db_task.is_done = form.is_done.data or False
        db.session.commit()
    db_task = Task.query.filter_by(user_id=current_user.id, id=id).first()
    return render_template('task.html', form=form, task=db_task)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))
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
    return render_template('login.html', title='Sign In', form=form)


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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

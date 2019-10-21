from wtforms.validators import EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    header = TextField('What you want to do?')
    body = TextAreaField('Describe what you want to do?')
    submit = SubmitField('Create task')


class UpdateTaskForm(FlaskForm):
    header = TextField('What you want to do?')
    body = TextAreaField('Describe what you want to do?')
    is_done=BooleanField('Is task done?')
    submit = SubmitField('Update')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
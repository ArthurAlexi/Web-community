from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from community.models import User
from flask_login import current_user


class FormCreateAccount(FlaskForm):
    name = StringField('User name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirmPassword = PasswordField('Confirm your Password', validators=[DataRequired(), EqualTo('password')])
    btnSubmitCreate = SubmitField('Create')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail already registered')


class FormLogin(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    remember = BooleanField('remember me?')
    btnSubmitLogin = SubmitField('login')


class FormEditProfile(FlaskForm):
    name = StringField('User name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    photo = FileField('Profile picture', validators=[FileAllowed(['png', 'jpg'])])
    course_math = BooleanField('math')
    course_philosophy = BooleanField('philosophy')
    course_history = BooleanField('history')
    course_chemical = BooleanField('chemical')
    course_Physical = BooleanField('Physical')

    btnSubmitEditProfile = SubmitField('Confirm')

    def validate_email(self, email):
        # verificar se o cara mudou de email:
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('E-mail already registered')


class FormPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField('subject', validators=[DataRequired()])
    btnSubmit = btnSubmitLogin = SubmitField('Submit')

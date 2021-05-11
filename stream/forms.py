from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from stream.models import accounts


class RegisterForm(FlaskForm):
    user = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwd = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    conf_passwd = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('passwd')])
    submit = SubmitField('Sign Up')

    def validate_user(self, username):
        user = accounts.query.filter_by(user=username.data).first()
        if user:
            raise ValidationError('Username already exists, choose a different one.')

    def validate_email(self, email):
        email = accounts.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email address already exists, choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwd = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    rem = BooleanField('Keep me signed in')
    submit = SubmitField('Login')

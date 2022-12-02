from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email, Regexp
from wtforms import ValidationError
from models import User
from database import db
from wtforms import TextAreaField

class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Username', validators=[Length(3, 16)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])
    #TODO create regex phrase for checking password for reqs
    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=20), Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%*#?&]{6,}$', message="Please enter a valid password with a length of 6-20 characters, uppercase letters, numbers, and symbols (@$!%*#?&)")
    ])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Email already in use.')

class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

class CommentForm(FlaskForm):
    class Meta:
        csrf = False

    comment = TextAreaField('Comment',validators=[Length(min=1)])

    submit = SubmitField('Add Comment')
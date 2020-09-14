from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from chat_app.models import User, Message, get_all_users
from datetime import datetime


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message="username required"), Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired(message='password required'), Length(min=4)])
    conf_password = PasswordField('conf_password',
                                  validators=[DataRequired(message='password required'), EqualTo('password')])
    submit_button = SubmitField('submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Taken')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class MessageFrom(FlaskForm):
    subject = StringField('username', validators=[Length(max=50), DataRequired()])
    content = TextAreaField('content')
    receiver = SelectField('receiver', choices=get_all_users())
    submit = SubmitField('Send to:')



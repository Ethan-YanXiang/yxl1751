# 從 包 調用 模組
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields import DateField, TelField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Email, Length, NumberRange, ValidationError
# DataRequired: non-empty input
# EqualTo: two passwords are identical
# Email: valid email address


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    date = DateField('Date of Birth', validators=[DataRequired(message='Required field')])
    number = TelField('Telephone Number', validators=[DataRequired()])
    address = TextAreaField('Mailing Address', validators=[DataRequired()])
    height = DecimalField('Height', validators=[DataRequired(), NumberRange(min=54.6, max=272.0, message='Height must between %(min)s and %(max)s cm')])
    weight = DecimalField('Weight', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(granular_message=True)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='%(other_label)s doesn\'t match')])
    submit = SubmitField('Register')



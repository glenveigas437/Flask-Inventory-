from wtforms import Form, StringField, PasswordField, validators, ValidationError, SelectField, IntegerField, SubmitField
from flask_wtf import FlaskForm
from .models import *

class AdminRegistrationForm(FlaskForm):
    username = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    address = StringField('Address', [validators.Length(min=4, max=300)])

    def validate_username(self, username):
        if AdminUser.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already registered")

    def validate_email(self, email):
        if AdminUser.query.filter_by(email=email.data).first():
            raise ValidationError("This Email is already registered")

class AdminLoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired()])
    

class MovementForm(FlaskForm):
    to_location = SelectField('To Location', coerce=int) #coerce is for the dropdown box so it considers the id of the entry made
    from_location = SelectField('From Location', coerce=int)
    product = SelectField('Product', coerce=int)
    quantity = IntegerField('Quantity')
    add_movement = SubmitField('Add Movement')
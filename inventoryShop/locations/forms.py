from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm
from .models import Location

class LocationRegisterForm(FlaskForm):
	name = StringField('Location: ')
	email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
	password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm',
	message ="Both Passwords must match")])
	confirm = PasswordField('Repeat Password: ',[validators.DataRequired()])
	address = StringField('Address: ',[validators.DataRequired()])
	submit = SubmitField('Register')

	def validate_location(self, name):
		if Location.query.filter_by(name=name.data).first():
			raise ValidationError("This Location is already registered")

	def validate_email(self, email):
		if Location.query.filter_by(email=email.data).first():
			raise ValidationError("This Email is already registered")

class LocationLoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
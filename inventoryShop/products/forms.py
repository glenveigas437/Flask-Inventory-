from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators

class AddProducts(Form):
	name = StringField('Name', [validators.DataRequired()])
	stock = IntegerField('Stock', [validators.DataRequired()])
	description = TextAreaField('Description', [validators.DataRequired()])
	image1 = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

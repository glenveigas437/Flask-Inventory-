from inventoryShop import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import json

@login_manager.user_loader
def user_loader(user_id):
	return Location.query.get(user_id)

class Location(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(50), unique=False)
	address = db.Column(db.String(50), unique=False)

	def __repr__(self):
		return '<Location %r>' % self.name


class JsonEcodedDict(db.TypeDecorator):
	impl = db.Text

	def process_bind_param(self, value, dialect):
		if value is None:
			return '{}'
		else:
			return json.dumps(value)
	def process_result_value(self, value, dialect):
		if value is None:
			return {}
		else:
			return json.loads(value)


class LocationOrder(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invoice = db.Column(db.String(20), unique=True, nullable=False)
	status = db.Column(db.String(20), default='Pending', nullable=False)
	location_id = db.Column(db.String(100), unique=False, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
	orders = db.Column(JsonEcodedDict)

	def __repr__(self):
		return '<LocationOrder %r>' % self.invoice


db.create_all()
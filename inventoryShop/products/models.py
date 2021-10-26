from inventoryShop import db
from datetime import datetime

class Product(db.Model):
	__searchable__ = ['name', 'desc']
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False, unique=True)
	stock = db.Column(db.Integer(), nullable=False)
	brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
	brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	category = db.relationship('Category', backref=db.backref('categories', lazy=True))
	desc = db.Column(db.Text(), nullable=False)

	image1 = db.Column(db.String(150), nullable=False, default='image.jpg')


	def __repr__(self):
		return '<Product %r>' % self.name

class Brand(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	name = db.Column(db.String(30), nullable=False, unique=True)

	def __repr__(self):
		return '<Brand %r>' % self.name

class Category(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	name = db.Column(db.String(30), nullable=False, unique=True)

	def __repr__(self):
		return '<Category %r>' % self.name


db.create_all()
from flask import redirect, render_template, url_for, flash, request, session
from inventoryShop import db, app, photos, search
from .forms import AddProducts
from .models import Brand, Category, Product
import secrets



@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=8)
    return render_template('products/index.html', title='Home', products=products)

#Returns Search Results
@app.route('/result')
def result():
	searchword= request.args.get('q')
	products = Product.query.msearch(searchword, fields=['name', 'desc'], limit=3)
	return render_template('products/result.html', products=products)

#Gets description About the product
@app.route('/product/<int:id>')
def product_desc(id):
    product = Product.query.get_or_404(id)
    return render_template('products/product_desc.html', product=product)

#View to add Brands
@app.route('/addBrand', methods=['GET','POST'])
def addBrand():
	if 'email' not in session:
		flash('Please login first', 'warning')
		return redirect(url_for('login'))
	if request.method=='POST':
		getBrand = request.form.get('brand')
		brand = Brand(name=getBrand)
		db.session.add(brand)
		flash(f'The Brand {getBrand} has been added to your database', 'success')
		db.session.commit()
		return redirect(url_for('addBrand'))
	return render_template('products/addBrand.html',brands='brands')

#View to add Categories
@app.route('/addCategory', methods=['GET','POST'])
def addCategory():
	if 'email' not in session:
		flash('Please login first', 'warning')
		return redirect(url_for('login'))
	if request.method=='POST':
		getCategory = request.form.get('category')
		category = Category(name=getCategory)
		db.session.add(category)
		flash(f'The Category {getCategory} has been added to your database', 'success')
		db.session.commit()
		return redirect(url_for('addCategory'))
	return render_template('products/addBrand.html')

#View to add Products
@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
	if 'email' not in session:
		flash('Please login first', 'warning')
		return redirect(url_for('login'))
	brands = Brand.query.all()
	categories = Category.query.all()
	form = AddProducts(request.form)

	if request.method == 'POST':
		name = form.name.data
		stock = form.stock.data
		desc = form.description.data
		brand = request.form.get('brand')
		category = request.form.get('category') 
		image1=photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
		addProd = Product(name=name, stock=stock, desc=desc, brand_id=brand, category_id=category, image1=image1)
		db.session.add(addProd)
		flash(f'The Product {form.name.data} has been added to the database', 'success')
		db.session.commit()
		return redirect(url_for('admin'))
	return render_template('products/addProducts.html', form=form, title='Add Products', brands=brands, categories=categories)


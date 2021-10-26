from flask import render_template, session, request, redirect, url_for, flash, current_app
from inventoryShop import app, db, photos, search, bcrypt, login_manager
from inventoryShop.inventoryAdmin.models import Movement
from inventoryShop.products.models import Product
from inventoryShop.inventoryAdmin.routes import available_quantity 
from flask_login import login_required, current_user, logout_user, login_user
from .forms import LocationRegisterForm, LocationLoginForm
from .models import Location, LocationOrder
import secrets, pygal, pdfkit, os
import datetime as datetime

config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

kitoptions = {
  "enable-local-file-access": None
}

#Function:location_register
#Description: Register Location
@app.route('/locations/register', methods=['GET','POST'])
def location_register():
	form = LocationRegisterForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data)
		register = Location(name=form.name.data, email=form.email.data, password=hash_password, address=form.address.data)
		db.session.add(register)
		flash(f'Welcome {form.email.data}, Thank You for regsitering Location - {form.name.data}', 'success')
		db.session.commit()
		return redirect(url_for('Locationlogin'))

	return render_template('locations/register.html', form=form)

#Function:Locationlogin
#Description: Location Supervisor Login
@app.route('/locations/login', methods=['GET', 'POST'])
def Locationlogin():
	form = LocationLoginForm()
	print(Location.query.all())
	if form.validate_on_submit():
		location = Location.query.filter_by(email=form.email.data).first()
		if location and bcrypt.check_password_hash(location.password, form.password.data):
			login_user(location)
			flash(f'You are now logged in at Location-{location.name}', 'success')
			next = request.args.get('next')
			return redirect(next or url_for('home'))
		flash('Incorrect Email and Password Combination', 'danger')
		return redirect(url_for('Locationlogin'))
	return render_template('locations/login.html', form=form)

#Logout Location Supervisor
@app.route('/locations/logout')
def locationlogout():
	logout_user()
	return redirect(url_for('Locationlogin'))

#Returns a view of order sent to the cart
@app.route('/getorder')
@login_required
def get_order():
	if current_user.is_authenticated:
		location_id  = current_user.name
		invoice = secrets.token_hex(5)
		try:
			order = LocationOrder(invoice = invoice, location_id=location_id, orders=session['requestCart'])
			db.session.add(order)
			db.session.commit()
			session.pop('requestCart')
			flash('Your order has been successfully added', 'success')
			return redirect(url_for('home'))
		except Exception as e:
			flash('Some thing went wrong with your order', 'danger')
			return redirect(url_for('getCart'))

#View all orders in a particular location
@app.route('/myOrders')
@login_required
def myOrders():
	if current_user.is_authenticated:
		location_id  = current_user.name
		LocationOrders = LocationOrder.query.filter_by(location_id=location_id).all()
		return render_template('locations/myOrders.html', title='My Orders', LocationOrders=LocationOrders)

#In detail view of the order cart
@app.route('/myOrders/view/<invoice>')
@login_required
def viewMyOrder(invoice):
	if current_user.is_authenticated:
		currentOrder = LocationOrder.query.filter_by(invoice=invoice).all() 
		x=currentOrder[0].orders
		return render_template('locations/viewOrder.html', title='Order', x=x)

#Location Profile
@app.route('/locations/profile')
def myProfile():
    if current_user.is_authenticated:
    	location_id  = current_user.id
    	locationMovementsTo = Movement.query.filter_by(to_location_id=location_id).all()
    	locationMovementsFrom = Movement.query.filter_by(from_location_id=location_id).all()
    	return render_template('locations/locationProfile.html', lmt=locationMovementsTo, lmf=locationMovementsFrom)

#Returns The Status of location activities
@app.route('/locations/status')
def myStatus():
	if current_user.is_authenticated:

		Locations = Location.query.all()
		Products = Product.query.all()

		status_list = []

		for product in Products:
			row = {}
			row["product"] = product.name
			row["quantity"] = available_quantity(current_user.id,product.id)
			if row["quantity"]<0:
				row["quantity"]=0
			status_list.append(row)


		locIntDict={}

		movement = Movement.query.all()
		
		for move in movement:
			if(move.from_location_id==current_user.id):
				if(move.to_location.name not in locIntDict):
					locIntDict[move.to_location.name]=[0,0]
				locIntDict[move.to_location.name][0]+=1

		locIntDict['HQ']=[0,0]
		for move in movement:
			if(move.to_location_id==current_user.id):
				if(move.from_location is None):
					locIntDict['HQ'][1]+=1
					continue
				if(move.from_location.name not in locIntDict):
					locIntDict[move.from_location.name]=[0,0]
				locIntDict[move.from_location.name][1]+=1


		line_chart = pygal.StackedBar()
		line_chart.title = 'Location Interaction (in %)'
		line_chart.x_labels = ['To', 'From']
		for key, value in locIntDict.items():
			line_chart.add(key, value)

		line_chart=line_chart.render_data_uri()		
	
		return render_template('locations/status.html', status_list=status_list, line_chart=line_chart)

#Downloads the status report of the Location Activities
@app.route('/locations/status/pdf', methods=['POST'])
def statusPdf():
	if current_user.is_authenticated:
		if request.method=='POST':
			date=datetime.datetime.now()
			dateX=date.strftime('%d/%m/%Y')


			Locations = Location.query.all()
			Products = Product.query.all()

			status_list = []

			for product in Products:
				row = {}
				row["product"] = product.name
				row["quantity"] = available_quantity(current_user.id,product.id)
				if row["quantity"]<0:
					row["quantity"]=0
				status_list.append(row)


			locIntDict={}
			movement = Movement.query.all()

			for move in movement:
				if(move.from_location_id==current_user.id):
					if(move.to_location.name not in locIntDict):
						locIntDict[move.to_location.name]=[0,0]
					locIntDict[move.to_location.name][0]+=1

			locIntDict['HQ']=[0,0]
			for move in movement:
				if(move.to_location_id==current_user.id):
					if(move.from_location is None):
						locIntDict['HQ'][1]+=1
						continue
					if(move.from_location.name not in locIntDict):
						locIntDict[move.from_location.name]=[0,0]
					locIntDict[move.from_location.name][1]+=1


			rendered = render_template('locations/statusPdf.html',dateX=dateX,status_list=status_list, locIntDict=locIntDict)
			pdf = pdfkit.from_string(rendered, 'Status'+current_user.name+'.pdf', configuration=config, options=kitoptions)
		return redirect(url_for('myStatus'))
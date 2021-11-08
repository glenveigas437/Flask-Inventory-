from flask import render_template, session, request, redirect, url_for, flash, current_app
from inventoryShop import app, db, bcrypt, photos
from inventoryShop.products.forms import AddProducts
from inventoryShop.locations.models import *
from inventoryShop.products.models import *
from geopy import distance
from .forms import *
from .models import AdminUser
from sqlalchemy.sql.functions import func
import os, secrets, datetime, pygal, pdfkit, requests, json, inspect


config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

kitoptions = {
  "enable-local-file-access": None
}

#Function: admin
#Decsription: Admin Home
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    return render_template('inventoryAdmin/home.html', title='Admin Home')

@app.route('/')
def homePage():
    return render_template('home.html', title='Home Page')



#Function: register
#Decsription: Admin Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        adminU = AdminUser(username=form.username.data, email=form.email.data,
                    password=hash_password, address=form.address.data)
        db.session.add(adminU)
        flash(f'Thank You! {form.username.data} registered successfully', 'success')
        db.session.commit()
        print(AdminUser.query.all())
        return redirect(url_for('login'))
    return render_template('inventoryAdmin/register.html', form=form)

#Function: login
#Decsription: Admin Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admin = AdminUser.query.filter_by(email = form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong email and password combination', 'danger')
    return render_template('inventoryAdmin/login.html', form=form, title='Login Page')


#Function: logout
#Decsription: Admin logout from account
@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        return redirect(url_for('login'))

#Function: brands
#Description: View Brands Added
@app.route('/brands')
def brands():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('inventoryAdmin/brand.html', title='Brand Page', brands=brands)

#Function: updateBrand
#Description: Update details of a brand
@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updateBrand(id):
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method=='POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated!','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)

#Function: categories
#Description: View for categories
@app.route('/categories')
def categories():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('inventoryAdmin/brand.html', title='Category Page', categories=categories)


#Function: updateCategory
#Description: View for Updating categories
@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updateCategory(id):
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=='POST':
        updatecat.name = category
        flash(f'Your Category has been updated!','success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatecat=updatecat)

#Function: updateProduct
#Description: View for updating Products
@app.route('/updateProduct/<int:id>', methods=['GET','POST'])
def updateProduct(id):
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    categories = Category.query.all()
    brands = Brand.query.all()
    product = Product.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = AddProducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.stock = form.stock.data
        product.desc = form.description.data
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app, root_path,"static/images/"+product.image1))
                product.image1=photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
            except:
                product.image1=photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'The Product has been updated', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.stock.data = product.stock
    form.description.data = product.desc
    return render_template('products/updateProducts.html', title='Update Product Page', form=form, brands=brands, categories=categories, product=product)

#Function: productList
#Description: View for Listing Products
@app.route('/productList')
def productList():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('inventoryAdmin/productsList.html', title='Product List', products=products)


#Function: orderRequests
#Description: Displays Orders sent by Locations
@app.route('/inventoryAdmin/orderrequests')
def orderRequests():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    orderreqPend = LocationOrder.query.filter_by(status='Pending').all()
    orderreqComp = LocationOrder.query.filter_by(status='Completed').all()
    return render_template('inventoryAdmin/orderreq.html', title='Order Requests', orderreqPend=orderreqPend, orderreqComp=orderreqComp)

#Function: viewOrders
#Description: Details of Products available in the orders
@app.route('/inventoryAdmin/orderrequests/vieworder/<invoice>')
def viewOrders(invoice):
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    currentOrder = LocationOrder.query.filter_by(invoice=invoice).all() 
    x=currentOrder[0].orders
    status = currentOrder[0].status
    return render_template('inventoryAdmin/vieworder.html', status=status, x=x)

#Function: add_movements
#Description: Feature to make movements
@app.route('/inventoryAdmin/movements',methods=["GET","POST"])
def add_movements():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    form = MovementForm()
    form.to_location.choices = [(location.id, location.name) for location in Location.query.all()] #for the dropdown boxes
    form.from_location.choices = [(location.id, location.name) for location in Location.query.all()] #for the dropdown boxes
    form.product.choices = [(product.id, product.name) for product in Product.query.all()] #for the dropdown boxes
    form.from_location.choices.insert(0, (0, 'None'))   #can select 'None' option too
    if request.method=='POST':
        new_movement = Movement(to_location_id=form.to_location.data, from_location_id=form.from_location.data, product_id=form.product.data, quantity=form.quantity.data)
        if form.from_location.data==0:
            prod_id=form.product.data
            prod=Product.query.get_or_404(prod_id)
            prodQuantity=prod.stock-form.quantity.data
            if prodQuantity<0:
                flash('Product cannot be moved, due to insufficient quantity!', 'danger')
            else:
                db.session.add(new_movement)
                prod.stock=prodQuantity
                flash('Product has been moved!', 'success')
                db.session.commit()
            return redirect(url_for('add_movements'))
        else:
            quantity_check = available_quantity(form.from_location.data, form.product.data)
            if int(form.quantity.data) > quantity_check:
                flash('Product cannot be moved, due to insufficient quantity!', 'danger')
            else:
                new_movement=Movement(to_location_id=form.to_location.data, from_location_id=form.from_location.data, product_id=form.product.data, quantity=form.quantity.data)
                db.session.add(new_movement)
                db.session.commit()
                flash('Product has been moved!', 'success') 
            return redirect(url_for('add_movements'))       
    return render_template('inventoryAdmin/movements.html', form=form) 

#to check the available quantity of stocks
def available_quantity(location, product):
    sum_from=Movement.query.filter(Movement.to_location_id==location,Movement.product_id==product).from_self(func.sum(Movement.quantity, )).all()
    sum_to=Movement.query.filter(Movement.from_location_id==location,Movement.product_id==product).from_self(func.sum(Movement.quantity,name="moved")).all()
    sum_from=sum_from[0][0] 
    sum_to=sum_to[0][0]
    if sum_from is None:
        sum_from=0  
    if sum_to is None:
        sum_to=0
    
    quantity_check=sum_from - sum_to
    return quantity_check   

#function: view_movements
#Description: View to List Movements
@app.route('/inventoryAdmin/view_movements')
def view_movements():
    movement_list = Movement.query.all()
    return render_template('inventoryAdmin/movementList.html', movement_list=movement_list)

#function: update_status
#Description: By Default, the status of an order request is set as Pending, once the move is complete
#This function sets it to Completed
@app.route('/inventoryAdmin/orderrequests/<invoice>')
def update_status(invoice):
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    status='Completed'
    LocationOrder.query.filter_by(invoice=invoice).update({'status': status})
    db.session.commit()
    return redirect(url_for('orderRequests'))

#function: viewLocation
#Description: view to return a list of Locations registered 
@app.route('/inventoryAdmin/locations')
def viewLocations():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    location = Location.query.all()
    return render_template('/inventoryAdmin/locations.html', location=location)


def fetch(address):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params={
        'q': address,
        'format': 'geocodejson'
    }
    res = requests.get(url=base_url, params=params)

    if res.status_code==200:
        return res
    else:
        return None

def parse(res):
    try:
        data = coordinates = json.dumps(res['features'][0]['geometry']['coordinates'], indent=2).replace('\n', '').replace('[', '').replace(']', '').strip().replace(' ', '').split(',')
        lat, lon = data[0], data[1]
        return lat, lon
    except Exception as e:
        return 0,0

def run(address):
    try:
        res=fetch(address).json()
        lat, lon=parse(res)
        return lat, lon
    except Exception as e:
        return 0,0

#function: locationProfile
#Description: View that returns the Location Profile like address, movements and stocks available
@app.route('/inventoryAdmin/locations/<int:id>')
def locationProfile(id):
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    location = Location.query.get_or_404(id)
    adminHome = AdminUser.query.filter_by(email=session['email']).all()
    AdminAddress = adminHome[0].address
    LocAddress = location.address
    lat1, lon1=run(AdminAddress)
    lat2, lon2=run(LocAddress)
    
    place1=(lon1, lat1)
    place2=(lon2, lat2)
    
    dis=distance.distance(place1, place2)
    distA = round(inspect.getmembers(dis)[1][1],2)
    speed=80
    hours=12
    distanceDay = speed*hours
    try:
        Days = int(distA/distanceDay)
    except:
        Days = 0 
    if(distA == 0.0 or place1==(0.0, 0.0) or place2==(0.0, 0.0)):
        distA = 'Unable to Fetch'
        Days = 'N/A'

    locationMovementsTo = Movement.query.filter_by(to_location_id=id).all()
    locationMovementsFrom = Movement.query.filter_by(from_location_id=id).all()
    return render_template('inventoryAdmin/locationProfile.html',location=location, lmt=locationMovementsTo, lmf=locationMovementsFrom, distance=distA, days=Days)

#function: status
#Description: View that returns the status of activities completed by the Admin Head
@app.route('/inventoryAdmin/status')
def status():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    date=datetime.datetime.now().date()
    dateX=date.strftime('%d/%m/%Y')
    

    Locations = Location.query.all()
    Products = Product.query.all()

    countDictionary={'lCount':['Locations Registered',Location.query.count()], 
    'catCount': ['Categories Added', Category.query.count()],
    'bCount' : ['Brands Added', Brand.query.count()],
    'pCount' : ['Products Added', Product.query.count()],
    'mCount' : ['Movements so far', Movement.query.count()],
    'oCount' : ['Orders Pending', LocationOrder.query.filter_by(status='Pending').count()]}

    status_list = []

    for location in Locations:
        for product in Products:
            row = {}
            row["location"] = location.name
            row["product"] = product.name
            row["quantity"] = available_quantity(location.id,product.id)
            if row["quantity"]<0:
                row["quantity"]=0
            status_list.append(row)

    products=[]
    quants=[]
    for i in Products:
        products.append(i.name)
        quants.append(i.stock)


    line_chart = pygal.Bar()
    line_chart.title = 'Stock Availability'
    line_chart.x_labels = products
    line_chart.add('Products',quants)
    line_chart = line_chart.render_data_uri()


    locIntDict={}
    for i in range(len(Locations)):
        countsFrom=Movement.query.filter_by(from_location_id=Locations[i].id).count()
        locIntDict[Locations[i].name] = locIntDict.get(Locations[i].name, 0)+countsFrom
        countsTo=Movement.query.filter_by(to_location_id=Locations[i].id).count()
        locIntDict[Locations[i].name] = locIntDict.get(Locations[i].name, 0)+countsTo

    interactiveSums=sum(locIntDict.values())

    pie_chart = pygal.Pie()
    pie_chart.title = 'Location wise Interaction (in %)'
    exc=1
    for key, value in locIntDict.items():
        try:
            pie_chart.add(key, round((value/interactiveSums)*100,2))
            exc=0
        except ZeroDivisionError as e:
            exc=1

    pie_chart = pie_chart.render_data_uri()

    movementDict={}
    MovX = Movement.query.all()
    for i in range(len(MovX)):
        date=MovX[i].curr_time.date()
        date=date.strftime('%d/%m/%Y')
        movementDict[date]=movementDict.get(date, 0)+1
        
    graph = pygal.Line()
    graph.title = 'Daily Movement Track Record'
    graph.x_labels = movementDict.keys()
    graph.add('Movements',  movementDict.values())
    
    graph = graph.render_data_uri()


    return render_template('inventoryAdmin/status.html',exc=exc, dateX=dateX, status_list=status_list, cD=countDictionary, line_chart=line_chart, pie_chart=pie_chart, graph=graph)

#function: get_pdf
#Description: creates a pdf and downloads the status report
@app.route('/inventoryAdmin/status', methods=['POST'])
def get_pdf():
    if 'email' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    if request.method=='POST':
        date=datetime.datetime.now()
        dateX=date.strftime('%d/%m/%Y')


        Locations = Location.query.all()
        Products = Product.query.all()

        countDictionary={'lCount':['Locations Registered',Location.query.count()], 
        'catCount': ['Categories Added', Category.query.count()],
        'bCount' : ['Brands Added', Brand.query.count()],
        'pCount' : ['Products Added', Product.query.count()],
        'mCount' : ['Movements so far', Movement.query.count()],
        'oCount' : ['Orders Pending', LocationOrder.query.filter_by(status='Pending').count()]}

        status_list = []

        for location in Locations:
            for product in Products:
                row = {}
                row["location"] = location.name
                row["product"] = product.name
                row["quantity"] = available_quantity(location.id,product.id)
                if row["quantity"]<0:
                    row["quantity"]=0
                status_list.append(row)

        products=[]
        quants=[]
        for i in Products:
            products.append(i.name)
            quants.append(i.stock)


        line_chart_data = {}
        for product in Products:
            line_chart_data[product.name]=product.stock


        locIntDict_data={}
        for i in range(len(Locations)):
            countsFrom=Movement.query.filter_by(from_location_id=Locations[i].id).count()
            locIntDict_data[Locations[i].name] = locIntDict_data.get(Locations[i].name, 0)+countsFrom
            countsTo=Movement.query.filter_by(to_location_id=Locations[i].id).count()
            locIntDict_data[Locations[i].name] = locIntDict_data.get(Locations[i].name, 0)+countsTo
        
        exc=1
        interactiveSums=sum(locIntDict_data.values())
        for key, value in locIntDict_data.items():
            try:
                locIntDict_data[key]=round((value/interactiveSums)*100,2)
                exc=0
            except ZeroDivisionError as e:
                exc=1

        movementDict_data={}
        MovX = Movement.query.all()
        for i in range(len(MovX)):
            date=MovX[i].curr_time.date()
            date=date.strftime('%d/%m/%Y')
            movementDict_data[date]=movementDict_data.get(date, 0)+1



        x='name'
        rendered = render_template('inventoryAdmin/pdf.html',exc=exc, dateX=dateX,status_list=status_list, cD=countDictionary, line_chart_data=line_chart_data, locIntDict=locIntDict_data, movementDict=movementDict_data)
        pdf = pdfkit.from_string(rendered, 'Status.pdf', configuration=config, options=kitoptions)
    return redirect(url_for('status'))

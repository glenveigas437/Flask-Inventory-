from flask import redirect, render_template, url_for, flash, request, session
from inventoryShop import db, app
from inventoryShop.products.models import Product

#Function: MergeDicts
#Description: used to add multiple products to the cart
#Returns: Merged List/Dictionaries of Multiple items selected
def MergeDicts(dict1, dict2):
	if isinstance(dict1, list) and isinstance(dict2, list):
		return dict1+dict2
	elif isinstance(dict1, dict) and isinstance(dict2, dict):
		return dict(list(dict1.items())+list(dict2.items()))
	return False

#Function: addCart 
#Description: Feature to add requested products to the cart
@app.route('/addCart', methods=['POST'])
def addCart():
	try:
		product_id = request.form.get('product_id')
		quantity = request.form.get('quantity')
		quantity = int(quantity)
		product = Product.query.filter_by(id=product_id).first()
		if(product_id and quantity and request.method=='POST'):
			DictItems={product_id:{'name':product.name, 'quantity':quantity, 'image':product.image1}}

			if 'requestCart' in session:
				if(product_id in session['requestCart']):
					for key, item in session['requestCart'].items():
						if int(key) == int(product_id):
							session.modified = True
							item['quantity']+=1
				else:
					session['requestCart']=MergeDicts(session['requestCart'], DictItems)
					return redirect(request.referrer)
			else:
				session['requestCart']=DictItems
				return redirect(request.referrer)

	except Exception as e:
		print(e)
	finally:
		return redirect(request.referrer)

#Function: getCart
#Description: Returns a view of the cart
@app.route('/carts')
def getCart():
	if 'requestCart' not in session:
		return redirect(request.referrer)
	return render_template('/products/carts.html')

#Function: clearcart
#Description: Makes the cart empty
@app.route('/clearcart')
def clearcart():
	try:
		session.clear()
		return redirect(url_for('home'))
	except Exception as e:
		print(e)

#Function: updatecart
#Description: Updates single item in the cart
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
	if 'requestCart' not in session or len(session['requestCart'])<=0:
		return redirect(url_for('home'))
	if request.method=='POST':
		quantity = request.form.get('quantity')
		try:
			session.modify = True
			for key, item in session['requestCart'].items():
				if(int(key)==code):
					item['quantity']=quantity
					flash('Item is updated', 'success')
					return redirect(url_for('getCart'))
		except Exception as e:
			print(e)
			return redirect(url_for('getCart'))

#Function: deleteitem
#Description: Deletes one item from the cart
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'requestCart' not in session or len(session['requestCart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['requestCart'].items():
            if int(key) == id:
                session['requestCart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
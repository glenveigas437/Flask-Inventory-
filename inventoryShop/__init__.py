from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from flask_msearch import Search
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'f5ebbb5f1c054f3c2e8317cb0eba2d25'
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir, 'static/images')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='Locationlogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u'Please Login first'
 

from inventoryShop.inventoryAdmin import routes
from inventoryShop.products import routes
from inventoryShop.cart import routes
from inventoryShop.locations import routes
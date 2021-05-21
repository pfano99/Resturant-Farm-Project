from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
import os

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@localhost/Farmers_db'.format(USERNAME, PASSWORD)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_POST'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('APP_MAIL')
app.config['MAIL_PASSWORD'] = os.getenv('APP_PASSWORD')


loginmanager = LoginManager(app)
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin = Admin(app, name="Lets Work")

from Work.Main.routes import main
from Work.Farmer.routes import farmer
from Work.Auth.routes import auth 
from Work.Product.routes import prod
from Work.Messaging.routes import chat
from Work.Resturants.routes import rest
from Work.Map.routes import map 

app.register_blueprint(main)
app.register_blueprint(farmer)
app.register_blueprint(prod)
app.register_blueprint(auth)
app.register_blueprint(chat)
app.register_blueprint(rest)
app.register_blueprint(map)


loginmanager.login_view = 'Auth.user_login'
loginmanager.login_message_category = 'info'

from Work.models import *

# admin.add_view(AdminModelView(Farmer, db.session))
# admin.add_view(AdminModelView(Service, db.session))
# admin.add_view(AdminModelView(Service_category, db.session))
# admin.add_view(AdminModelView(Address, db.session))


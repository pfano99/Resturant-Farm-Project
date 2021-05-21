from Work import db, loginmanager, app
from datetime import datetime
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import abort, session
from sqlalchemy import and_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@loginmanager.user_loader
def load_user(id):
    if session['account_type'] == 'restuarant':
        return Restuarant.query.get(id)
    elif session['account_type'] == 'farmer':
        return Farmer.query.get(id)


class Farmer(db.Model, UserMixin):
    __tablename__ = "farmer"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(170), nullable = False, unique=True)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    about_me = db.Column(db.Text, nullable = True)
    telephone = db.Column(db.String(10), nullable = True, unique = True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    profile_picture = db.Column(db.String(60), nullable = False, default = 'default.jpeg')
    gender = db.Column(db.String(6), nullable = False) 
    password = db.Column(db.String(60), nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False, default=False)
    offer_services = db.Column(db.Boolean, nullable = False, default = False)
    joindate = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_type = db.Column(db.Boolean, nullable = False, default=0) #this is to determne if the user, is a restuarant(1), or not(0=user)

    product = db.relationship('Product', backref='farmer', lazy=True)
    address = db.relationship('Address', backref='farmer', lazy=True)

    cart_client = db.relationship('Cart', foreign_keys='Cart.client_id', backref='client', lazy='dynamic')
    cart_seller = db.relationship('Cart', foreign_keys='Cart.seller_id', backref='seller', lazy='dynamic')

    message_send = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    message_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    last_read_time = db.Column(db.DateTime)

    # reviews new approach
    reviewer = db.relationship('Reviews', foreign_keys='Reviews.reviewer', backref='reviewer_', lazy='dynamic')
    reviews = db.relationship('Reviews', foreign_keys='Reviews.reviewed', backref='reviewed_', lazy='dynamic')

    def new_messages(self,):
        last_read_time = self.last_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient = self).filter(Message.timestamp > last_read_time).count()

    def exist_in_cart(self, seller_id, user_type):
        #This check if the seller exist in the cart.. return true if they exist or false if not
        if user_type == 0:
            return Cart.query.filter(and_(Cart.seller_id == seller_id, Cart.client_id == self.id)).count() > 0
        else:
            return Cart.query.filter(and_(Cart.rest_seller_id == seller_id, Cart.client_id == self.id)).count() > 0

    def add_to_cart(self, seller_id, user_type):
        if self.exist_in_cart(seller_id, user_type):
            # this will check if the user(service provider) is already added to the cart
            return False
        else:
            if user_type == 0:
                farmer = Cart(
                    client_id = self.id,
                    seller_id = seller_id
                )
            else:
                farmer = Cart(
                    client_id = self.id,
                    rest_seller_id = seller_id
                )
            db.session.add(farmer)
            db.session.commit()
            return True

    def delete_from_cart(self, seller_id, user_type):
        if self.exist_in_cart(seller_id, user_type):
            if user_type == 0:
                farmer = Cart.query.filter(and_(Cart.client_id == self.id, Cart.seller_id == seller_id)).first()
            else:
                farmer = Cart.query.filter(and_(Cart.client_id == self.id, Cart.rest_seller_id == seller_id)).first()

            db.session.delete(farmer)
            db.session.commit()

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'farmer_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_resert_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            farmer_id = s.loads(token)['farmer_id']
        except:
            return None  
        return Farmer.query.get(farmer_id)

    def __repr__(self,):
        return "First-Name: {}, Last-Name: {}, Email:{}".format(self.first_name, self.last_name, self.email)


class Restuarant(db.Model, UserMixin):
    __tablename__ = "restuarant"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(170), nullable = False, unique=True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False, unique=True)
    telephone = db.Column(db.String(10), nullable = False, unique=True)
    website = db.Column(db.String(250), nullable = True) 
    password = db.Column(db.String(60), nullable = False)
    date_joined = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_type = db.Column(db.Boolean, nullable = False, default=1) #this will be used to check if the user, is a restuarant(1), or not(0)
    profile_picture = db.Column(db.String(60), nullable = False, default = 'default.jpeg')

    message_send = db.relationship('Message', foreign_keys='Message.comp_sender_id', backref='restuarant_author', lazy='dynamic')
    message_received = db.relationship('Message', foreign_keys='Message.comp_recipient_id ', backref='restuarant_recipient', lazy='dynamic')
    last_read_time = db.Column(db.DateTime)

    #Cart
    cart_seller = db.relationship('Cart', foreign_keys='Cart.rest_seller_id ', backref='seller_restuarant', lazy='dynamic')
    cart_client = db.relationship('Cart', foreign_keys='Cart.rest_client_id ', backref='client_restuarant', lazy='dynamic')
    
    address = db.relationship('Address', backref='restuarant', lazy = True)

    #Reviews 
    reviewed = db.relationship('Reviews', foreign_keys='Reviews.reviewed_restuarant', backref='reviewed_comp', lazy='dynamic')
    reviewer = db.relationship('Reviews', foreign_keys='Reviews.reviewer_restuarant', backref='reviewer_comp', lazy='dynamic')

    def exist_in_cart(self, seller_id, user_type):
        #This check if the seller exist in the cart.. return true if they exist or false if not
        if user_type == 0:
            return Cart.query.filter(and_(Cart.seller_id == seller_id, Cart.rest_client_id == self.id)).count() > 0
        else:
            return Cart.query.filter(and_(Cart.comp_seller_id == seller_id, Cart.rest_client_id == self.id)).count() > 0
            
    def add_to_cart(self, seller_id, user_type):
        if self.exist_in_cart(seller_id, user_type):
            # this will check if the user(service provider) is already added to the cart
            return False
        else:
            if user_type == 0:
                user = Cart(
                    rest_client_id = self.id,
                    seller_id = seller_id
                )
            else:
                user = Cart(
                    rest_client_id = self.id,
                    rest_seller_id = seller_id
                )
            db.session.add(user)
            db.session.commit()
            return True

    def delete_from_cart(self, seller_id, user_type):
        if self.exist_in_cart(seller_id, user_type):
            if user_type == 0:
                user = Cart.query.filter(and_(Cart.rest_client_id == self.id, Cart.seller_id == seller_id)).first()
            else:
                user = Cart.query.filter(and_(Cart.rest_client_id == self.id, Cart.rest_seller_id == seller_id)).first()
            db.session.delete(user)
            db.session.commit()

    def __repr__(self,):
        return "Name: {}, Category: {}, Telephone: {}".format(self.name, self.email, self.telephone)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=True)
    stock_count = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable = False ) # apples, carrots, etc
    category = db.Column(db.String(100), nullable = False) #livestock, crops
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable = False)
    images = db.relationship('Images', backref='product', lazy = True)
    
    def __repr__(self,):
        return "Title: {}, Price: {}, Experience: {}".format(self.job_title, self.price, self.experience)


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('farmer.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('farmer.id'))
    rest_client_id = db.Column(db.Integer, db.ForeignKey('restuarant.id'))
    rest_seller_id = db.Column(db.Integer, db.ForeignKey('restuarant.id'))
    timestamp = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('farmer.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('farmer.id'))
    comp_sender_id = db.Column(db.Integer, db.ForeignKey('restuarant.id'))
    comp_recipient_id = db.Column(db.Integer, db.ForeignKey('restuarant.id'))
    body = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self,):
        return "Body: {}".format(self.body)


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    reviewed = db.Column(db.Integer, db.ForeignKey("farmer.id"))
    reviewed_restuarant = db.Column(db.Integer, db.ForeignKey("restuarant.id"))
    reviewer_restuarant = db.Column(db.Integer, db.ForeignKey("restuarant.id"))
    reviewer = db.Column(db.Integer, db.ForeignKey("farmer.id"))

    parent_id = db.Column(db.Integer, db.ForeignKey("reviews.id"))
    replies = db.relationship('Reviews', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def add_replies(self, text):
        return Reviews(text=text, parent=self)

    def __repr__(self,):
        return "id: {}, body: {}, parent id: {}",format(self.id, self.body, self.parent_id )


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    suburb = db.Column(db.String(100), nullable = True)
    town = db.Column(db.String(100), nullable = True)
    city = db.Column(db.String(100), nullable = True)
    province = db.Column(db.String(13), nullable = False)
    streat_address = db.Column(db.String(100), nullable = True)
    building_name = db.Column(db.String(100), nullable = True)
    
    latitude = db.Column(db.String(120), nullable=True)
    longtitude = db.Column(db.String(120), nullable=True)

    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable = True, unique=True)
    restuarant_id = db.Column(db.Integer, db.ForeignKey('restuarant.id'), nullable = True, unique=True)
    
    def __repr__(self,):
        return "Province: {}, Town: {},  Suburb: {}".format(self.province, self.town, self.suburb)


class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(13), nullable = False, unique = True)
    image = db.Column(db.String(60), nullable = True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable =False)

    @staticmethod
    def imgaes_limit(farmer_id):
        return Images.query.filter_by(farmer_id=farmer_id).count() > 5 

    def __repr__(self,):
        return "Name: {}, farmer-ID: {}".format(self.name, self.farmer_id)


class AdminModelView(ModelView):
    #Authorization and Authentication for flask-admin
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False
    
    def not_auth(self, name, **kwargs):
        abort(404)

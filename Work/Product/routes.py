from flask import Blueprint, session, render_template,flash, redirect, url_for, request, abort
from Work.Product.forms import ProductForm, AddressForm
from Work.models import Product, Address
from flask_login import current_user, login_required
from Work import db


prod = Blueprint('Product', __name__)

@prod.route('/services/registration/', methods=['POST', 'GET'])
@login_required
def add_product():
    title = "Add Products"
    form = ProductForm()
    
    if form.validate_on_submit():
        
        product = Product(
                price = form.price.data,
                stock_count = form.stock_count.data,
                product_name = form.product_name.data,
                category = str(form.category.data),             
                farmer_id = current_user.id
        )
        current_user.offer_services = True
        db.session.add(product)
        db.session.commit()

        flash("Successfully Created service", 'success')
        return redirect(url_for('Product.add_product'))
    return render_template("Product/product_add.html", form = form, title = title)



@prod.route('/address/', methods=['POST', 'GET'])
@login_required
def address_registration():
    title = "Address Registration"
    form = AddressForm()
    if form.validate_on_submit():

        streat_addr = None
        building_name = None

        if form.streat_address.data:  streat_addr = form.streat_address.data
        if form.building_name.data:  building_name = form.building_name.data

        address = Address(
            town = form.town.data,
            province = form.province.data,
            suburb = form.suburb.data,
            building_name = building_name,
            streat_address = streat_addr,
        )
        if current_user.user_type == 0:
            address.farmer_id = current_user.id 
        else:
            address.restuarant_id = current_user.id 

        db.session.add(address)
        db.session.commit()
        if current_user.user_type == 0:
            return redirect(url_for('Farmer.farmer_profile', username = current_user.username))
        else:
            return redirect(url_for('Restuarant.restuarant_profile', username = current_user.username))

    return render_template('Product/address.html', title = title, form=form)




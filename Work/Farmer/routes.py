from flask import Blueprint,render_template, redirect, url_for, request, abort, flash
from flask_login import current_user, login_required
from Work.models import Farmer, Product, Reviews, Restuarant
from Work.Utility.utils import SaveDocuments
from Work.Farmer.forms import UpdateFarmerProfile
from Work.Product.forms import ReviewForm
from Work import db
from sqlalchemy import and_

farmer = Blueprint('Farmer', __name__)


@farmer.route('/farmer/profile/<string:username>', methods=['POST', 'GET'])
@login_required
def farmer_profile(username):

    user = Farmer.query.filter_by(username=username).first_or_404()
    #this will return page not found if entered invalid username in the url.  
    #it will avoid having a blank page when username entered is not found 

    service = Product.query.filter_by(farmer_id=user.id).first()
    reviews = Reviews.query.filter(and_(Reviews.parent==None, Reviews.reviewed==user.id))

    address = user.address
    title = "{}'s profle".format(user.first_name)

    form = UpdateFarmerProfile()
    if current_user == user:
        if request.method =='GET':
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.email.data = user.email
            if user.about_me: form.about_me.data = user.about_me
            if user.telephone: form.telephone.data = user.telephone

        elif request.method =='POST':
            if form.validate_on_submit():
                if form.profile_picture.data:
                    print('picture form has data')
                    current_user.profile_picture = SaveDocuments.save_profile_picture( form_picture = form.profile_picture.data)


                if form.telephone.data:
                    current_user.telephone = form.telephone.data

                current_user.email = form.email.data
                current_user.first_name = form.first_name.data
                current_user.last_name = form.last_name.data
                current_user.about_me = form.about_me.data
                
                db.session.commit()
                flash('Profile is Seccessfully Updated ', 'success')
                return redirect(url_for('Farmer.farmer_profile', username=current_user.username))
    return render_template('Farmer/farmer_profile.html', form=form, user=user, service=service, address=address, reviews=reviews, title = title)


@farmer.route('/farmer/dashboard/<string:username>', methods=['POST', 'GET'])
@login_required
def farmer_dashboard(username):
    user = Farmer.query.filter_by(username=username).first()
    if not user and current_user != user:
        abort(404)
    
    title = "{}'s DashBoard".format(user.first_name)
    return render_template('Farmer/farmer_dashboard.html', user=user,
     title = title)
    

@farmer.route('/farmer/review/<string:username>/<int:parent_id>/<int:user_type>/', methods=['GET', 'POST'])
@login_required
def farmer_review(username, user_type, parent_id=None):
    # The user type tell which user is being reviewed, either a company or user.
    if user_type == 0:
        user = Farmer.query.filter_by(username=username).first_or_404()
    elif user_type == 1:
        company = Restuarant.query.filter_by(username=username).first_or_404()
    else:
        # if user_type is not one or zero, means url is not legit
        abort(404)

    
    title = "Review Page"
    form = ReviewForm()
    if form.validate_on_submit():
        if parent_id == 0:
            parent_id=None

        if user_type == 0 and current_user.user_type == 0:
            review = Reviews(reviewer=current_user.id,
                            reviewed=user.id, body= form.body.data, parent_id=parent_id)
        
        elif user_type == 0 and current_user.user_type == 1:
            review = Reviews(reviewer_company=current_user.id,
                            reviewed=user.id, body= form.body.data, parent_id=parent_id)
        
        elif user_type == 1 and current_user.user_type == 1:
            review = Reviews(reviewer_company=current_user.id,
                            reviewed_company=company.id, body= form.body.data, parent_id=parent_id)
        else:
            review = Reviews(reviewer=current_user.id,
                            reviewed_company=company.id, body= form.body.data, parent_id=parent_id)
            
        db.session.add(review)
        db.session.commit()
        flash('Your review is submitted', 'info')
        if user_type == 0:
            return redirect(url_for('Farmer.farmer_profile', username = username ))
        else:
            return redirect(url_for('Company.company_profile', username = username ))

    return render_template('Product/review.html', title=title, form=form)


@farmer.route('/farmer/cart/add/<int:seller_id>/<int:user_type>/', methods=['GET', 'POST'])
@login_required
def add_to_cart(seller_id, user_type):
    if user_type != 0 and user_type != 1:
        flash('Failed to add user to cart.', 'warning')
        return redirect(url_for('Main.home'))
    current_user.add_to_cart(seller_id, user_type)
    return redirect(url_for('Main.home'))
    

@farmer.route('/farmer/cart/delete/<int:seller_id>/<int:user_type>/', methods=['GET', 'POST'])
@login_required
def delete_from_cart(seller_id, user_type):
    if user_type != 0 and user_type != 1:
        flash('Failed to remove user from cart.', 'warning')
        return redirect(url_for('Main.home'))
    current_user.delete_from_cart(seller_id, user_type)
    return redirect(url_for('Main.home'))
    








from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import current_user, login_required
from Work.models import Farmer, Product
from Work.Product.forms import FilterSearchForm, AdvancedSearchForm
from sqlalchemy import or_, and_, text


main = Blueprint('Main', __name__)


@main.route('/')
def index():
    title = "LetsWork"
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    return render_template('Main/index.html', title=title)
    

@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    title = "LetsWork"
    page = request.args.get('page', 1, type=int)
    farmers = Farmer.query.paginate(page=page, per_page=12)

    if request.method == 'POST':
        data = request.form.get('query')
        return redirect(url_for('Main.search_results', values = data))
    return render_template('Main/home.html', farmers=farmers, title=title)


@main.route('/search/<string:values>', methods = ['GET', 'POST'])
@login_required
def search_results(values:None):
    
    title = "{} results".format(values)
    page = request.args.get('page', 1, type=int)

    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(or_(Product.product_name.like("%{}%".format(values)))).paginate(page=page, per_page=12)

    if not products:
        return "<h3>Nothing was Found</h3>"

    form = AdvancedSearchForm()
    # services = None
    if form.validate_on_submit():
        min_price, max_price, min_stock = 0, 9999999, 1
        if form.min_stock: min_stock= form.min_stock.data 
        if form.min_price: min_price = form.min_price.data 
        if form.max_price: max_price = form.max_price.data
        product_name = form.product_name.data

        products = Product.query.filter(and_(Product.stock_count >= min_stock, Product.product_name.like("%{}%").format(product_name), Product.price >= min_price, Product.price <=max_price ))
        
        return render_template('search_result.html', title = title,form=form, products = products)
        
    return render_template('search_result.html', title = title,form=form, products = products)


@main.route('/search/', methods = ['GET', 'POST'])
@login_required
def advanced_search():
    title = "search"
    form = AdvancedSearchForm()
    services = None
    if form.validate_on_submit():
        pass
    # location[province, radius(km)], product_name, product_price, Product_category
    # select 
    # from address a, product p, farmer f
    # where a.farmer_id == f.id
    # and 

    # products = Product.query.filter( or_( Product.category.like("%{}%".format( values )), 
    #         Product.job_title.like("%{}%".format( values )),Product.skills.like("%{}%".format( values )),
    #         Product.qualifications.like("%{}%".format( values )) ) ).paginate(page=page, per_page=8)
    min_price, min_stock, max_price = 0, 0, 0
    product_name = ""

    # products = Product.query.filter(and_(Product.stock_count >= min_stock, Product.product_name.like("%{}%").format(product_name), Product.price >= min_price, Product.price <=max_price ))
    # products = Product.query.filter(and_(Product.stock_count >= min_stock)) #, Product.product_name.like("%{}%").format(product_name), Product.price >= min_price, Product.price <=max_price ))

    return render_template('search_result.html', title = title, form = form, services = services)


from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import current_user, login_required
from Work.models import Farmer, Product
from Work.Product.forms import FilterSearchForm, AdvancedSearchForm
from sqlalchemy import or_, and_, text


map = Blueprint('Map', __name__)


@map.route('/maps/')
def maps():
    # api = "AIzaSyDV2bOUGX28d0lnalwpl2MVmPHnM8w2jrc"
    return render_template('Maps/map.html')
    

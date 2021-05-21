from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import current_user, login_required
from Work.models import Reviews, Restuarant
from Work.Utility.utils import SaveDocuments
# from Work.Resturants.forms import UpdateUserProfile
from sqlalchemy import and_
from Work.Product.forms import ReviewForm
from Work import db


rest = Blueprint('Restuarant', __name__)


@rest.route('/restuarant/profile/<string:username>', methods=['POST', 'GET'])
@login_required
def restuarant_profile(username):
    restuarant = Restuarant.query.filter_by(username=username).first_or_404()
    reviews = Reviews.query.filter(and_(Reviews.parent==None, Reviews.reviewed_restuarant==restuarant.id))
    title="{}'s profile".format(restuarant.name)
    return render_template('Restuarant/restuarant_profile.html', restuarant=restuarant, reviews=reviews, title=title)

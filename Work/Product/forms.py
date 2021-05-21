from itertools import product
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import  DataRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
# from Work.models import Service_category


class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    price = StringField('Price per kg', validators=[DataRequired(), Length(min=1, max=7)])
    stock_count = IntegerField('Stock Count', validators=[DataRequired()])
    category = SelectField('Category', choices=(['Fruit', 'Vegetables', 'Meat']))
    submit = SubmitField('Submit')


class FilterSearchForm(FlaskForm):
    searched_word = StringField('Keyword', validators=[DataRequired(), Length(min=1, max=2)])
    sort_price = SelectField('Sort Price by', choices=([ 'Lowest to Highest', 'Highest to Lowest' ]))
    province = SelectField('Province', choices=( ['Eastern Cape', 'Free State', 'Gauteng', 'Kwazulu-Natal', 'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape', 'Western Cape']
    ))
    submit = SubmitField('Search')
    
class AdvancedSearchForm(FlaskForm):
    province = SelectField('Province', choices=( ['Eastern Cape', 'Free State', 'Gauteng', 'Kwazulu-Natal', 'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape', 'Western Cape']
    ))
    product_name = StringField('Product Name', validators=[DataRequired()])
    min_price = IntegerField('Minimum Price', validators=[Optional(strip_whitespace=True)])
    max_price = IntegerField('Maximum Price', validators=[Optional(strip_whitespace=True)])
    min_stock = IntegerField('Minimum Stock', validators=[Optional(strip_whitespace=True)])
    
    submit = SubmitField('Search')


class AddressForm(FlaskForm):
    suburb = StringField('Suburb', validators=[DataRequired(), Length(min=3, max=100)])
    town = StringField('Town', validators=[DataRequired(), Length(min=3, max=100)])
    streat_address = StringField('Streat address', validators=[Length(min=3, max=100), Optional(strip_whitespace=True)])
    building_name = StringField('Building Name', validators=[Length(min=3, max=100), Optional(strip_whitespace=True)])
    province = SelectField('Province', choices=( ['Eastern Cape', 'Free State', 'Gauteng', 'Kwazulu-Natal', 'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape', 'Western Cape']
    ))
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):

    body = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit Review')
    




from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from Work.models import Farmer


class FarmerRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    # location = StringField('Location', validators=[DataRequired()])
    gender = SelectField('Gender', choices=(['Female', 'Male']))
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        farmer = Farmer.query.filter_by(email = email.data).first()
        if farmer:
            raise ValidationError('Email already exist')
    
class UpdateFarmerProfile(FlaskForm):
    profile_picture = FileField('Profile picture', validators=[ FileAllowed(['jpg', 'png', 'jpeg'])])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    about_me = TextAreaField('About Me', validators=[Optional(strip_whitespace=True)])
    telephone = StringField('Telephone', validators=[ Length(min=10, max=10), Optional(strip_whitespace=True)])
    # profile_picture = 
    submit = SubmitField('Update')


    def validate_email(self, email):
        if current_user.email != email.data:
            farmer = Farmer.query.filter_by(email = email.data).first()
            if farmer:
                raise ValidationError('Email already exist')




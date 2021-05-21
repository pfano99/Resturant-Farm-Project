from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from Work.models import Company


# class CompanyRegistrationForm(FlaskForm):
#     name = StringField('Company Name', validators=[DataRequired(), Length(min=3, max=150)])
#     email = StringField('Email', validators=[DataRequired(), Email()]) 
#     company_reg_no = StringField('Company Registration Number', validators=[DataRequired(), Length(min=13, max=13)])
#     password = PasswordField('Password', validators=[DataRequired()]) 
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Submit')

#     def validate_email(self, email):
#         company = Company.query.filter_by(email = email.data).first()
#         if company:
#             raise ValidationError('Email already exist')
    

# class UpdateCompanyProfile(FlaskForm):
#     profile_picture = FileField('Profile picture', validators=[ FileAllowed(['jpg', 'png', 'jpeg'])])
#     first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=100)])
#     last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=100)])
#     email = StringField('Email', validators=[DataRequired(), Email()]) 
#     about_me = TextAreaField('About Me', validators=[Optional(strip_whitespace=True)])
#     telephone = StringField('Telephone', validators=[ Length(min=10, max=10), Optional(strip_whitespace=True)])
#     id_number = StringField('Identity Number', validators=[ Length(min=13, max=13), Optional(strip_whitespace=True)])
#     # profile_picture = 
#     submit = SubmitField('Update')


#     def validate_email(self, email):
#         if current_user.email != email.data:
#             user = User.query.filter_by(email = email.data).first()
#             if user:
#                 raise ValidationError('Email already exist')




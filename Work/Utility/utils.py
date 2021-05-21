import os
import secrets
import random
from flask import session, abort, redirect, url_for
from Work.models import Farmer
from Work import app

            
class SaveDocuments:
    @staticmethod
    def _save_in_directory(form_picture, sub_folder):
        random_name = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fullname = random_name + f_ext
        picture_path = os.path.join(app.root_path, 'static/{}'.format(sub_folder), picture_fullname)
        form_picture.save(picture_path)
        return picture_fullname
    @staticmethod
    def save_profile_picture(form_picture):
        picture_fullname = SaveDocuments._save_in_directory(form_picture, 'profile_pictures')
        return picture_fullname
    @staticmethod    
    def save_post_picture(self, form_picture):
        picture_fullname = SaveDocuments._save_in_directory(form_picture, 'post_pictures')
        return picture_fullname


def format_email(email):
    email = email.lower()
    email = email.lstrip()
    email = email.rstrip()
    return email

def generate_username(fname, lname=None):
    count = Farmer.query.count()
    count = count + random.randint(99, 900)
    if lname:
        username = "{}{}{}".format(fname, lname, count)
    else:
        username = "{}{}".format(fname, count)
    return username


def service_registered(func):
    #  This decorator will check if the Worker or Organization has already registered their Services
    # if they haven't register their services they will be rdirected to service registration page.
    #  The decorator will only be used on certain pages after the user(Worker|Organization) is logged in
    def wrapper(*args, **kwargs):
        if 'is_registered' in session:
            if  session['is_registered'] == 'False':
                return redirect(url_for('Service.register_services'))
            elif session['is_registered'] == 'True':
                f = func(*args, **kwargs)
                return f
            else:
                # if there is is_registered session on the browser but the value is not True or false
                # Something went wrong either someone tried to change the session value
                return abort(400)
        else:
            return abort(400)
    return wrapper



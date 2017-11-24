from flask import Flask, render_template
from flask_admin import Admin
from lib.http import BaseView
from flask_login import login_required, login_user
from database import init_db
import packages


app = Flask(__name__)
# wwhat is an admin? it is a flask_admin concept, why is it needed?
# what is template_mode?
admin = Admin(app, name="endpoint", template_mode="bootstrap3")


def init():
    app.config.from_object("endpoint.default_config")
    app.config.from_pyfile("endpoint.cfg", silent=True)
    # init_db calls db.init_app(app) which uses flask_sqlalchemy
    init_db(app)
    # what is packages? it is a funciton that wraps
    # importing the public, user, and twilio packages
    # the app and admin params are passed in to the 
    # init funcs of each packages - see endpoint/packages/__init__.py
    packages.init(app, admin)

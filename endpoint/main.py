from flask import Flask, render_template
from flask_admin import Admin
from lib.http import BaseView
from flask_login import login_required, login_user
from database import init_db
import packages


app = Flask(__name__)
admin = Admin(app, name="endpoint", template_mode="bootstrap3")


def init():
    app.config.from_object("endpoint.default_config")
    app.config.from_pyfile("endpoint.cfg", silent=True)
    init_db(app)
    packages.init(app, admin)

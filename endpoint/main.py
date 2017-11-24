from flask import Flask, render_template
from flask_admin import Admin
from lib.http import BaseView
from flask_login import login_required, login_user
from endpoint.data_backends import DataLayer
import packages


app = Flask(__name__)


def init():
    app.config.from_object("endpoint.default_config")
    app.config.from_pyfile("endpoint.cfg", silent=True)
    DataLayer.load_api(app.config["DATASTORE"])
    DataLayer.init(app)
    packages.init(app)

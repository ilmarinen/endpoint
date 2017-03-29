from flask import Flask, render_template
from lib.http import BaseView
from flask.ext.login import login_required, login_user
from database import init_db
import packages


app = Flask(__name__)


def init():
    app.config.from_object('endpoint.default_config')
    init_db(app)
    packages.init(app)


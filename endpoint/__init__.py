import os
import click
import jinja2
from datetime import datetime
from flask import Flask, request, send_from_directory, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from endpoint.config import Config
from endpoint.lib.http import APIException

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from endpoint.models import models
from endpoint.blueprints import users, restaurants, google_auth, github_auth, twilio

basedir = os.path.abspath(os.path.dirname(__file__))

app.register_blueprint(users.rest_bp, url_prefix='/api')
app.register_blueprint(restaurants.rest_bp, url_prefix='/api')
app.register_blueprint(twilio.bp, url_prefix='/twilio')
app.register_blueprint(google_auth.bp)
app.register_blueprint(github_auth.bp)

admin = Admin(app, name="endpoint", template_mode="bootstrap3")
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.TwilioAccount, db.session))


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(basedir, '/static'), path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(basedir, 'static'), 'favicon.ico')


@login_required
@app.route('/uploads', methods=["POST"])
def uploads():
    if "file" not in request.files:
        raise APIException(403, "No files")
    file = request.files["file"]
    if file.filename == "":
        raise APIException(403, "No files selected")

    filename = "{}-{}.jpg".format(current_user.username, str(datetime.utcnow().timestamp()))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    current_user.profile_filename = filename
    db.session.add(current_user)
    db.session.commit()

    return "uploads/{}".format(filename)


@login_required
@app.route('/uploads/<path:path>')
def get_uploads(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', selected_tab="LOGIN")


@app.route('/signup')
def user_signup():
    return render_template('index.html', selected_tab="SIGNUP")


def gen_fixtures():
    from endpoint.models import api

    owners_groups = models.Group.query.filter_by(groupname="restaurant_owners")
    admin_groups = models.Group.query.filter_by(groupname="admins")
    if owners_groups.count() == 0:
        restaurant_owners = models.Group(groupname="restaurant_owners")
        db.session.add(restaurant_owners)
        db.session.commit()

    if admin_groups.count() == 0:
        admins = models.Group(groupname="admins")
        admin_user = models.User(username="admin")
        admin_user.password = "admin"
        admin_user.is_active = True
        db.session.add(admins)
        db.session.add(admin_user)
        db.session.flush()
        admins_membership = models.Membership(user_id=admin_user.id, group_id=admins.id)
        db.session.add(admins_membership)
        db.session.commit()

    user_a = api.create_user("jack", "Jack", "EinstSpratein", "t@test.com", restaurant_owner=False, is_active=True, password="test")
    user_b = api.create_user("john", "John", "Doe", "j@test.com", restaurant_owner=True, is_active=True, password="test")
    db.session.add(user_a)
    db.session.add(user_b)
    db.session.commit()


@app.cli.command("generate-fixtures")
def generate_fixtures():
    gen_fixtures()


@app.cli.command("generate-deployment-configs")
@click.option("--host", "-h")
@click.option("--application-root", "-r")
@click.option("--docker", "-d", is_flag=True)
def generate_deployment_configs(host, application_root, docker):
    nginx_site_template_file = "../deployment/nginx-config/endpoint-site"
    systemd_unit_template_file = "../deployment/systemd-unit/endpoint.service"
    with open("./deployment/nginx-config/endpoint-site", "r") as nginx_site_template_file:
        nginx_site_template = jinja2.Template(nginx_site_template_file.read())
    nginx_site_text = nginx_site_template.render(host_name=host, endpoint_root=application_root)

    with open("./deployment/systemd-unit/endpoint.service", "r") as systemd_unit_template_file:
        systemd_unit_template = jinja2.Template(systemd_unit_template_file.read())
    systemd_unit_text = systemd_unit_template.render(endpoint_root=application_root)

    with open("./deployment/uwsgi-config/endpoint.ini", "r") as endpoint_ini_template_file:
        endpoint_ini_template = jinja2.Template(endpoint_ini_template_file.read())
    endpoint_ini_text = endpoint_ini_template.render(docker=docker)

    with open("./deployment/endpoint-site", "w") as nginx_site_file:
        nginx_site_file.write(nginx_site_text)

    with open("./deployment/endpoint.service", "w") as systemd_unit_file:
        systemd_unit_file.write(systemd_unit_text)

    with open("./deployment/endpoint.ini", "w") as endpoint_ini_file:
        endpoint_ini_file.write(endpoint_ini_text)

    print("Created the Nginx site config: endpoint-site")
    print("Created the Systemd unit: endpoint.service")
    print("Both files were saved under the deployment folder.")
    print("Copy the endpoint-site file to /etc/nginx/sites-available/")
    print("Create a symlink to it under /etc/nginx/sites-enabled/")
    print("Copy the endpoint.service file to /etc/systemd/system/")
    print("Start the endpoint service with: sudo service endpoint start")

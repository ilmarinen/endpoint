import functools
import os
import flask
from flask import render_template
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
from endpoint.lib.http import no_cache
from endpoint.models import api
from flask_login import login_user
import requests
from datetime import datetime


ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'

AUTH_REDIRECT_URI = "http://endpoint.zay.io:5000/oauth2callback"
BASE_URI = "http://endpoint.zay.io:5000"
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", default=False)

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

bp = flask.Blueprint('google_auth', __name__, template_folder="templates")


def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False


def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
    
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)


def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()


@bp.route('/google/login')
@no_cache
def login():
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)
  
    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return flask.redirect(uri, code=302)


@bp.route('/oauth2callback')
@no_cache
def google_auth_redirect():
    req_state = flask.request.args.get('state', default=None, type=None)

    if req_state != flask.session[AUTH_STATE_KEY]:
        response = flask.make_response('Invalid state parameter', 401)
        return response
    
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens
    
    user_info = get_user_info()
    firstname = user_info.get("given_name")
    lastname = user_info.get("family_name")
    email = user_info.get("email")
    username = email
    profile_picture_url = user_info.get("picture")

    user_by_email = api.get_user_by_email(email)

    if user_by_email is not None and user_by_email.external_auth != "google":
        return render_template("error.html", error="Email address already in use.")
    elif user_by_email is not None and user_by_email.external_auth == "google":
        result = login_user(user_by_email)
        return flask.redirect(BASE_URI, code=302)

    resp = requests.get(profile_picture_url)
    filename = "{}-{}.jpg".format(username, str(datetime.utcnow().timestamp()))
    from endpoint import app
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as file:
        file.write(resp.content)
    user = api.create_user(username, firstname, lastname, email, profile_filename=filename, external_auth="google", is_active=True)
    login_user(user)

    return flask.redirect(BASE_URI, code=302)


@bp.route('/google/logout')
@no_cache
def logout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)

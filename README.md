# Endpoint

[![Build Status](https://travis-ci.org/ilmarinen/endpoint.svg?branch=master)](https://travis-ci.org/ilmarinen/endpoint)

## Installation

1. `python3 -m venv venv`

Then activate your virtual environment and then do.

1. `npm install`
2. `pip install -r requirements.txt`
3. `python setup.py develop`

## Initialize Database

1. `FLASK_APP=endpoint.py flask db init`
2. `FLASK_APP=endpoint.py flask db migrate -m "Create all tables etc."`
3. `FLASK_APP=endpoint.py flask generate-fixtures`

## Run Server

`GITHUB_CLIENT_ID='<github-oauth-client-id>' GITHUB_CLIENT_SECRET='<github-oauth-client-secret>' GOOGLE_CLIENT_ID='<google-oauth-client-id>' GOOGLE_CLIENT_SECRET='<google-oauth-client-secret>'  HOSTNAME=<hostname:port> SENDGRID_API_KEY=<sendgrid-api-key> ADMIN=<admin-email> FLASK_APP=endpoint.py flask run -h 0.0.0.0 -p 5000`

Add an entry to your `/etc/hosts` file pointing the hostname to the host ip address.

Then point your browser to `http://<hostname>:5000`

## Flask Shell

`FLASK_APP=endpoint.py flask shell`

## Development workflow - Migrations

1. Make changes to the SQLAlchemy models in the project.
2. Then create a migration with `FLASK_APP=endpoint.py flask db migrate -m "<description-of-migration>"`
3. Then apply the migration with`FLASK_APP=endpoint.py flask db upgrade`

## Deployment

The tightest way to deploy this is as a WSGI application with NGINX proxying the web requests to the WSGI application. The obvious choice for running the WSGI application is uWSGI (which is included in the requirements.txt as a dependency). The setup is very simple.

1. Create a user `endpoint` with home folder `/home/endpoint`
2. Clone the repo into `/home/endpoint/endpoint`
3. Within `/home/endpoint/endpoint` run `python3 -m venv venv`. This will create a virtual environment under `/home/endpoint/endpoint/venv`.
4. With the virtual environment activated, install all the requirements and run step.py to install endpoint.
5. Initialize the database and setup the admin user and groups. Setup any additional users and groups you may need.
6. Run `FLASK_APP=endpoint.py flask generate-deployment-configs -h test.com -r /home/code/endpoint`
7. Copy the file `deployment/endpoint.service` to `/etc/systemd/system/endpoint.service`
8. Copy the file `deployment/endpoint-site` to `/etc/nginx/sites-available/endpoint-site`
9. Chown the repo so that the user `www-data` can read and write to it: `chown -R www-data:www-data /home/endpoint/endpoint`
10. Create a symlink to activate the configuration `ln -s /etc/nginx/sites-available/endpoint-site /etc/nginx/sites-enabled/endpoint-site`
11. Start the endpoint service `sudo service endpoint start`
12. Reload the Nginx config `sudo service nginx reload`
13. Point your browser to `http://<hostname>` and you should see the Endpoint site working.
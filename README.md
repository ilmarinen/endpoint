# Endpoint


## Installaation

`python3 -m venv venv`

Then activate your virtual environment and then do.

`npm install`
`pip install -r requirements.txt`
`python setup.py develop`

## Initialize Database

`FLASK_APP=endpoint.py flask db init`
`FLASK_APP=endpoint.py flask db migrate -m "Create all tables etc."`

## Run Server

`GITHUB_CLIENT_ID='<github-oauth-client-id>' GITHUB_CLIENT_SECRET='<github-oauth-client-secret>' GOOGLE_CLIENT_ID='<google-oauth-client-id>' GOOGLE_CLIENT_SECRET='<google-oauth-client-secret>'  HOSTNAME=<hostname:port> SENDGRID_API_KEY=<sendgrid-api-key> ADMIN=<admin-email> FLASK_APP=endpoint.py flask run -h 0.0.0.0 -p 5000`

Add an entry to your `/etc/hosts` file pointing the hostname to the host ip address.

Then point your browser to http://<hostname>:5000

## Flask Shell

`FLASK_APP=endpoint.py flask shell`

## Development workflow - Migrations

1. `FLASK_APP=endpoint.py flask db migrate -m "<description-of-migration>"`
2. `FLASK_APP=endpoint.py flask db upgrade`

## Deployment

The tightest way to deploy this is as a WSGI application with NGINX proxying the web requests to the WSGI application. The obvious choice for running the WSGI application is uWSGI (which is included in the requirements.txt as a dependency). The setup is very simple.

1. Create a user `endpoint` with home folder `/home/endpoint`
2. Clone the repo into `/home/endpoint/endpoint`
3. Create a virtual environment. In `/home/endpoint` run `virtualenv -p /usr/bin/python2 vendpoint`
4. With the virtual environment activated, install all the requirements and run step.py to install endpoint.
5. Initialize the database and setup the admin user and groups. Setup any additional users and groups you may need.
6. Copy the file `wsgi/systemd-unit/endpoint.service` to `/etc/systemd/system/endpoint.service`
7. Copy the file `wsgi/nginx-config/endpoint-site` to `/etc/nginx/sites-available/endpoint-site`
8. Add a config file `endpoint.cfg` under `/home/endpoint/endpoint/endpoint` and declare values there to override values in the default config.
9. Chown the repo so that the user `www-data` can read and write to it: `chown -R www-data:www-data /home/endpoint/endpoint`
10. Change the variable `server_name your.hostname.com` to whatever hostname you want the server to run on.
11. Create a symlink to activate the configuration `ln -s /etc/nginx/sites-available/endpoint-site /etc/nginx/sites-enabled/endpoint-site`
12. Start the endpoint service `sudo service endpoint start`
13. Reload the Nginx config `sudo service nginx reload`

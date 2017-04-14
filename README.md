# Endpoint
## About
Endpoint is a barebones web server with a few dynamic templated pages and RESTful routes. It has basic user / group permissions implemented, and a token system for securely providing an endpoint for remote services to call. This is a very extensibe project which is also easily deployable.

## Introduction

### Installation
```
pip install -r requirements.txt
python setup.py develop
```

### Initialize Database
```
python manage.py init-db
alembic upgrade head
```
#### Create Users
```
python manage.py add-user --username admin --password 1234
python manage.py add-user --username joe --password 1234
```

#### Create Groups
```
python manage.py add-group --groupname admin
python manage.py add-group --groupname users
```

#### Add Users to Groups
```
python manage.py add-group-member --groupname admin --membername admin
python manage.py add-group-member --groupname users --membername joe
```

### Run the Development Server
```
python manage.py dev-server
```

Then point your browser to port 8000 on the machine where the server is running.

## Architecture

Endpoint is built atop Flask, which is a webserver (Werkzeug) together with various session management, middleware and other convenience helpers, that make writing a web back-end relatively easy. There are also a lot of Flask modulews out there which allow you to add functionality such as login / logout and session management logic (Flask-Login), as well as an administrative CRUD interface (Flask-Admin). What I like about Flask is that it is very lightweight, does not dictate project structure, and does not populate your project with auto-generated code.

The Endpoint project itself is composed of a set of data models implemented in SqlAlchemy, together with a set of packages that interface with the data models and implement some internal business logic. Each package implements its own views and routes. The views and routes are mapped to handlers which handle web requests and interface them with the business logic within the package and the data models.

[Alembic](http://alembic.zzzcomputing.com/en/latest/index.html) is used for managing database migrations. It works well with SqlAlchemy and is able to auto-generate migrations based on your SqlAlchemy models most of the time. The command to auto-generate a migration goes like:

```
$ alembic revision --autogenerate -m "Added account table"
INFO [alembic.context] Detected added table 'account'
Generating /path/to/foo/alembic/versions/27c6a30d7c24.py...done
```

It can then be used to upgrade to the latest migration by:

```
$ alembic upgrade head
```

It can be used to downgrade by:

```
$ alembic downgrade -1
```

## Deployment

The tightest way to deploy this is as a WSGI application with NGINX proxying the web requests to the WSGI application. The obvious choice for running the WSGI application is uWSGI (which is included in the requirements.txt as a dependency). The setup is very simple.

1. Create a user `endpoint` with home folder `/home/endpoint`
2. Clone the repo into `/home/endpoint/endpoint`
3. Create a virtual environment. In `/home/endpoint` run `virtualenv -p /usr/bin/python2 vendpoint`
4. With the virtual environment activated, instaqll all the requirements and run step.py to install endpoint.
5. Initialize the database and setup the admin user and groups. Setup any additional users and groups you may need.
6. Copy the file `wsgi/systemd-unit/endpoint.service` to `/etc/systemd/system/endpoint.service`
7. Copy the file `wsgi/nginx-config/endpoint-site` to `/etc/nginx/sites-available/endpoint-site`
8. Chown the repo so that the user `www-data` can read and write to it: `chown -R www-data:www-data /home/endpoint/endpoint`
9. Change the variable `server_name your.hostname.com` to whatever hostname you want the server to run on.
10. Create a symlink to activate the configuration `ln -s /etc/nginx/sites-available/endpoint-site /etc/nginx/sites-enabled/endpoint-site`
11. Start the endpoint service `sudo service endpoint start`
12 Reload the Nginx config `sudo service nginx reload`

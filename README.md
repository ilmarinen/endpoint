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

Endpoint built atop Flask, which is a webserver (Werkzeug) together with various session management, middleware and other convenience helpers, that make writing a web back-end relatively easy. There are also a lot of Flask modulews out there which allow you to add functionality such as login / logout and session management logic (Flask-Login), as well as an administrative CRUD interface (Flask-Admin). What I like about Flask is that it is very lightweight, does not dictate project structure, and does not populate your project with auto-generated code.

The Endpoint project itself is composed of a set of data models implemented in SqlAlchemy, together with a set of packages that interface with the data models and implement some internal business logic. Each package implements its own views and routes. The views and routes are mapped to handlers which handle web requests and interface them with the business logic within the package and the data models.
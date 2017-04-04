# Endpoint
## About

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

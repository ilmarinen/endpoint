# Endpoint
## Installation
```
pip install -r requirements.txt
python setup.py develop
```

## Initialize Database
```
python manage.py init-db
alembic upgrade head
```

## Run the Development Server
```
python manage.py dev-server
```

Then point your browser to port 8000 on the machine where the server is running.

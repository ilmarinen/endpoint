FROM python:3.6.5
RUN apt-get update && apt-get -y dist-upgrade

RUN pip install --upgrade pip==18.0
RUN pip install "uWSGI>=2,<3"

ADD . /var/www/endpoint
WORKDIR /var/www/endpoint
RUN pip install -r requirements.txt
RUN python setup.py develop
RUN FLASK_APP=endpoint.py flask db upgrade
RUN FLASK_APP=endpoint.py flask generate-fixtures
RUN FLASK_APP=endpoint.py flask generate-deployment-configs --host ~. --application-root /var/www/endpoint --docker
RUN cp deployment/endpoint.ini .
RUN chown -R www-data:www-data /var/www/endpoint

EXPOSE 5000

ENTRYPOINT ["uwsgi", "--ini", "endpoint.ini"]

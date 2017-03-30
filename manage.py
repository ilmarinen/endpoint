from opster import command, dispatch


@command()
def init_db():
    from endpoint.main import app, init
    from endpoint.database import db

    init()

    with app.app_context():
        db.create_all()


@command()
def dev_server(port=('p', 8000, 'Port'),
               host=('h', '0.0.0.0', 'Host address')):
    from endpoint import app, init
    from endpoint.lib import http

    init()

    http.expose_static_files(app)
    app.debug = True
    app.run(host=host, port=port)


if __name__ == '__main__':
    dispatch()

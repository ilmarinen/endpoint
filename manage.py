from opster import command, dispatch

# This file is a script for running commands
# it's a wrapper around functionality
# that instantiates an app, starts a db session
# and peforms a db operation or
# starts the server

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


@command()
def add_user(username=('u', '', 'Username'),
             firstname=('f', '', 'First name'),
             lastname=('l', '', 'Last name'),
             password=('p', '12345', 'Password')):
    from endpoint.main import app, init
    from endpoint.database import db
    from endpoint.packages.user.model import User

    init()

    with app.app_context():
        user = User(username=username,
                    first_name=firstname,
                    last_name=lastname,
                    password=password,
                    active=True)

        db.session.add(user)
        db.session.commit()


@command()
def add_group(groupname=('g', '', 'Group name'),
              description=('d', '', 'Group description')):
    from endpoint.main import app, init
    from endpoint.database import db
    from endpoint.packages.user.model import Group

    init()

    with app.app_context():
        group = Group(name=groupname,
                      description=description)

        db.session.add(group)
        db.session.commit()


@command()
def add_group_member(groupname=('g', '', 'Group name'),
                     membername=('m', '', 'Member username')):
    from endpoint.main import app, init
    from endpoint.database import db
    from endpoint.packages.user.model import Group, User

    init()

    with app.app_context():
        group = Group.query.filter(Group.name == groupname).first()
        user = User.query.filter(User.username == membername).first()
        group.members.append(user)

        db.session.add(group)
        db.session.commit()


if __name__ == '__main__':
    dispatch()

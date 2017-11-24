from opster import command, dispatch


@command()
def init_db():
    from endpoint.main import app, init

    init()

    from endpoint.packages.user import DataLayer

    with app.app_context():
        DataLayer.init_db()


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

    init()

    from endpoint.packages.user import DataLayer

    with app.app_context():
        if DataLayer.get_user_by_username(username):
            print "User {} already exists.".format(username)
            return
        user = DataLayer.create_user(username, password, firstname, lastname)
        print "Created user: {}".format(user.username)


@command()
def add_group(groupname=('g', '', 'Group name'),
              description=('d', '', 'Group description')):
    from endpoint.main import app, init

    init()

    from endpoint.packages.user import DataLayer

    with app.app_context():
        if DataLayer.get_group_by_groupname(groupname):
            print "Group {} already exists.".format(groupname)
            return
        group = DataLayer.create_group(groupname, description)
        print "Created group: {}".format(group.name)


@command()
def add_group_member(groupname=('g', '', 'Group name'),
                     membername=('m', '', 'Member username')):
    from endpoint.main import app, init
    from endpoint.packages.user import DataLayer

    init()

    with app.app_context():
        user = DataLayer.get_user_by_username(membername)
        if not user:
            print "User {} not found.".format(membername)

        group = DataLayer.get_group_by_groupname(groupname)
        if not group:
            print "Group {} not found.".format(groupname)

        group = DataLayer.add_group_member(membername, groupname)
        if not group:
            print "Failed to add user {} to group {}.".format(membername, groupname)
        else:
            print "Succeeded in adding user {} to group {}.".format(membername, group.name)


@command()
def create_admin(password=('p', '1234', "Admin password")):
    from endpoint.main import app, init
    from endpoint.packages.user import DataLayer

    init()

    with app.app_context():
        DataLayer.create_user("admin", password, "Admin", "User")
        DataLayer.create_group("admin", "Admin group")
        group = DataLayer.add_group_member("admin", "admin")
        if not group:
            print "Failed to create admin user."
        else:
            print "Successfully created admin user."


if __name__ == '__main__':
    dispatch()

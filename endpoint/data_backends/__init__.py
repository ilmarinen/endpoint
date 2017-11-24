import importlib


class DataLayer(object):
    api = None

    @classmethod
    def load_api(cls, module_name):
        cls.api = importlib.import_module("endpoint.data_backends.{}".format(module_name))

    @classmethod
    def init(cls, app):
        cls.api.init(app)

    @classmethod
    def init_db(cls):
        cls.api.init_db()

    @classmethod
    def get_user_by_username(cls, username):
        return cls.api.get_user_by_username(username)

    @classmethod
    def verify_user_password(cls, user, password):
        return cls.api.verify_user_password(user, password)

    @classmethod
    def get_user_by_id(cls, id):
        return cls.api.get_user_by_id(id)

    @classmethod
    def user_in_group(cls, user, group_name):
        return cls.api.user_in_group(user, group_name)

    @classmethod
    def list_users(cls, limit, offset):
        return cls.api.list_users(limit, offset)

    @classmethod
    def get_token_by_value(cls, value):
        return cls.api.get_token_by_value(value)

    @classmethod
    def create_user(cls, username, password, firstname, lastname):
        return cls.api.create_user(username, password, firstname, lastname)

    @classmethod
    def create_group(cls, groupname, description):
        return cls.api.create_group(groupname, description)

    @classmethod
    def get_group_by_groupname(cls, groupname):
        return cls.api.get_group_by_groupname(groupname)

    @classmethod
    def add_group_member(cls, username, groupname):
        return cls.api.add_group_member(username, groupname)

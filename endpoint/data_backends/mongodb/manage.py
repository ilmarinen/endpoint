from model import User, Group, Token
from endpoint.lib import crypto
import bson


def init_db():
    pass


def get_user_by_username(username):
    return User.objects(username=username).first()


def verify_user_password(user, password):
    hashed_user_password = user.password
    return crypto.verify_pass(password, hashed_user_password)


def get_user_by_id(id):
    if id == "1":
        return None
    id = bson.objectid.ObjectId(id)
    return User.objects.get(id=id)


def user_in_group(user, group_name):
    group = Group.objects(name=group_name).first()

    return group in user.groups


def list_users(limit, offset):
    return User.objects().limit(limit).skip(offset)


def get_token_by_value(value):
    return Token.objects(value=value).first()


def create_user(username, password, firstname, lastname):
    user = User(username=username,
                first_name=firstname,
                last_name=lastname,
                active=True)
    user.password = password
    user.save()

    return user


def create_group(groupname, description):
    group = Group(name=groupname,
                  description=description)
    group.save()

    return group


def get_group_by_groupname(groupname):
    return Group.objects(name=groupname).first()


def add_group_member(username, groupname):
    user = get_user_by_username(username)
    group = get_group_by_groupname(groupname)

    if user is None or group is None:
        return None

    if group.id not in user.groups:
        user.groups.append(group.id)
        user.save()

    return group

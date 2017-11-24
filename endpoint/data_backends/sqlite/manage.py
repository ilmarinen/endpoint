from model import User, Group, Token
from endpoint.lib import crypto
from database import db


def init_db():
    db.create_all()


def get_user_by_username(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        return None

    return user


def verify_user_password(user, password):
    hashed_user_password = user.password
    return crypto.verify_pass(password, hashed_user_password)


def get_user_by_id(id):
    return User.query.filter(User.id == id).first()


def user_in_group(user, group_name):
    user_groups = [group.name for group in user.groups]

    return (group_name in user_groups)


def list_users(limit, offset):
    return User.query.limit(limit).offset(offset).all()


def get_token_by_value(value):
    token = Token.query.filter(Token.value == value).first()
    if not token:
        return None

    return token


def create_user(username, password, firstname, lastname):
    user = User(username=username,
                first_name=firstname,
                last_name=lastname,
                password=password,
                active=True)

    db.session.add(user)
    db.session.commit()

    return user


def create_group(groupname, description):
    group = Group(name=groupname,
                  description=description)

    db.session.add(group)
    db.session.commit()

    return group


def get_group_by_groupname(groupname):
    group = Group.query.filter(Group.name == groupname).first()
    if not group:
        return None

    return group


def add_group_member(username, groupname):
    user = get_user_by_username(username)
    group = get_group_by_groupname(groupname)

    if not user or not group:
        return None

    group.members.append(user)

    db.session.add(group)
    db.session.commit()

    return group

from model import User, Token
import crypto


def get_user_by_username(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        return False

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
        return False

    return token

from flask_login import current_user
from endpoint.lib.http import permission, APIException
from endpoint.models import api


@permission
def can_list_user_orders(user_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    if current_user.id == user_id:
        return True

    return False


@permission
def can_block_users(*args, **kwargs):
    if not current_user.is_authenticated:
        return False

    return api.is_restaurant_owner(current_user)


@permission
def can_unblock_users(*args, **kwargs):
    if not current_user.is_authenticated:
        return False

    return api.is_restaurant_owner(current_user)


@permission
def can_list_blocked_users(*args, **kwargs):
    if not current_user.is_authenticated:
        return False

    return api.is_restaurant_owner(current_user)

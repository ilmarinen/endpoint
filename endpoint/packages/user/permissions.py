from flask_login import current_user
from endpoint.lib.http import permission, APIException
import manage


@permission
def can_list_users():
    if not current_user.is_authenticated:
        return False

    current_user_groups = [group.name for group in current_user.groups]
    if 'admin' not in current_user_groups:
        raise APIException(401, 'Unauthorized')
    else:
        return True


@permission
def can_view_user(user_id):
    if not current_user.is_authenticated:
        return False

    if manage.user_in_group(current_user, 'admin') or current_user.id == user_id:
        return True
    else:
        raise APIException(401, 'Unauthorized')

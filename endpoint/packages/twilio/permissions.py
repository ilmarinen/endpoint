from flask_login import current_user
from endpoint.lib.http import permission, APIException
import manage


@permission
def can_view_user(user_id):
    if not current_user.is_authenticated:
        return False

    if manage.user_in_group(current_user, 'admin') or current_user.id == user_id:
        return True
    else:
        raise APIException(401, 'Unauthorized')

from endpoint.lib.http import RESTView
from flask import Blueprint, request
from flask_login import current_user
import permissions
import manage


bp = Blueprint('user_rest_views', __name__, template_folder='templates')


class AuthenticatedUserAPI(RESTView):

    def get(self):
        # return populator.marshal(current_user, user_format)
        return "Test"


class UserModelAPI(RESTView):

    @permissions.can_view_user
    def get(self, user_id):
        user = manage.get_user_by_id(user_id)
        # return populator.marshal(user, user_format)
        return "Test"


class UsersAPI(RESTView):

    @permissions.can_list_users
    def get(self, **kwargs):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        users = manage.list_users(limit, offset)
        # return populator.marshal(users, user_format)
        return "Test"


bp.add_url_rule('/v1/users/authenticated_user', view_func=AuthenticatedUserAPI.as_view('authenticated_user_api'))
bp.add_url_rule('/v1/users/<int:user_id>', view_func=UserModelAPI.as_view('user_model_api'))
bp.add_url_rule('/v1/users/', view_func=UsersAPI.as_view('users_view'))

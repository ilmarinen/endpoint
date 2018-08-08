from endpoint.lib.http import RESTView, APIException
from endpoint.lib import formatter
from endpoint.packages.user import data_format
from flask import Blueprint, request
from flask_login import current_user, login_required, login_user, logout_user
import permissions
import manage


bp = Blueprint('user_rest_views', __name__, template_folder='templates')


class WebEventAPI(RESTView):

    @permissions.can_list_users
    def get(self, **kwargs):
        return True

bp.add_url_rule('/v1/event/', view_func=WebEventAPI.as_view('webevent_view'))

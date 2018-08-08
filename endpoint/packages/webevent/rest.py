from endpoint.lib.http import RESTView, APIException
from flask import Blueprint, request
import manage


bp = Blueprint('webevent_rest_views', __name__, template_folder='templates')


class WebEventAPI(RESTView):

    def get(self, **kwargs):
        return True

bp.add_url_rule('/v1/event/', view_func=WebEventAPI.as_view('webevent_view'))

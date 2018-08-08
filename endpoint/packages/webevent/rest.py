from endpoint.lib.http import RESTView, APIException
from flask import Blueprint, request
import manage


bp = Blueprint('webevent_rest_views', __name__, template_folder='templates')


class InitialWebEventAPI(RESTView):

    def get(self, visitor_slug):
        return visitor_slug

class WebEventAPI(RESTView):

    def get(self, visitor_slug):
        return visitor_slug


class InformativeWebEventAPI(RESTView):

    def get(self, visitor_slug):
        return visitor_slug


bp.add_url_rule('/v1/event/initial/<string:visitor_slug>', view_func=InitialWebEventAPI.as_view('initial_webevent_view'))
bp.add_url_rule('/v1/event/<string:visitor_slug>', view_func=WebEventAPI.as_view('webevent_view'))
bp.add_url_rule('/v1/event/informative/<string:visitor_slug>', view_func=InformativeWebEventAPI.as_view('informative_webevent_view'))

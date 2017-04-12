from flask import Blueprint
from endpoint.lib.http import RESTView


bp = Blueprint('twilio_rest_views', __name__, template_folder='templates')


class TwilioAPI(RESTView):

    def post(self, **kwargs):
        return True


bp.add_url_rule('/v1/twilio/', view_func=TwilioAPI.as_view('twilio_endpoint'))

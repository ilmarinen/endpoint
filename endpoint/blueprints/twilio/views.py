from flask import Blueprint, request, Response, current_app
from endpoint.blueprints.twilio import permissions
import re


bp = Blueprint('twilio_views', __name__, template_folder='templates')


@bp.route('/sms', methods=['POST'])
@permissions.twilio_account_exists
def receive_sms(**kwargs):
    sms_body = request.form.get("Body")

    # Insert logic to handle message here
    print("Twilio SMS: ", sms_body)

    xml_response = "<Response><Message>Thanks</Message></Response>"
    return Response(xml_response, mimetype="text/xml")

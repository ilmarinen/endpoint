from flask import Blueprint, request, Response
import permissions
import urlmarker
import re


bp = Blueprint('twilio_views', __name__, template_folder='templates')


@bp.route('/sms', methods=['POST'])
@permissions.accountsid_matches_token
def receive_sms(**kwargs):
    sms_body = request.form.get("Body")
    print re.findall(urlmarker.WEB_URL_REGEX, sms_body)
    xml_response = "<Response><Message>Thanks</Message></Response>"
    return Response(xml_response, mimetype="text/xml")

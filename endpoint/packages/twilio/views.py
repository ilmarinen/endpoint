from flask import Blueprint, request, Response, current_app
from link_archiver import mediawiki_bot
import permissions
import urlmarker
import re


bp = Blueprint('twilio_views', __name__, template_folder='templates')


@bp.route('/sms', methods=['POST'])
@permissions.accountsid_matches_token
def receive_sms(**kwargs):
    sms_body = request.form.get("Body")
    links = re.findall(urlmarker.WEB_URL_REGEX, sms_body)
    mediawiki_bot.login()
    for link in links:
        mediawiki_bot.append_url(current_app.config["WIKI_PAGE"], link)
    xml_response = "<Response><Message>Thanks</Message></Response>"
    return Response(xml_response, mimetype="text/xml")

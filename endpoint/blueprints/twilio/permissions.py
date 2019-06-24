from endpoint.lib.http import permission, APIException
from endpoint.models import api
from flask import request


@permission
def twilio_account_exists():
    accountsid = request.form.get("AccountSid")
    twilio_account = api.get_twillio_account_by_sid(accountsid)
    if twilio_account is not None:
        return True
    else:
        raise APIException(401, "Unauthorized")

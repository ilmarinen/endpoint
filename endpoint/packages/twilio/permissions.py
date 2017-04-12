from endpoint.lib.http import permission, APIException
from endpoint.packages.user import manage
from flask import request


@permission
def accountsid_matches_token():
    accountsid = request.form.get("AccountSid")
    if manage.get_token_by_value(accountsid):
        return True
    else:
        raise APIException(401, "Unauthorized")

from endpoint.lib.http import permission, APIException
from endpoint.data_backends import DataLayer
from flask import request


@permission
def accountsid_matches_token():
    accountsid = request.form.get("AccountSid")
    if DataLayer.get_token_by_value(accountsid):
        return True
    else:
        raise APIException(401, "Unauthorized")

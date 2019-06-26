from endpoint.lib.http import RESTView, BaseView, APIException
from endpoint.lib import formatter
from endpoint.blueprints.users import data_format
from endpoint.blueprints.restaurants import data_format as restaurants_data_format
from flask import Blueprint, request, session, render_template
from endpoint.models import api
from flask_login import current_user, logout_user
from endpoint.blueprints.users import permissions
from endpoint.models import formatting
from endpoint.models import models


bp = Blueprint('user_rest_views', __name__, template_folder='templates')


class AuthenticationUserAPI(RESTView):

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        authenticated = api.authenticate(username, password)
        if not authenticated:
            raise APIException(401, "Unauthorized")

        return authenticated


class LogoutUserAPI(RESTView):

    def post(self):
        logout_user()
        return True


class AuthenticatedUserAPI(RESTView):

    def get(self):
        if not current_user.is_authenticated:
            raise APIException(401, "Unauthorized")
        user_data = formatter.make(current_user, formatting.user_format)
        if api.is_restaurant_owner(current_user):
            user_data["restaurant_owner"] = True
        else:
            user_data["restaurant_owner"] = False

        return user_data

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if api.authenticate(username, password):
            user_data = formatter.make(current_user, formatting.user_format)
            if api.is_restaurant_owner(current_user):
                user_data["restaurant_owner"] = True
            else:
                user_data["restaurant_owner"] = False

            return user_data

        raise APIException(401, "Incorrect login")



class UserModelAPI(RESTView):

    def get(self, user_id):
        return "UserModelAPI GET"

    def put(self, user_id):
        user_data = request.get_json()
        firstname = user_data.get("firstname")
        lastname = user_data.get("lastname")
        user = api.update_user(user_id, firstname, lastname)
        user_data = formatter.make(current_user, data_format.user_format)
        if api.is_restaurant_owner(current_user):
            user_data["restaurant_owner"] = True
        else:
            user_data["restaurant_owner"] = False
        return user_data


class UsersAPI(RESTView):

    def get(self, **kwargs):
        return "UsersAPI GET"


class UserUnBlockedModelAPI(RESTView):

    @permissions.can_unblock_users
    def post(self, user_id):
        user = api.unblock_user(user_id)
        user_data = formatter.make(user, formatting.user_format)
        if api.is_restaurant_owner(user):
            user_data["restaurant_owner"] = True
        else:
            user_data["restaurant_owner"] = False
        return user_data


class UsersBlockedAPI(RESTView):

    @permissions.can_list_blocked_users
    def get(self, **kwargs):
        users = models.User.query.filter_by(blocked=True).all()
        users_data = []
        for user in users:
            users_data.append(formatter.make(user, formatting.user_format))

        return users_data


class UsersBlockingAPI(RESTView):

    @permissions.can_block_users
    def post(self, **kwargs):
        request_data = request.get_json()
        if "username" not in request_data:
            raise APIException(500, "Must provide username")
        username = request_data.get("username")
        user = api.block_user_by_username(username)
        return formatter.make(user, formatting.user_format)


class SignupAPI(RESTView):

    def post(self, **kwargs):
        data = request.get_json()
        user, token = api.signup(
            data.get('username'),
            data.get('firstname'),
            data.get('lastname'),
            data.get('email'),
            data.get('password'),
            data.get('restaurant_owner'))
        return True


@bp.route('/v1/users/signup/<string:token>')
def confirmation(token):
    user = api.confirm_signup(token)
    return render_template("confirmed.html")


@bp.route('/v1/users/claim_invite/<string:token>')
def claim_invite(token):
    if not api.claim_invite(token):
        raise Exception("Failed to claim invite")
    return render_template("invite_claimed.html")


class InviteAPI(RESTView):

    def post(self, **kwargs):
        request_data = request.get_json()
        if "email" not in request_data:
            raise APIException(403, "Email required")
        token = api.invite_via_email(current_user, request_data.get("email"))
        print("Invite: ", token)
        return True


class UserOrdersAPI(RESTView):

    @permissions.can_list_user_orders
    def get(self, user_id, **kwargs):
        orders = api.list_user_orders(current_user.id)
        return list(map(formatting.build_order_json, orders))


class UserOrdersModelAPI(RESTView):

    @permissions.can_list_user_orders
    def get(self, user_id, order_id, **kwargs):
        order = api.get_order_by_id(order_id)
        return formatting.build_order_json(order)


class UserIncrementOrderAPI(RESTView):

    def put(self, user_id, order_id, **kwargs):
        order = api.user_order_increment_status(order_id)
        return formatting.build_order_json(order)


class UserIncomingOrdersAPI(RESTView):

    @permissions.can_list_user_orders
    def get(self, user_id, **kwargs):
        orders = api.list_incoming_orders(user_id)
        return list(map(formatting.build_order_json, orders))


class UserIncomingOrdersModelAPI(RESTView):

    @permissions.can_list_user_orders
    def get(self, user_id, order_id, **kwargs):
        order = api.get_order_by_id(order_id)
        return formatting.build_order_json(order)


class UserIncrementIncomingOrdersAPI(RESTView):

    def put(self, user_id, order_id, **kwargs):
        order = api.user_incoming_order_increment_status(order_id)
        return formatting.build_order_json(order)


class UserRestaurantModelAPI(RESTView):

    def get(self, user_id):
        restaurants = api.list_user_restaurants(current_user.id)
        return list(map(formatting.build_restaurant_json, restaurants))


bp.add_url_rule('/v1/users/authenticated', view_func=AuthenticatedUserAPI.as_view('authenticated_user_api'))
bp.add_url_rule('/v1/users/authenticate', view_func=AuthenticationUserAPI.as_view('authentication_user_api'))
bp.add_url_rule('/v1/users/logout', view_func=LogoutUserAPI.as_view('logout_user_api'))
bp.add_url_rule('/v1/users/<int:user_id>', view_func=UserModelAPI.as_view('user_model_api'))
bp.add_url_rule('/v1/users', view_func=UsersAPI.as_view('users_view'))
bp.add_url_rule('/v1/blocked_users', view_func=UsersBlockedAPI.as_view('blocked_users_view'))
bp.add_url_rule('/v1/blocked_users', view_func=UsersBlockingAPI.as_view('blocking_users_view'))
bp.add_url_rule('/v1/blocked_users/<int:user_id>', view_func=UserUnBlockedModelAPI.as_view('blocked_user_model_view'))
bp.add_url_rule('/v1/users/signup', view_func=SignupAPI.as_view('signup_view'))
bp.add_url_rule('/v1/users/<int:user_id>/invites', view_func=InviteAPI.as_view('invite_view'))
bp.add_url_rule('/v1/users/<int:user_id>/orders', view_func=UserOrdersAPI.as_view('user_orders_view'))
bp.add_url_rule('/v1/users/<int:user_id>/orders/<int:order_id>/increment_status', view_func=UserIncrementOrderAPI.as_view('user_increment_orders_view'))
bp.add_url_rule('/v1/users/<int:user_id>/orders/<int:order_id>', view_func=UserOrdersModelAPI.as_view('user_orders_model_view'))
bp.add_url_rule('/v1/users/<int:user_id>/incoming_orders', view_func=UserIncomingOrdersAPI.as_view('user_incoming_orders_view'))
bp.add_url_rule('/v1/users/<int:user_id>/incoming_orders/<int:order_id>/increment_status', view_func=UserIncrementIncomingOrdersAPI.as_view('user_increment_incoming_orders_view'))
bp.add_url_rule('/v1/users/<int:user_id>/incoming_orders/<int:order_id>', view_func=UserIncomingOrdersModelAPI.as_view('user_incoming_orders_model_view'))
bp.add_url_rule('/v1/users/<int:user_id>/restaurants', view_func=UserRestaurantModelAPI.as_view('user_restaurants_view'))

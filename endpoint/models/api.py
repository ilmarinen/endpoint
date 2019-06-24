import base64
from datetime import datetime, timedelta
from endpoint import db
from endpoint.models import models
from endpoint import app
from itsdangerous import Signer
from flask_login import login_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from endpoint.lib.http import APIException


def _email_confirmation(email, token):
    html_content =\
        "<h1>Please Confirm by Clicking the Following Link</h1><br /><h2><a href='http://{}/api/v1/users/signup/{}'>Confirm Email</a></h2>".format(
            app.config.get("HOSTNAME"), token)
    message = Mail(
        from_email=app.config.get("ADMIN"),
        to_emails=email,
        subject="Signup Confirmation",
        html_content=html_content)
    sendgrid_client = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
    sendgrid_client.send(message)


def _email_invite(email, token):
    html_content =\
        "<h1>You have been invited to join the Endpoint!</h1><h2>Please signup by Clicking the following Link<br /><h3><a href='http://{}/api/v1/users/claim_invite/{}'>Claim Invite</a></h3>".format(
            app.config.get("HOSTNAME"), token)
    message = Mail(
        from_email=app.config.get("ADMIN"),
        to_emails=email,
        subject="Invitation to the Endpoint",
        html_content=html_content)
    sendgrid_client = SendGridAPIClient(app.config.get("SENDGRID_API_KEY"))
    sendgrid_client.send(message)


def generate_expiring_token(payload, expiry_date):
    signer = Signer(app.config.get("SECRET_KEY"))
    expiry_string = expiry_date.strftime("%Y-%m-%d-%H-%M-%S")
    cleartext_string = base64.b64encode("{},{}".format(payload, expiry_string).encode("utf-8")).decode()
    token = signer.sign(cleartext_string).decode()
    return token


def set_user_password(user, password):
    user.password = password
    db.session.add(user)
    db.session.commit()


def signup(username, firstname, lastname, email, password, restaurant_owner, send_email=True):
    restaurant_owner_group = models.Group.query.filter_by(groupname="restaurant_owners").first()
    user = models.User(username=username, firstname=firstname, lastname=lastname, email=email)
    user.password = password
    db.session.add(user)
    db.session.flush()
    if restaurant_owner:
        membership = models.Membership(user_id=user.id, group_id=restaurant_owner_group.id)
        db.session.add(membership)
        db.session.flush()
    try:
        expiry = datetime.now() + timedelta(days=app.config.get("CLAIM_EXPIRY_IN_DAYS"))
        token = generate_expiring_token(str(user.id), expiry)
        if send_email:
            _email_confirmation(user.email, token)
        db.session.commit()
    except:
        db.session.rollback()
        raise APIException(500, "Failed to send confirmation email")

    return user, token


def confirm_signup(token):
    signer = Signer(app.config.get("SECRET_KEY"))
    data = base64.b64decode(signer.unsign(token.encode("utf-8")).decode()).decode()
    user_id, expiry_string = data.split(",")
    user_id = int(user_id)
    user = models.User.query.get(user_id)
    expiry = datetime.strptime(expiry_string, "%Y-%m-%d-%H-%M-%S")
    if datetime.now() > expiry:
        raise Exception("Expired")
    user = models.User.query.get(user_id)
    user.is_active = True
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    user = models.User.query.filter_by(email=email).first()
    return user


def get_user_by_username(username):
    user = models.User.query.filter_by(username=username).first()
    return user


def claim_invite(token):
    signer = Signer(app.config.get("SECRET_KEY"))
    data = base64.b64decode(signer.unsign(token.encode("utf-8")).decode()).decode()
    email, expiry_string = data.split(",")
    if check_email_in_use(email):
        raise Exception("Email in use")
    expiry = datetime.strptime(expiry_string, "%Y-%m-%d-%H-%M-%S")
    if datetime.now() > expiry:
        raise Exception("Expired")
    return True


def invite_via_email(email):
    if check_email_in_use(email):
        raise APIException(500, "Email in use")

    expiry = datetime.now() + timedelta(days=app.config.get("CLAIM_EXPIRY_IN_DAYS"))
    token = generate_expiring_token(str(user.id), expiry)
    _email_invite(email, token)

    return token


def check_email_exists(email):
    users = models.User.query.filter_by(email=email).all()
    return (len(users) > 0)


def create_user(username, firstname, lastname, email, profile_filename=None, external_auth="", is_active=False, restaurant_owner=False, password=None):
    user = models.User(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        profile_filename=profile_filename,
        external_auth=external_auth,
        is_active=is_active)
    if password is not None:
        user.password = password
    db.session.add(user)
    db.session.flush()

    if restaurant_owner:
        restaurant_owner_group = models.Group.query.filter_by(groupname="restaurant_owners").first()
        membership = models.Membership(user_id=user.id, group_id=restaurant_owner_group.id)
        db.session.add(membership)
        db.session.flush()

    db.session.commit()
    return user


def update_user(user_id, firstname, lastname):
    user = models.User.query.get(user_id)
    if user is None:
        raise APIException(404, "Not found.")
    user.firstname = firstname
    user.lastname = lastname
    db.session.add(user)
    db.session.commit()
    return user


def block_user_by_username(username):
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        raise APIException(404, "Not found.")
    user.blocked = True
    db.session.add(user)
    db.session.commit()
    return user


def unblock_user(user_id):
    user = models.User.query.get(user_id)
    if user is None:
        raise APIException(404, "Not found.")
    user.blocked = False
    user.failed_login_attempts = 0
    db.session.add(user)
    db.session.commit()
    return user


def failed_login(user):
    if user is not None:
        user.failed_login_attempts = user.failed_login_attempts + 1

    if user.failed_login_attempts == 3:
        user.blocked = True

    db.session.add(user)
    db.session.commit()


def authenticate(username, password):
    user = models.User.query.filter_by(username=username).first()
    if user.blocked:
        return False

    if user.verify_password(password) and user.blocked == False:
        user.failed_login_attempts = 0
        db.session.add(user)
        db.session.commit()
        return login_user(user)

    elif not user.verify_password(password):
        failed_login(user)

    return False


def is_restaurant_owner(user):
    restaurant_owners_group = models.Group.query.filter_by(groupname="restaurant_owners").first()
    user_membership = models.Membership.query.filter_by(user_id=user.id, group_id=restaurant_owners_group.id)

    return user_membership.count() > 0


def create_restaurant(name, description, owner_id):
    restaurant = models.Restaurant(name=name, description=description, owner_id=owner_id)
    db.session.add(restaurant)
    db.session.commit()
    return restaurant


def list_restaurants():
    restaurants = models.Restaurant.query.all()
    return restaurants


def get_restaurant(restaurant_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")
    return restaurant


def update_restaurant(restaurant_id, name, description):
    restaurant = models.Restaurant.query.get(restaurant_id)
    restaurant.name = name
    restaurant.description = description
    db.session.add(restaurant)
    db.session.commit()
    return restaurant


def delete_restaurant(restaurant_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    db.session.delete(restaurant)
    db.session.commit()


def list_restaurant_meals(restaurant_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    meals = models.Meal.query.filter_by(restaurant_id=restaurant_id)
    return meals


def get_restaurant_meal(restaurant_id, meal_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    meal = models.Meal.query.get(meal_id)
    if not meal:
        raise APIException(404, "Not found")

    return meal


def create_restaurant_meal(restaurant_id, name, description, price):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    meal = models.Meal(name=name, description=description, price=price, restaurant_id=restaurant_id)
    db.session.add(meal)
    db.session.commit()
    return meal


def update_restaurant_meal(restaurant_id, meal_id, name, description, price):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    meal = models.Meal.query.get(meal_id)
    if not meal:
        raise APIException(404, "Not found")

    meal.name = name
    meal.description = description
    meal.price = price
    db.session.add(meal)
    db.session.commit()
    return meal


def delete_restaurant_meal(restaurant_id, meal_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    meal = models.Meal.query.get(meal_id)
    if not meal:
        raise APIException(404, "Not found")

    db.session.delete(meal)
    db.session.commit()


def create_restaurant_order(restaurant_id, meal_ids, user_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    meals = list(
                filter(
                    lambda restaurant_meal: restaurant_meal.restaurant_id == restaurant_id,
                    filter(
                        lambda meal: meal is not None,
                        map(lambda meal_id: models.Meal.query.get(meal_id), meal_ids))))
    if len(meals) != len(meal_ids):
        raise APIException(404, "Meal not found")

    total_meal_price = sum(map(lambda meal: meal.price, meals))
    order = models.Order(user_id=user_id, restaurant_id=restaurant_id, amount=total_meal_price, status=models.EnumStatus.placed)
    order_history = record_order_history(order)
    db.session.add(order)
    db.session.flush()

    order_meals = map(lambda meal: models.OrderMeal(order_id=order.id, meal_id=meal.id), meals)
    order_meals = list(map(lambda order_meal: db.session.add(order_meal), order_meals))
    order_history = record_order_history(order)
    db.session.add(order_history)
    db.session.commit()

    return order


def list_restaurant_orders(restaurant_id):
    restaurant = models.Restaurant.query.get(restaurant_id)
    if not restaurant:
        raise APIException(404, "Not found")

    orders = models.Order.query.filter_by(restaurant_id=restaurant_id).all()
    return orders


def list_user_orders(user_id):
    orders = models.Order.query.filter(models.Order.user_id == user_id, models.Order.status != models.EnumStatus.canceled).all()
    return orders


def list_order_meals(order_id):
    order_meals = models.OrderMeal.query.filter_by(order_id=order_id)
    return map(models.Meal.query.get, [order_meal.meal_id for order_meal in order_meals])


def list_user_restaurants(user_id):
    restaurants = models.Restaurant.query.filter_by(owner_id=user_id)
    return restaurants


def list_incoming_orders(user_id):
    restaurants = list_user_restaurants(user_id)
    orders = []
    for restaurant in restaurants:
        restaurant_orders = list_restaurant_orders(restaurant.id)
        orders = orders + restaurant_orders
    return orders


def record_order_history(order):
    order_history_record = models.OrderHistory(order_id=order.id, order_status=order.status)
    return order_history_record


def user_order_increment_status(order_id):
    order = models.Order.query.get(order_id)
    if order is None:
        raise APIException(404, "Order not found")

    if order.status != models.EnumStatus.placed and order.status != models.EnumStatus.delivered:
        raise APIException(403, "Not allowed")

    if order.status == models.EnumStatus.placed:
        order.status = models.EnumStatus.canceled
    elif order.status == models.EnumStatus.delivered:
        order.status = models.EnumStatus.received

    order_history = record_order_history(order)

    db.session.add(order)
    db.session.add(order_history)
    db.session.commit()
    return order


def user_incoming_order_increment_status(order_id):
    order = models.Order.query.get(order_id)
    if order is None:
        raise APIException(404, "Order not found")
    print(order.id, order.status)

    if order.status == models.EnumStatus.canceled or order.status == models.EnumStatus.delivered or order.status == models.EnumStatus.received:
        raise APIException(403, "Not allowed")

    if order.status == models.EnumStatus.placed:
        order.status = models.EnumStatus.processing
    elif order.status == models.EnumStatus.processing:
        order.status = models.EnumStatus.enroute
    elif order.status == models.EnumStatus.enroute:
        order.status = models.EnumStatus.delivered

    order_history = record_order_history(order)

    db.session.add(order)
    db.session.add(order_history)
    db.session.commit()
    return order


def get_order_by_id(order_id):
    order = models.Order.query.get(order_id)
    if order is None:
        raise APIException(404, "Order not found")
    return order

def get_twillio_account_by_sid(sid):
    token = Token.query.filter(Token.sid == sid).first()

    return token


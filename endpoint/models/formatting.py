from endpoint.models import api
from endpoint.lib import formatter
from endpoint.models import models

status_lookup = (
    models.EnumStatus.placed,
    models.EnumStatus.canceled,
    models.EnumStatus.processing,
    models.EnumStatus.enroute,
    models.EnumStatus.delivered,
    models.EnumStatus.received)


restaurant_format = {
    "id": "id",
    "name": "name",
    "description": "description",
    "owner_id": "owner_id"
}


meal_format = {
    "id": "id",
    "name": "name",
    "description": "description",
    "price": "price",
    "restaurant_id": "restaurant_id"
}

order_format = {
    "id": "id",
    "restaurant_id": "restaurant_id",
    "user_id": "user_id",
    "amount": "amount"
}

user_format = {
    "id": "id",
    "username": "username",
    "firstname": "firstname",
    "lastname": "lastname",
    "is_active": "is_active",
    "profile_filename": "profile_filename"
}


def build_restaurant_json(restaurant):
    restaurant_data = formatter.make(restaurant, restaurant_format)
    restaurant_meals = api.list_restaurant_meals(restaurant.id)
    meals = []
    for meal in restaurant_meals:
        meals.append(formatter.make(meal, meal_format))
    restaurant_data["meals"] = meals
    return restaurant_data


def build_order_history_json(order):
    statuses = {}
    statuses[models.EnumStatus.placed] = "placed"
    statuses[models.EnumStatus.canceled] = "canceled"
    statuses[models.EnumStatus.processing] = "processing"
    statuses[models.EnumStatus.enroute] = "enroute"
    statuses[models.EnumStatus.delivered] = "delivered"
    statuses[models.EnumStatus.received] = "received"
    order_history_records = models.OrderHistory.query.filter_by(order_id=order.id).order_by(models.OrderHistory.set_at.desc()).all()
    history_data = []
    for order_history_record in order_history_records:
        record_data = {}
        record_data["status"] = statuses[order_history_record.order_status]
        record_data["set_at"] = order_history_record.set_at.strftime("%Y-%m-%d %H:%M:%S")
        history_data.append(record_data)

    return history_data

def build_order_json(order):
    order_data = formatter.make(order, order_format)
    order_status = status_lookup.index(order.status)
    order_data["status"] = order_status
    meals_for_order = list(api.list_order_meals(order.id))
    meals_for_order_data = list(map(lambda meal: formatter.make(meal, meal_format), meals_for_order))
    order_data["meals"] = meals_for_order_data
    order_data["history"] = build_order_history_json(order)
    return order_data

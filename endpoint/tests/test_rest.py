import os
import unittest
import json

from endpoint.config import basedir
from endpoint import app, db, gen_fixtures
from endpoint.models import models
from endpoint.models import api

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        gen_fixtures()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_and_logout(self):
        user = api.create_user("heisenberg", "Werner", "Heisenberg", "test@test.com", is_active=True)
        api.set_user_password(user, "test1")

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test1"}))
        
        assert(response.status_code == 200)
        assert(response.get_json() == True)

        response = self.client.get(
            "api/v1/users/authenticated")

        assert(response.status_code == 200)

        user_data = response.get_json()

        assert(user_data.get("username") == "heisenberg")

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.get(
            "api/v1/users/authenticated")

        assert(response.status_code == 401)

    def test_only_owners_can_create_restaurants(self):
        user_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        user_b = api.create_user("heisenberg", "Werner", "Heisenberg", "h@test.com", restaurant_owner=False, is_active=True, password="test")

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Quantum Cafe", "description": "Veg and Non-Veg"}))
        
        assert(response.status_code == 200)

        restaurant_data = response.get_json()

        assert(restaurant_data.get("name") == "Quantum Cafe")
        assert(restaurant_data.get("description") == "Veg and Non-Veg")
        assert(restaurant_data.get("owner_id") == user_a.id)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})
        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Quanta", "description": "Tapas"}))

        assert(response.status_code == 401)

    def test_only_owner_can_create_meals_in_restaurant(self):
        owner_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_b = api.create_user("einstein", "Albert", "Einstein", "einstein@test.com", restaurant_owner=True, is_active=True, password="test")

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Quantum Cafe", "description": "Veg and Non-Veg"}))

        restaurant_data = response.get_json()
        restaurant_id = restaurant_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Schrodingers Cat", "description": "Surprise dish based on chef's discretion."}))

        assert(response.status_code == 200)

        meal_data = response.get_json()

        assert(meal_data.get("restaurant_id") == restaurant_id)
        assert(meal_data.get("name") == "Schrodingers Cat")
        assert(meal_data.get("description") == "Surprise dish based on chef's discretion.")
        

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "No Dice", "description": "A cocktail that only God could have created."}))

        assert(response.status_code == 401)

    def test_user_can_place_order(self):
        owner_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_b = api.create_user("einstein", "Albert", "Einstein", "einstein@test.com", restaurant_owner=True, is_active=True, password="test")
        user_b = api.create_user("heisenberg", "Werner", "Heisenberg", "h@test.com", restaurant_owner=False, is_active=True, password="test")

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Quantum Cafe", "description": "Veg and Non-Veg"}))

        restaurant_data = response.get_json()
        restaurant_id = restaurant_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Schrodingers Cat", "description": "Surprise dish based on chef's discretion.", "price": 3}))
        
        meal_data = response.get_json()
        meal_id_a = meal_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "No Dice", "description": "A cocktail that only God could have created.", "price": 5}))

        meal_data = response.get_json()
        meal_id_b = meal_data.get("id")

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/{}/orders".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"meal_ids": [meal_id_a, meal_id_b]}))

        order_data = response.get_json()

        assert(len(order_data.get("meals")) == 2)
        assert(order_data.get("amount") == 8)
        assert(order_data.get("restaurant_id") == restaurant_id)

    def test_order_placer_and_restaurant_owner_can_see_order(self):
        owner_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_a_id = owner_a.id

        owner_b = api.create_user("einstein", "Albert", "Einstein", "einstein@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_b_id = owner_b.id

        user_b = api.create_user("heisenberg", "Werner", "Heisenberg", "h@test.com", restaurant_owner=False, is_active=True, password="test")
        user_b_id = user_b.id

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Quantum Cafe", "description": "Veg and Non-Veg"}))

        restaurant_data = response.get_json()
        restaurant_id = restaurant_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Schrodingers Cat", "description": "Surprise dish based on chef's discretion.", "price": 3}))
        
        meal_data = response.get_json()
        meal_id_a = meal_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "No Dice", "description": "A cocktail that only God could have created.", "price": 5}))

        meal_data = response.get_json()
        meal_id_b = meal_data.get("id")

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/{}/orders".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"meal_ids": [meal_id_a, meal_id_b]}))
        order_data = response.get_json()
        order_id = order_data.get("id")

        response = self.client.get("api/v1/users/{}/orders".format(user_b_id))

        orders_data = response.get_json()

        assert(orders_data[0].get("id") == order_id)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.get(
            "api/v1/users/{}/incoming_orders".format(owner_a_id))
        incoming_order_data = response.get_json()

        assert(len(incoming_order_data) == 1)
        assert(incoming_order_data[0].get('id') == order_id)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))

        response = self.client.get(
            "api/v1/users/{}/incoming_orders".format(owner_a_id))

        assert(response.status_code == 401)

        response = self.client.get(
            "api/v1/users/{}/incoming_orders".format(owner_b_id))
        incoming_order_data = response.get_json()

        assert(len(incoming_order_data) == 0)

    def test_increment_order_status(self):
        owner_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_a_id = owner_a.id

        owner_b = api.create_user("einstein", "Albert", "Einstein", "einstein@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_b_id = owner_b.id

        user_b = api.create_user("heisenberg", "Werner", "Heisenberg", "h@test.com", restaurant_owner=False, is_active=True, password="test")
        user_b_id = user_b.id

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Quantum Cafe", "description": "Veg and Non-Veg"}))

        restaurant_data = response.get_json()
        restaurant_id = restaurant_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Schrodingers Cat", "description": "Surprise dish based on chef's discretion.", "price": 3}))
        
        meal_data = response.get_json()
        meal_id_a = meal_data.get("id")

        response = self.client.post(
            "api/v1/restaurants/{}/meals".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "No Dice", "description": "A cocktail that only God could have created.", "price": 5}))

        meal_data = response.get_json()
        meal_id_b = meal_data.get("id")

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.post(
            "api/v1/restaurants/{}/orders".format(restaurant_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"meal_ids": [meal_id_a, meal_id_b]}))
        order_data = response.get_json()
        order_id = order_data.get("id")

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.put(
            "api/v1/users/{}/incoming_orders/{}/increment_status".format(owner_a_id, order_id))

        assert(response.status_code == 200)

        response = self.client.get(
            "api/v1/users/{}/incoming_orders/{}".format(owner_a_id, order_id))
        order_data = response.get_json()

        assert(order_data.get("status") == 2)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.put(
            "api/v1/users/{}/orders/{}/increment_status".format(user_b_id, order_id))

        assert(response.status_code == 403)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.put(
            "api/v1/users/{}/incoming_orders/{}/increment_status".format(owner_a_id, order_id))
        assert(response.status_code == 200)

        response = self.client.put(
            "api/v1/users/{}/incoming_orders/{}/increment_status".format(owner_a_id, order_id))
        assert(response.status_code == 200)

        response = self.client.put(
            "api/v1/users/{}/incoming_orders/{}/increment_status".format(owner_a_id, order_id))
        assert(response.status_code == 403)

        response = self.client.put(
            "api/v1/users/{}/incoming_orders/{}/increment_status".format(owner_a_id, order_id))
        assert(response.status_code == 403)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.put(
            "api/v1/users/{}/orders/{}/increment_status".format(user_b_id, order_id))

        assert(response.status_code == 200)

        response = self.client.get(
            "api/v1/users/{}/orders/{}".format(user_b_id, order_id))
        order_data = response.get_json()

        assert(order_data.get("status") == 5)

    def test_owner_can_block_user(self):
        owner_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_a_id = owner_a.id

        user_b = api.create_user("einstein", "Albert", "Einstein", "einstein@test.com", restaurant_owner=False, is_active=True, password="test")
        user_b_id = user_b.id

        user_c = api.create_user("heisenberg", "Werner", "Heisenberg", "h@test.com", restaurant_owner=False, is_active=True, password="test")
        user_c_id = user_c.id

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/blocked_users",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein"}))
        assert(response.status_code == 200)

        response = self.client.get("api/v1/blocked_users")

        assert(response.status_code == 200)

        blocked_users_data = response.get_json()
        assert(len(blocked_users_data) == 1)
        assert(blocked_users_data[0].get("id") == user_b_id)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))
        assert(response.status_code == 401)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test"}))

        response = self.client.post(
            "api/v1/blocked_users/{}".format(user_b_id),
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein"}))
        assert(response.status_code == 401)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/blocked_users/{}".format(user_b_id),
            headers={"Content-Type": "application/json"})
        assert(response.status_code == 200)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))
        assert(response.status_code == 200)

    def test_user_blocked_after_three_failed_login_attempts(self):
        owner_a = api.create_user("max", "Max", "Planck", "max@test.com", restaurant_owner=True, is_active=True, password="test")
        owner_a_id = owner_a.id

        user_b = api.create_user("einstein", "Albert", "Einstein", "einstein@test.com", restaurant_owner=False, is_active=True, password="test")
        user_b_id = user_b.id

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))
        assert(response.status_code == 200)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test1"}))
        assert(response.status_code == 401)

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test1"}))
        assert(response.status_code == 401)

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test1"}))
        assert(response.status_code == 401)

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))
        assert(response.status_code == 401)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "max", "password": "test"}))

        response = self.client.post(
            "api/v1/blocked_users/{}".format(user_b_id),
            headers={"Content-Type": "application/json"})
        assert(response.status_code == 200)

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "einstein", "password": "test"}))
        assert(response.status_code == 200)

from datetime import datetime
import enum
import uuid
from endpoint import db
from flask_sqlalchemy import orm
from flask_login import UserMixin
from endpoint import login
from endpoint.lib import crypto


class EnumStatus(enum.Enum):
    placed = 1
    canceled = 2
    processing = 3
    enroute = 4
    delivered = 5
    received = 6


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    blocked = db.Column(db.Boolean, default=False)
    profile_filename = db.Column(db.String(70))
    external_auth = db.Column(db.String(20))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password_string):
        if password_string:
            self.password_hash = crypto.hash_pass(password_string)
        else:
            self.password_hash = None

    def verify_password(self, password):
        return crypto.verify_pass(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Group {}>'.format(self.username)


class Invite(db.Model):
    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True)
    invitee_email = db.Column(db.String(64), unique=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    claimed = db.Column(db.Boolean, default=False)


class Membership(db.Model):
    __tablename__ = "memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    user = orm.relationship(User, backref=orm.backref("orders", cascade="all, delete-orphan"))
    group = orm.relationship(Group, backref=orm.backref("groups", cascade="all, delete-orphan"))


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    owner = orm.relationship(User, backref=orm.backref("owners", cascade="all, delete-orphan"))


class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    status = db.Column(db.Enum(EnumStatus))
    amount = db.Column(db.Integer)


class OrderMeal(db.Model):
    __tablename__ = "ordermeals"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"))


class OrderHistory(db.Model):
    __tablename__ = "orders_history"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    order_status = db.Column(db.Enum(EnumStatus))
    set_at = db.Column(db.DateTime, default=datetime.utcnow)


class TwilioAccount(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(100), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", backref="tokens")

    def __init__(self):
        self.value = str(uuid.uuid4())

    def __repr__(self):
        return self.value


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

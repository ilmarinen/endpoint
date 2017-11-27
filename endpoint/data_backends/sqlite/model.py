import uuid
from database import db
from endpoint.data_backends import mixins
from flask_login import current_user


membership_table = db.Table("group_members", db.Model.metadata,
                            db.Column("group_id", db.Integer, db.ForeignKey("groups.id"), nullable=False),
                            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=False)
                            )


class User(mixins.UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    _password = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False, nullable=False)


class Group(mixins.GroupMixin, db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))

    members = db.relationship("User", secondary=membership_table,
                              backref="groups")


class Token(mixins.TokenMixin, db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", backref="tokens")

    def __init__(self):

        self.value = str(uuid.uuid4())

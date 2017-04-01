from endpoint.database import db
from crypto import hash_pass
from flask_login import current_user


membership_table = db.Table('group_members', db.Model.metadata,
                            db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
                            db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                            )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    _password = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self.username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_string):
        if password_string:
            self._password = hash_pass(password_string)
        else:
            self._password = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    members = db.relationship('User', secondary=membership_table, backref='groups')

    def __repr__(self):
        return self.name

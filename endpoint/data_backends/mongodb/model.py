import uuid
from database import db
from endpoint.data_backends import mixins


class User(mixins.UserMixin, db.Document):
    username = db.StringField(max_length=40, required=True)
    first_name = db.StringField(max_length=100)
    last_name = db.StringField(max_length=100)
    _password = db.StringField(max_length=100)
    active = db.BooleanField(default=False, required=True)
    groups = db.ListField(db.ReferenceField('Group'))
    tokens = db.ListField(db.ReferenceField('Token'))


class Group(mixins.GroupMixin, db.Document):
    name = db.StringField(max_length=100, required=True)
    description = db.StringField(max_length=40)


class Token(mixins.TokenMixin, db.Document):
    value = db.StringField(max_length=100, required=False)

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = str(uuid.uuid4())

        return super(Token, self).save(*args, **kwargs)

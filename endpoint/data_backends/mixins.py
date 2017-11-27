from endpoint.lib import crypto


class UserMixin(object):

    def __repr__(self):
        return self.username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_string):
        if password_string:
            self._password = crypto.hash_pass(password_string)
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


class GroupMixin(object):

    def __repr__(self):
        return self.name


class TokenMixin(object):

    def __repr__(self):
        return self.value

class Result(object):

    def __init__(self, success=False, data=None, errors=None):
        self.success = success
        self.data = data
        self.errors = errors

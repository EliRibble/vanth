import logging

LOGGER = logging.getLogger(__name__)

class User():
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = 'a person'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        LOGGER.debug("Getting user id")
        return str(self.user_id)

def load(user_id):
    return User(user_id)

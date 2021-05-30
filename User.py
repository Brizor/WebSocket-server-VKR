

class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
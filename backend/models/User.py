class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.attempt = 0
        self.locked = False
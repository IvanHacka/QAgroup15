class UserService:
    def __init__(self):
        # two fixed account
        self.users = {
            "staff01": "password123",
            "staff02": "password123"
        }

    def login(self, username, password):
        if not username or not password:
            return False, "Username and password are required"

        return self.users.get(username) == password

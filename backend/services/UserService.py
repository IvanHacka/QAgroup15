class UserService:
    def __init__(self):
        # fixed account 
        self.users = {
            "staff01": "password123",
            "staff02": "password123"
        }

    def login(self, username, password):
        if not username or not password:
            return False, "Username and password are required"

        if username in self.users and self.users[username] == password:
            return True, {
                "username": username,
                "role": "staff"
            }

        return False, "Invalid username or password"

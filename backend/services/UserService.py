from backend.models.User import User
class UserService:
    def __init__(self):
        # two fixed account
        self.users = {
            "staff01": User("staff01", "password123"),
            "staff02": User("staff02", "password123")
        }

    def login(self, username, password) -> User:
        user = self.users.get(username)
        if not user:
            raise ValueError("User not found")
        if user.locked:
            raise ValueError("User Account is locked")

        if user.password != password:
            user.attempt += 1
            if user.attempt >= 3:
                user.locked = True
                raise ValueError("Account is locked due to 3 failed attempts")

            raise ValueError(f"User attempt: {user.attempt}/3")

        if not username or not password:
            return False, "Username and password are required"

        # Reset attempt if successful
        user.attempt = 0
        return user


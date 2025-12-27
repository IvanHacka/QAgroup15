class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register(self, username, password):
        users = self.user_repo.load_users()

        if username is None or username.strip() == "":
            return False, "Username cannot be empty"

        if password is None or password.strip() == "":
            return False, "Password cannot be empty"

        username = username.strip()

        if username in users:
            return False, "Username already in use"

        users[username] = password
        self.user_repo.save_users(users)

        return True, "User registered successfully"

    def login(self, username, password):
        users = self.user_repo.load_users()

        if username is None :
            return False, "Username cannot be empty"

        if password is None :
            return False, "Password cannot be empty"

        username = username.strip()

        if username in users and users[username] == password:
            return True, "Login successful"

        return False, "Invalid username or password"


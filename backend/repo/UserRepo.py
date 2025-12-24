import json
import os


class UserRepo:
    # file path for storing users
    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = os.path.join("data", "Users.json")#sets file path
        else:
            self.file_path = file_path

    def load_users(self):
        # if file does not exist return empty
        if not os.path.exists(self.file_path):
            return {}

        # open file and read users
        with open(self.file_path, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                return {}
            except json.JSONDecodeError:
                # if file is empty
                return {}

    def save_users(self, users):
        # checks data folder exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # write users back to file
        with open(self.file_path, "w") as f:
            json.dump(users, f)

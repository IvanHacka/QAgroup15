from flask import request, jsonify


class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def register(self):
        # get json from request
        data = request.get_json(silent=True) or {}

        username = data.get("username")
        password = data.get("password")

        ok, message = self.user_service.register(username, password)

        if ok:
            return jsonify({"message": message}), 201
        else:
            return jsonify({"error": message}), 400

    def login(self):
        # get json from request
        data = request.get_json(silent=True) or {}

        username = data.get("username")
        password = data.get("password")

        ok, message = self.user_service.login(username, password)

        if ok:
            return jsonify({"message": message, "username": username}), 200
        else:
            return jsonify({"error": message}), 401

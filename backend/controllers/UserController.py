from flask import request, jsonify
from backend.services.UserService import UserService


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, username, password):
        # data = request.get_json(silent=True) or {}
        #
        # username = data.get("username")
        # password = data.get("password")
        #
        # try:
        #     user = self.user_service.login(username, password)
        #
        #     return jsonify({
        #         "message": "Login successful",
        #         "user": user
        #     }), 200
        #
        # except ValueError as e:
        #     return jsonify({
        #         "error": str(e)
        #     }), 401
        return self.user_service.login(username, password)
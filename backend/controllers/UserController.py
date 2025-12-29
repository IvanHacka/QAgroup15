from flask import request, jsonify


class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def login(self):
        data = request.get_json(silent=True) or {}

        username = data.get("username")
        password = data.get("password")

        try:
            user = self.user_service.login(username, password)

            return jsonify({
                "message": "Login successful",
                "user": user
            }), 200

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 401

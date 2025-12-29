from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

# Bug
from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

# User (Login only)
from backend.controllers.UserController import UserController
from backend.services.UserService import UserService

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)
CORS(app)

# Bug setup
bug_repo = BugRepo()
bug_service = BugService(bug_repo)
bug_controller = BugController(bug_service)


# User (login only)
user_service = UserService()
user_controller = UserController(user_service)


# Routes

@app.route("/")
def index():
    return render_template("index.html")

# ---- Bug APIs

@app.route("/api/bugs", methods=["GET"])
def get_bugs():
    return bug_controller.get_all()

@app.route("/api/bugs", methods=["POST"])
def create_bug():
    return bug_controller.create()

@app.route("/api/bugs/<bug_id>", methods=["PUT", "PATCH"])
def update_bug(bug_id):
    return bug_controller.update(bug_id)

@app.route("/api/bugs/<bug_id>/status", methods=["PUT"])
def update_bug_status(bug_id):
    return bug_controller.update_status(bug_id)

@app.route("/api/bugs/<bug_id>/assign", methods=["POST"])
def assign_bug(bug_id):
    return bug_controller.assign(bug_id)

@app.route("/api/bugs/<bug_id>", methods=["DELETE"])
def delete_bug(bug_id):
    return bug_controller.delete(bug_id)

# Login API 

@app.route("/api/login", methods=["POST"])
def login():
    return user_controller.login()

# Error handling
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


# Run
if __name__ == "__main__":
    print("Starting server...")
    print("Bug Tracker API starting...")
    app.run(host="0.0.0.0", port=5001, debug=True)

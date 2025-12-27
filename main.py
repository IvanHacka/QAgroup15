from flask import Flask, jsonify
from flask import render_template, request


from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

from backend.controllers.UserController import UserController
from backend.repo.UserRepo import UserRepo
from backend.services.UserService import UserService

app = Flask(__name__, template_folder="frontend/templates")


# Bug tracking setup
bug_repo = BugRepo()
bug_service = BugService(bug_repo)
bug_controller = BugController(bug_service)

# Routes

# Get everything
@app.route("/api/bugs", methods=["GET"])
def get_bugs():
    return bug_controller.get_all()

# Create bug
@app.route("/api/bugs", methods=["POST"])
def create_bug():
    return bug_controller.create()

# Update bug title / description (#6 user story)
@app.route("/api/bugs/<bug_id>", methods=["PUT", "PATCH"])
def update_bug(bug_id):
    return bug_controller.update(bug_id)

# Update bug status (#13 user story)
@app.route("/api/bugs/<bug_id>/status", methods=["PUT"])
def update_bug_status(bug_id):
    return bug_controller.update_status(bug_id)

# Assign bug to developer
@app.route("/api/bugs/<bug_id>/assign", methods=["POST"])
def assign_bug(bug_id):
    return bug_controller.assign(bug_id)

# Register user
@app.route("/api/users/register", methods=["POST"])
def register_user():
    return user_controller.register()

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        # show registration form
        return render_template("register.html")

    if request.method == "POST":
        # get form data
        username = request.form.get("username")
        password = request.form.get("password")

        ok, message = user_service.register(username, password)

        if ok:
            return f"Registration successful. You can now <a href='/login'>login</a>."
        else:
            return f"Registration failed: {message}"


# Login user
@app.route("/api/users/login", methods=["POST"])
def login_user():
    return user_controller.login()

# Error handling

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        # show login form
        return render_template("login.html")

    if request.method == "POST":
        # read form input
        username = request.form.get("username")
        password = request.form.get("password")

        ok, message = user_service.login(username, password)

        if ok:
            return f"Login successful{username}"
        else:
            return f"Login failed: {message}"

@app.route("/api/bugs/<bug_id>", methods=["DELETE"])
def delete_bug(bug_id):
    return bug_controller.delete(bug_id)



if __name__ == "__main__":
    print("Starting server...")
    print("Bug Tracker API starting...")
    app.run(host="0.0.0.0", port=5001, debug=True)

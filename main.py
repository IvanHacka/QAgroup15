from flask import Flask, jsonify, render_template, request

from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

from backend.services.ScreenshotsServices import ScreenshotsServices
from backend.api.ScreenShots import upload_screenshots

app = Flask(__name__, template_folder="frontend/templates")

bug_repo = BugRepo()
bug_service = BugService(bug_repo)
bug_controller = BugController(bug_service)

# Screenshots service
screenshots_service = ScreenshotsServices(bug_repo)

# Routes

@app.route("/")
def index():
    return render_template("index.html")

# Get everything
@app.route("/api/bugs", methods=["GET"])
def get_bug():
    return bug_controller.get_all()

# Create POST request for bug
@app.route("/api/bugs", methods=["POST"])
def create_bug():
    return bug_controller.create()

# Assign bug to developer
@app.route("/api/bug/<bug_id>/assign", methods=["POST"])
def assign_bug(bug_id):
    return bug_controller.assign(bug_id)

# Upload screenshots for a bug (multipart/form-data)
@app.route("/api/bugs/<bug_id>/screenshots", methods=["POST"])
def upload_bug_screenshots(bug_id):
    return upload_screenshots(request, bug_id, screenshots_service)

# Error handling
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Starting server...")
    print("Bug Tracker API starting...")
    app.run(host="0.0.0.0", port=5001, debug=True)

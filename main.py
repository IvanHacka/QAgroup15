from flask import Flask, jsonify

from backend.controllers.BugController import BugController
from backend.repo.BugRepo import BugRepo
from backend.services.BugService import BugService

app = Flask(__name__)

# Initialize the dependencies thing
bug_repo = BugRepo()
bug_service = BugService(bug_repo)
bug_controller = BugController(bug_service)

# Routes

# Get all bugs
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
    
#for assign bugs
@app.route("/api/bugs/assigned/<int:developer_id>", methods=["GET"])
def get_bugs_assigned_to_developer(developer_id):
    return bug_controller.get_assigned_bugs(developer_id)


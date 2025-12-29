from flask import request, jsonify
from backend.models.Bug import BugPriority, BugStatus, Bug
from backend.services.BugService import BugService


class BugController:
    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service
        
    # P0st
    def create(self):
        try:
            data = request.get_json()
            bug = Bug(
                title=data["title"],
                description=data["description"],
                priority=BugPriority(data["priority"]),
                status=BugStatus(data["status"]),
                tester_id=data.get("tester_id"),
                assigned_to=data.get("assigned_to")
            )

            created = self.bug_service.create_bug(bug)
            return jsonify(created.to_dict()), 201

        except KeyError as e:
            return jsonify({'error': f"Missing required fields {e}"}), 400
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Put
    def update(self, bug_id: str):
        try:
            data = request.get_json() or {}
            title = data.get("title")
            description = data.get("description")

            if title is None and description is None:
                return jsonify({"error": "Nothing to update"}), 400

            updated_bug = self.bug_service.update_bug_details(
                bug_id=bug_id,
                title=title,
                description=description
            )
            return jsonify(updated_bug.to_dict()), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "Server error"}), 500

    # Put statas
    def update_status(self, bug_id: str):
        try:
            data = request.get_json()
            new_status = data.get("status")

            updated_bug = self.bug_service.update_bug_status(
                bug_id, new_status
            )
            return jsonify(updated_bug.to_dict()), 200

        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                return jsonify({"error": msg}), 404
            return jsonify({"error": msg}), 400

        except Exception:
            return jsonify({"error": "Server error"}), 500

    # get bug
    def get_all(self):
        try:
            bugs = self.bug_service.list_bugs()
            return jsonify([bug.to_dict() for bug in bugs]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # get bug id
    def get_one(self, bug_id: str):
        try:
            bug = self.bug_service.get_bug(bug_id)
            return jsonify(bug.to_dict()), 200
        
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
            
        except Exception:
            return jsonify({'error': 'Server error'}), 500

    # POST assigns
    def assign(self, bug_id: str):
        try:
            assigned_to = request.get_json().get('assigned_to')
            if not assigned_to:
                return jsonify({'error': 'Who are you assigning it to'}), 400

            updated = self.bug_service.assign_bug(bug_id, assigned_to)
            return jsonify(updated.to_dict()), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # DELETE 
    def delete(self, bug_id: str):
        try:
            self.bug_service.delete_bug(bug_id)
            return jsonify({"message": "Bug deleted"}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 404

        except Exception:
            return jsonify({"error": "Server error"}), 500

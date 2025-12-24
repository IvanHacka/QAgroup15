from flask import request, jsonify

from backend.models.Bug import BugPriority, BugStatus, Bug
from backend.services.BugService import BugService


class BugController:
    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service

    def create(self):# POST /api/bugs
        try:    
            data = request.get_json()

            bug = Bug( # create bug object from request
                title=data['title'],
                description=data['description'],
                status=BugStatus(data.get('status')),
                priority=BugPriority(data.get('priority')),
                tester_id=data.get('tester_id'),
                assigned_to=data.get('assigned_to'),
                screenshot=data.get('screenshot', []),
            )

            created = self.bug_service.create_bug(bug)
            return jsonify(created.to_dict()), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except KeyError as e:
            return jsonify({'error': f"Missing required fields {e}"}), 400
        except Exception:
            return jsonify({'error': "Server error"}), 500

    
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

    def get_all(self):
        try:
            status = request.args.get('status')
            priority = request.args.get('priority')
            assigned_to = request.args.get('assigned_to')

            bugs = self.bug_service.list_bugs(status, priority, assigned_to)
            return jsonify([bug.to_dict() for bug in bugs]), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    def assign(self, bug_id: str):# POST
        try:
            assigned_to = request.get_json().get('assigned_to')
            if not assigned_to:
                return jsonify({'error': 'Who are you assigning it to'}), 400

            updated = self.bug_service.assign_bug(bug_id, assigned_to)
            return jsonify(updated.to_dict()), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

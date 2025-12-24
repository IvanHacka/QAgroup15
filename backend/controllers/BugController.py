from backend.models.Bug import BugPriority, BugStatus, Bug
from backend.repo.BugRepo import BugRepo
from flask import request, jsonify

from backend.services.BugService import BugService


class BugController:
    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service


    def create(self):
        # POST /api/bugs
        try:
            data = request.get_json()

            # create bug object from request
            bug = Bug(
                title = data['title'],
                description = data['description'],
                status = BugStatus(data.get('status')),
                priority = BugPriority(data.get('priority')),
                tester_id = data.get('tester_id'),
                assigned_to = data.get('assigned_to'),
                screenshot = data.get('screenshot', []),
            )

            created = self.bug_service.create_bug(bug)
            return jsonify(created.to_dict()), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except KeyError as e:
            return jsonify({'error': f"Missing required fields {e}"}), 400
        except Exception as e:
            return jsonify({'error': "Server error"}), 500

    def get_all(self):
        # GET /api/bugs?status=?&priority=?&assigned_to=?
        try:
            status = request.args.get('status')
            priority = request.args.get('priority')
            assigned_to = request.args.get('assigned_to')

            bugs = self.bug_service.list_bugs(status, priority, assigned_to)

            return jsonify([bugs.to_dict() for bugs in bugs]), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    def assign(self, bug_id: str):
        # POST
        try:
            bug = self.bug_service.get_bug(bug_id)
            assigned_to = bug.get('assigned_to')


            if not assigned_to:
                return jsonify({'error': 'Who are you assigning it to'}), 404

            updated = self.bug_service.assign_bug(bug_id, assigned_to)
            return jsonify(updated.to_dict()), 200

        except ValueError as e:
            return jsonify({'error': str(e)}),

    def delete(self, bug_id: str):
        # DELETE /api/bugs/<bug_id>
        try:
            self.bug_service.delete_bug(bug_id)
            return jsonify({"message": "Bug deleted"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception:
            return jsonify({"error": "Server error"}), 500




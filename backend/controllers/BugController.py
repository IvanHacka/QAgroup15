from flask import request, jsonify
from backend.models.Bug import Bug
from backend.services.BugService import BugService


class BugController:
    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service

    def create(self):
        """POST /api/bugs - Creates a bug with auto-generated ID"""
        try:
            # Create bug with auto-generated ID
            bug = Bug()

            created = self.bug_service.create_bug(bug)
            return jsonify(created.to_dict()), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all(self):
        """GET /api/bugs - Get all bugs"""
        try:
            bugs = self.bug_service.list_bugs()
            return jsonify([bug.to_dict() for bug in bugs]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_one(self, bug_id: str):
        """GET /api/bugs/<bug_id> - Get single bug"""
        try:
            bug = self.bug_service.get_bug(bug_id)

            if bug:
                return jsonify(bug.to_dict()), 200
            else:
                return jsonify({'error': 'Bug not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
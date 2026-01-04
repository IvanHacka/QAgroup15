from typing import Optional, List
from backend.models.Bug import Bug, BugPriority, BugStatus
from backend.services.BugService import BugService


class BugController:

    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service

    # create
    def create(
        self,
        title: str,
        description: str,
        priority: str,
        status: str,
        tester_id: Optional[str] = None,
        assigned_to: Optional[List[str]] = None
    ) -> Bug:

        if not title or not description:
            raise ValueError("Title and description are required")

        if assigned_to is None:
            assigned_to = [tester_id] if tester_id else []

        bug = Bug(
            title=title,
            description=description,
            priority=BugPriority[priority.upper()],
            status=BugStatus[status.upper()],
            tester_id=tester_id,
            assigned_to=assigned_to
        )

        return self.bug_service.create_bug(bug)

    # update 
    def update(
        self,
        bug_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Bug:

        if title is None and description is None:
            raise ValueError("Nothing to update")

        return self.bug_service.update_bug_details(
            bug_id=bug_id,
            title=title,
            description=description
        )

    # update status
    def update_status(self, bug_id: str, new_status: str) -> Bug:
        if not new_status:
            raise ValueError("Status cannot be empty")

        return self.bug_service.update_bug_status(bug_id, new_status)

    # assign
    def assign(self, bug_id: str, assigned_to: List[str]) -> Bug:
        return self.bug_service.assign_bug(bug_id, assigned_to)

    # get all
    def get_all(self, search_mode: Optional[str] = None, query=None) -> List[Bug]:
        if not search_mode:
            return self.bug_service.list_bugs()

        mode = search_mode.strip().lower()

        if mode == "person":
            if not isinstance(query, dict):
                raise ValueError("Person search requires a dictionary query")
            return self.bug_service.search_bugs(mode, query)

        if mode == "status":
            if not isinstance(query, dict):
                raise ValueError("Status search requires a dictionary query")
            return self.bug_service.search_bugs(mode, query)

        q = str(query).strip()
        return self.bug_service.search_bugs(mode, q)


    # get one
    def get_one(self, bug_id: str) -> Bug:
        return self.bug_service.get_bug(bug_id)

    # delete 32
    def delete(self, bug_id: str, confirm: bool) -> bool:
        if not confirm:
            return False

        self.bug_service.delete_bug(bug_id)
        return True

    # reopen 30
    def reopen(self, bug_id: str, user: str, reason: str) -> Bug:
        return self.bug_service.reopen_bug(bug_id, user, reason)

    #duplicate
    def mark_duplicate(self, bug_id: str, original_id: str) -> Bug:
        return self.bug_service.mark_duplicate(bug_id, original_id)

    def get_bug(self, bug_id):
        return self.bug_service.get_bug(bug_id)

    def add_comment(self, bug_id: str, user: str, text: str) -> Bug:
        return self.bug_service.add_comment(bug_id, user, text)



from typing import Optional, List
from backend.models.Bug import Bug, BugPriority, BugStatus
from backend.services.BugService import BugService


class BugController:

    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service

    # cretea
    def create(
        self,
        title: str,
        description: str,
        priority: str,
        status: str,
        tester_id: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> Bug:

        if not title or not description:
            raise ValueError("Title and description are required")

        bug = Bug(
            title=title,
            description=description,
            priority=BugPriority[priority.upper()],
            status=BugStatus[status.upper()],
            tester_id=tester_id,
            assigned_to=assigned_to
        )

        return self.bug_service.create_bug(bug)

    # update details
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

    # update stat
    def update_status(self, bug_id: str, new_status: str) -> Bug:
        if not new_status:
            raise ValueError("Status cannot be empty")

        return self.bug_service.update_bug_status(bug_id, new_status)

    # assign bug
    def assign(self, bug_id: str, assigned_to: str) -> Bug:
        return self.bug_service.assign_bug(bug_id, assigned_to)

    # search
    def get_all(
        self,
        search_mode: Optional[str] = None,
        query: Optional[str] = None
    ) -> List[Bug]:

        # No search → list all
        if not search_mode or not query:
            return self.bug_service.list_bugs()

        mode = search_mode.strip().lower()
        q = query.strip()

        if mode not in ("id", "title", "status", "priority"):
            raise ValueError("Invalid search mode")

        return self.bug_service.search_bugs(mode, q)

    #Get One 
    def get_one(self, bug_id: str) -> Bug:
        return self.bug_service.get_bug(bug_id)

    # Delete (User Story #32) 
    def delete(self, bug_id: str, confirm: bool) -> bool:
        if not confirm:
            return False

        self.bug_service.delete_bug(bug_id)
        return True

    # Reopen Bug (User Story #30)
    def reopen(self, bug_id: str, user: str, reason: str) -> Bug:
        return self.bug_service.reopen_bug(bug_id, user, reason)

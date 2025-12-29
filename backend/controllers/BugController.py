from typing import Optional, List

from backend.models.Bug import BugPriority, BugStatus, Bug
from backend.services.BugService import BugService


class BugController:
    """
    Pure Python controller (NO Flask, NO HTTP, NO JSON).
    This controller is designed for CLI usage and testing.
    """

    def __init__(self, bug_service: BugService):
        self.bug_service = bug_service

    # -------- CREATE --------
    def create(
        self,
        title: str,
        description: str,
        priority: str,
        status: str,
        tester_id: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> Bug:
        """
        Create a new bug.
        """
        if not title or not description:
            raise ValueError("Title and description are required")

        bug = Bug(
            title=title,
            description=description,
            priority=BugPriority(priority),
            status=BugStatus(status),
            tester_id=tester_id,
            assigned_to=assigned_to
        )
        return self.bug_service.create_bug(bug)

    # -------- UPDATE DETAILS --------
    def update(
        self,
        bug_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Bug:
        """
        Update bug title and/or description.
        """
        if title is None and description is None:
            raise ValueError("Nothing to update")

        return self.bug_service.update_bug_details(
            bug_id=bug_id,
            title=title,
            description=description
        )

    # -------- UPDATE STATUS --------
    def update_status(self, bug_id: str, new_status: str) -> Bug:
        """
        Update bug status.
        """
        if not new_status:
            raise ValueError("Status cannot be empty")

        return self.bug_service.update_bug_status(bug_id, new_status)

    # -------- ASSIGN BUG --------
    def assign(self, bug_id: str, assigned_to: str) -> Bug:
        """
        Assign bug to a user.
        """
        if not assigned_to:
            raise ValueError("Assigned user cannot be empty")

        return self.bug_service.assign_bug(bug_id, assigned_to)

    # -------- GET ALL / SEARCH --------
    def get_all(
    self,
    search_mode: Optional[str] = None,
    query: Optional[str] = None
) -> List[Bug]:
        
        if not search_mode or not query:
            return self.bug_service.list_bugs()
        
        mode = search_mode.strip().lower()
        
        q = query.strip()

        # ---- SEARCH BY TITLE ----
        if mode == "title":
            return self.bug_service.search_bugs("title", q)

        # ---- SEARCH BY STATUS ----
        elif mode == "status":
            try:
                status = BugStatus[q.upper()]
            except KeyError:
                raise ValueError("Invalid bug status")
            return self.bug_service.search_bugs("status", status)

        elif mode == "priority":
                try:
                    priority = BugPriority[q.upper()]
                except KeyError:
                    raise ValueError("Invalid bug priority")
                return self.bug_service.search_bugs("priority", priority)
        
        else:
                raise ValueError("Invalid search mode")



    # -------- GET ONE --------
    def get_one(self, bug_id: str) -> Bug:
        """
        Get a single bug by ID.
        """
        return self.bug_service.get_bug(bug_id)

    # -------- DELETE (WITH CONFIRMATION) --------
    def delete(self, bug_id: str, confirm: bool) -> bool:
        """
        Delete a bug only if user confirms.
        This method is intentionally designed to be good for symbolic execution.
        """
        if not confirm:
            return False

        self.bug_service.delete_bug(bug_id)
        return True

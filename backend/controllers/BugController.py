from typing import Optional, List

from backend.models.Bug import BugPriority, BugStatus, Bug
from backend.services.BugService import BugService


# ****No more flask****
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
        assigned_to: Optional[str] = None
    ) -> Bug:
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

    # update
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

    # update sattus
    def update_status(self, bug_id: str, new_status: str) -> Bug:
        if not new_status:
            raise ValueError("Status cannot be empty")

        return self.bug_service.update_bug_status(bug_id, new_status)

    def assign(self, bug_id: str, assigned_to: str) -> Bug:
        # Assign a user
        return self.bug_service.assign_bug(bug_id, assigned_to)

    # GET all
    # Search feature
    def get_all(
    self,
    search_mode: Optional[str] = None,
    query: Optional[str] = None
) -> List[Bug]:
        
        if not search_mode or not query:
            return self.bug_service.list_bugs()
        
        mode = search_mode.strip().lower()
        
        q = query.strip()

        # Searhc by title
        if mode == "title":
            return self.bug_service.search_bugs("title", q)

        if mode == "id":
            return self.bug_service.search_bugs("id", q)

        else:
                raise ValueError("Invalid search mode")



    # GET by id
    def get_one(self, bug_id: str) -> Bug:
        return self.bug_service.get_bug(bug_id)

    # DELETE
    # (Confirmation #32)
    def delete(self, bug_id: str, confirm: bool) -> bool:
        self.bug_service.delete_bug(bug_id)
        #add confirmation here
        if not confirm:
            return False
        return True

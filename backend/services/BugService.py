from typing import Optional, List
from datetime import datetime
from backend.models.Bug import Bug, BugStatus, BugPriority
from backend.repo.BugRepo import BugRepo



class BugService:
    def __init__(self, repo: BugRepo):
        self.repo = repo

    def validate_bug(self, bug: Bug) -> Optional[Bug]:
        if not bug.title or len(bug.title) == 0:
            raise ValueError("Bug title is required")
        if len(bug.title) > 200:
            raise ValueError("Bug title can't be exceeding 200 characters")
        if not bug.description or len(bug.description) == 0:
            raise ValueError("Bug description is required")
        if len(bug.description) > 2000:
            raise ValueError("Bug description can't be exceeding 2000 characters")

        if not isinstance(bug.status, BugStatus):
            raise ValueError("Bug status is required")
        if not isinstance(bug.priority, BugPriority):
            raise ValueError("Bug priority is required")


    def get_bug(self, bug_id: str) -> Optional[Bug]:
        if not bug_id:
            raise ValueError("Bug id is required")
        return self.repo.get_by_id(bug_id)

    # for filtering
    def list_bugs(self, status: Optional[str], priority: Optional[str],
                  assigned_to: Optional[str]) -> List[Bug]:
        bugs = self.repo.list(status = status)
        # Add other filtering here


        return bugs


    def create_bug(self, bug: Bug) -> Bug:
        """
        Create a new bug - only ID is saved

        Args:
            bug: Bug object (ID will be auto-generated if not provided)

        Returns:
            Created Bug object with ID

        Raises:
            Exception: If creation fails
        """
        # Update timestamp

        self.validate_bug(bug)
        bug.created_at = datetime.now().isoformat()


        if self.repo.create(bug):
            return bug
        raise Exception(f"Fail to create bug")
    
    def update_bug_details(
            self,
            bug_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
         ) -> Bug:
        
        if not bug_id:
            raise ValueError("Bug id is required")
        
        bug = self.repo.get_by_id(bug_id)
        if not bug:
            raise ValueError("Bug not found")
        
        # update if needed
        if title is not None:
            bug.title = title
        if description is not None:
            bug.description = description
            
        # update time
        bug.updated_at = datetime.now().isoformat()
        
        # re use validation
        self.validate_bug(bug)

        if self.repo.update(bug):
            return bug

        raise Exception("Fail to update bug")

    def get_bug(self, bug_id: str) -> Optional[Bug]:
        """Get a bug by ID"""
        if not bug_id:
            raise ValueError("Bug ID is required")
        return self.repo.get_by_id(bug_id)

    def list_bugs(self) -> List[Bug]:
        """Get all bugs"""
        return self.repo.list()
      

    def count_bugs(self) -> int:
        """Get total number of bugs"""
        return self.repo.count()
            Returns:
                Updated Bug object

    def delete_bug(self, bug_id: str) -> bool:
        deleted = self.repo.delete(bug_id)
        if not deleted:
            raise ValueError("Bug not found")
        return True
      

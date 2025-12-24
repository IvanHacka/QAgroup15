import json
import os
from typing import List, Optional
from backend.models.Bug import Bug, BugStatus, BugPriority


class BugRepo:
    def __init__(self, bug_file:str = "data/Bugs.json"):
        self.bug_file = bug_file
        self.data_dir()

    def data_dir(self):
        # Make one if it doesnt exist
        os.makedirs(os.path.dirname(self.bug_file), exist_ok=True)
        if not os.path.exists(self.bug_file):
            with open(self.bug_file, "w") as f:
                json.dump([], f)

    def read_all(self) -> List[dict]:
        # Read all bugs
        try:
            with open(self.bug_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            print(f"{self.bug_file} corruption detected.")
            return []

    def write_all(self, bugs: List[dict]) -> bool:
        # Write all bugs to the file
        # Using single file approach
        temp_file = self.bug_file + ".temp"
        try:
            with open(temp_file, "w") as f:
                json.dump(bugs, f, indent = 3)

            os.replace(temp_file, self.bug_file)
            return True
        except Exception as e:
            print(e)
            # Free up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def get_by_id(self, bug_id: str) -> Optional[Bug]:
        bugs = self.read_all()
        
        for b in bugs:
            if b["id"] == bug_id:
                return Bug(
                    id=b["id"],
                    title=b["title"],
                    description=b["description"],
                    status=BugStatus(b["status"]),
                    priority=BugPriority(b["priority"]),
                    tester_id=b["tester_id"],
                    screenshot=b.get("screenshot", []),
                    assigned_to=b.get("assigned_to"),
                    created=b.get("created"),
                    updated=b.get("updated"),
                    assigned=b.get("assigned")
                    
                    )
        return None


    # For filter method
    def list(self, status: Optional[str]) -> list[Bug]:
        bugs_data = self.read_all()
        bugs = []

        for b in bugs_data:
            # Apply status filter if provided
            if status and b.get("status") != status:
                continue

            bug = Bug(
    
    id=b["id"],
    title=b["title"],
    description=b["description"],
    status=BugStatus(b["status"]),
    priority=BugPriority(b["priority"]),
    tester_id=b["tester_id"],
    assigned_to=b.get("assigned_to"),
    screenshot=b.get("screenshot", []),
    created=b.get("created"),
    updated=b.get("updated") 
                        )
            
            bugs.append(bug)

        return bugs


    def create(self, bug: Bug) -> bool:
        bugs = self.read_all()
        if any(b["id"] == bug.id for b in bugs):
            print(f"Bug {bug.id} already exists.")
            return False

        bugs.append(bug.to_dict())
        return self.write_all(bugs)

    def update(self, bug: Bug) -> bool:
        bugs = self.read_all()
        for i, b in enumerate(bugs):
            if b["id"] == bug.id:
                bugs[i] = bug.to_dict()
                return self.write_all(bugs)

        print(f"Bug {bug.id} not found.")
        return False

    # Might want to display the total number of bugs
    def count(self) -> int:
        return len(self.read_all())
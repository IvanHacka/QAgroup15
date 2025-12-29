import json
import os
from typing import List, Optional
from backend.models.Bug import Bug, BugStatus, BugPriority


class BugRepo:
    def __init__(self, bug_file: str = "data/Bugs.json"):
        self.bug_file = bug_file
        self.data_dir()

    def data_dir(self):
        # Check if there exist directory
        # Create if not
        os.makedirs(os.path.dirname(self.bug_file), exist_ok=True)
        if not os.path.exists(self.bug_file):
            with open(self.bug_file, "w") as f:
                json.dump([], f)

    # Read all bugs from Bugs.json
    def read_all(self) -> List[dict]:
        try:
            with open(self.bug_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"{self.bug_file} corruption detected.")
            return []

    # Write Bugs.json
    def write_all(self, bugs: List[dict]) -> bool:
        temp_file = self.bug_file + ".temp"
        # backup_file = self.bug_file + ".backup"
        try:
            # Temp file
            with open(temp_file, "w") as f:
                json.dump(bugs, f, indent = 3)

            os.replace(temp_file, self.bug_file)
            return True
        except Exception as e:
            print(f"Error writing bugs: {e}")
            # Remove temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    # Return one bug
    def get_by_id(self, bug_id: str) -> Optional[Bug]:
        bugs = self.read_all()
        
        for b in bugs:
            if b["id"] == bug_id:
                return Bug.parse_from_dict(b)
        return None

    # For filter method
    def list(self) -> list[Bug]:
        bugs_data = self.read_all()
        bugs = []

        for b in bugs_data:
            try:
                # No manaul construction
                bug = Bug.parse_from_dict(b)
                bugs.append(bug)
            except Exception as e:
                print(f"Error parsing bug {b.get('id')}: {e}")
                continue

        return bugs

    def create(self, bug: Bug) -> bool:
        bugs = self.read_all()

        # Check if bug ID already exists
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

    def delete(self, bug_id: str) -> bool:
        bugs = self.read_all()
        new_bugs = [b for b in bugs if b.get("id") != bug_id]
        if len(new_bugs) == len(bugs):
            return False

        return self.write_all(new_bugs)

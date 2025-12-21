import json
import os
from backend.models.Bugs import Bugs, BugStatus

BugFile = "data/Bugs.json"

class BugRepo:
    @staticmethod
    def get_by_id(bug_id) -> Bugs | None:
        with open(BugFile) as f:
            bugs = json.load(f)

        for b in bugs:
            if b["id"] == bug_id:
                return Bugs(
                    id = b["id"],
                    title = b["title"],
                    description = b["description"],
                    status = BugStatus(b["status"]),
                    screenshot = b.get["screenshot", []]
                )
        return None

    @staticmethod
    def save(bug):
        with open(BugFile, "w") as f:
            bugs = json.load(f)
            for b in bugs:
                if b["id"] == bug.id:
                    b["screenshot"] = bug.screenshot
                    temp = BugFile + ".tmp"
                    with open(temp, "w") as f:
                        json.dump(bugs, f, indent=3)

                    os.replace(temp, BugFile)


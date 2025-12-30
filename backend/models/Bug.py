from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
import uuid


class BugPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class BugStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REOPEN = "REOPEN"


@dataclass
class Bug:

    title: str
    description: str

    status: BugStatus = BugStatus.OPEN
    priority: BugPriority = BugPriority.LOW
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    reopen_count: int = 0  #reopen #30

    tester_id: Optional[str] = None
    assigned_to: List[str] = field(default_factory=list)

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = None

    screenshot: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "reopen_count": self.reopen_count,   #reopen #30
            "created_by": self.tester_id,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "screenshot": self.screenshot,
        }


    @staticmethod
    def from_dict(data: dict) -> "Bug":

        # just in case）
        if "title" not in data or "description" not in data:
            raise ValueError("Invalid bug record: missing title or description")

        # status
        try:
            status = BugStatus(data.get("status", "OPEN"))
        except ValueError:
            status = BugStatus.OPEN

        try:
            priority = BugPriority(data.get("priority", "LOW"))
        except ValueError:
            priority = BugPriority.LOW

        return Bug(
    id=data.get("id", str(uuid.uuid4())),
    title=data["title"],
    description=data["description"],
    status=status,
    priority=priority,
    reopen_count=data.get("reopen_count", 0),  # reopen #30 !!
    tester_id=data.get("tester_id"),
    assigned_to=data.get("assigned_to"),
    created_at=data.get("created_at", datetime.now().isoformat()),
    updated_at=data.get("updated_at"),
    screenshot=data.get("screenshot", []),
)


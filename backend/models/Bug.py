from email.mime import image

from backend import models
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid
from PIL import Image

class BugStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class BugPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Bug:
    title: str
    description: str
    status: BugStatus
    priority: BugPriority
    tester_id: int
    developer_id: int
    screenshot: list[str] = field(default_factory=list)
    assigned_to: Optional[int] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    updated: str = field(default_factory=lambda: datetime.now().isoformat())
    assigned: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "tester_id": self.tester_id,
            "developer_id": self.developer_id,
            "screenshot": self.screenshot,
            "assigned_to": self.assigned_to,
            "created": self.created,
            "updated": self.updated,
            "assigned": self.assigned
        }


    @staticmethod
    def parse_from_dict(data: dict) -> "Bug":
        try:
            status = BugStatus(data["status"])
        except ValueError:
            raise ValueError("Invalid bug status")
        return Bug(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            status = status,
            priority = BugPriority(data["priority"]),
            tester_id = data["tester_id"],
            developer_id = data["developer_id"],
            screenshot = data["screenshot"],
            assigned_to = data.get("assigned_to"),
            created = data["created"],
            updated = data["updated"],
            assigned = data["assigned"]
        )

    def validate_image(file_path:str):
        with Image.open(file_path) as img:
            img.verify()
            if img.format not in ["PNG", "JPEG"]:
                raise ValueError("Invalid image format")
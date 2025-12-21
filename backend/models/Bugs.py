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
class Bugs:
    title: str
    description: str
    status: BugStatus
    priority: BugPriority
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created: field(default_factory=lambda: datetime.now().isoformat())
    updated: field(default_factory=lambda: datetime.now().isoformat())
    assigned: field(default_factory=lambda: datetime.now().isoformat())
    tester_id: int
    assigned_to: Optional[str] = None
    developer_id: int
    screenshot: list[str]

    @staticmethod
    def parse_from_dict(data: dict) -> "Bugs":
        try:
            status = BugStatus(data["status"])
        except ValueError:
            raise ValueError("Invalid bug status")
        return Bugs(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            status = status,
            priority = BugPriority(data["priority"]),
            created = data["created"],
            updated = data["updated"],
            assigned = data["assigned"],
            assigned_to = data.get("assigned_to"),
            tester_id = data["tester_id"],
            developer_id = data["developer_id"],
        )

    def validate_image(file_path:str):
        with Image.open(file_path) as img:
            img.verify()
            if img.format not in ["PNG", "JPEG"]:
                raise ValueError("Invalid image format")
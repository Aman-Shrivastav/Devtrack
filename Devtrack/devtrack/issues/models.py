from abc import ABC, abstractmethod
from datetime import datetime


# -------------------------
# Base Class
# -------------------------

class BaseEntity(ABC):

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }


# -------------------------
# Reporter Class
# -------------------------

class Reporter(BaseEntity):

    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):

        if not self.name:
            raise ValueError("Name cannot be empty")

        if '@' not in self.email:
            raise ValueError("Invalid email")


# -------------------------
# Issue Class
# -------------------------

class Issue(BaseEntity):

    ALLOWED_STATUS = [
        "open",
        "in_progress",
        "resolved",
        "closed"
    ]

    ALLOWED_PRIORITY = [
        "low",
        "medium",
        "high",
        "critical"
    ]

    def __init__(
        self,
        id,
        title,
        description,
        status,
        priority,
        reporter_id
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = str(datetime.now())

    def validate(self):

        if not self.title:
            raise ValueError("Title cannot be empty")

        if self.status not in self.ALLOWED_STATUS:
            raise ValueError(
                f"Status must be one of {self.ALLOWED_STATUS}"
            )

        if self.priority not in self.ALLOWED_PRIORITY:
            raise ValueError(
                f"Priority must be one of {self.ALLOWED_PRIORITY}"
            )

    def describe(self):
        return f"{self.title} [{self.priority}]"


# -------------------------
# Critical Issue Subclass
# -------------------------

class CriticalIssue(Issue):

    def describe(self):
        return (
            f"[URGENT] {self.title} "
            f"— needs immediate attention"
        )


# -------------------------
# Low Priority Issue Subclass
# -------------------------

class LowPriorityIssue(Issue):

    def describe(self):
        return (
            f"{self.title} "
            f"— low priority, handle when free"
        )
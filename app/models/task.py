from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime|None]

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"), nullable=True)
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, data):
        is_complete = data.get("is_complete", False)

        return cls(
            title=data["title"],
            description=data["description"],
            completed_at=datetime.now() if is_complete else None,
            goal_id=data.get("goal_id")
        )
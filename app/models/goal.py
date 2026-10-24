from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title

        if self.tasks:
            goal_as_dict["tasks"] = [
                task.to_dict() for task in self.tasks
                ]
        return goal_as_dict

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"])
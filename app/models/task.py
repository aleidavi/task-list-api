from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    
    def to_dict(self):
        if not self.completed_at:
            is_complete = False
        
        else:
            is_complete = True

        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=is_complete,

            goal=self.goal.title if self.goal else None
        )
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            goal_id=task_data.get("goal_id", None)
        )




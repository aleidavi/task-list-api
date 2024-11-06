from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]

    
    def to_dict(self):
        if not self.completed_at:
            is_complete = False
        
        else:
            is_complete = True

        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=is_complete
        )
    



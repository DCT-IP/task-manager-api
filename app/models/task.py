from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(100),
        nullable=False
    )

    completed = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="tasks"
    )
    
    description = Column(
    String(500),
    nullable=True
)
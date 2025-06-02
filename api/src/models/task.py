from database import Base
from enums import TaskStatus
from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class AITask(Base):
    __tablename__ = "ai_tasks"

    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(String, nullable=False)
    status: TaskStatus = Column(SQLAlchemyEnum(TaskStatus))
    created_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="tasks")

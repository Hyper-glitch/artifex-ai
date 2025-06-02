from database import Base
from enums import UserRole
from sqlalchemy import Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True, unique=True)
    first_name = Column(String, nullable=False, unique=True)
    last_name = Column(String, nullable=True, unique=True)
    language_code = Column(String, nullable=True, unique=True)
    role: UserRole = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER)

    tasks = relationship("AITask", back_populates="user")

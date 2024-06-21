from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TaskStatus(Enum):
    New = 0
    ToDo = 1
    InProgress = 2
    InReview = 3
    Implemented = 4


class Task(Base):
    """
    Database Task model.
    """

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    shortname = Column(String(25))
    title = Column(String(100))
    description = Column(String(250))
    project_shortname = Column(String(25))
    target_release = Column(String(250))
    status = Column(String(15))

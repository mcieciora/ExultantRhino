from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Status(Enum):
    New = 0
    Active = 1
    Implemented = 2


class Project(Base):
    """Database Project model."""

    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    shortname = Column(String(25))
    title = Column(String(100))
    description = Column(String(250))


class Release(Base):
    """Database Release model."""

    __tablename__ = "release"
    id = Column(Integer, primary_key=True)
    shortname = Column(String(25))
    title = Column(String(100))
    description = Column(String(250))
    project_shortname = Column(String(25))
    parent = Column(String(25))
    status = Column(String(15))


class Requirement(Base):
    """Database Requirement model."""

    __tablename__ = "requirement"
    id = Column(Integer, primary_key=True)
    shortname = Column(String(25))
    title = Column(String(100))
    description = Column(String(250))
    project_shortname = Column(String(25))
    parent = Column(String(25))
    target_release = Column(String(25))
    children_task = Column(String(15))


class TestCase(Base):
    """Database TestCase model."""

    __tablename__ = "testcase"
    id = Column(Integer, primary_key=True)
    shortname = Column(String(25))
    title = Column(String(100))
    description = Column(String(250))
    project_shortname = Column(String(25))
    parent = Column(String(25))
    target_release = Column(String(25))
    children_task = Column(String(15))


class Bug(Base):
    """Database Bug model."""

    __tablename__ = "bug"
    id = Column(Integer, primary_key=True)
    shortname = Column(String(25))
    title = Column(String(100))
    description = Column(String(250))
    project_shortname = Column(String(25))
    parent = Column(String(25))
    target_release = Column(String(25))
    children_task = Column(String(15))

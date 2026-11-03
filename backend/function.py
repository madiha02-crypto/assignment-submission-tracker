from fastapi import HTTPException
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH="Assigment.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    course = Column(String)
    title = Column(String)
    max_marks = Column(Integer)
    due_at = Column(DateTime, default=datetime.now)
    late_until = Column(DateTime, default=datetime.now)
    created_on = Column(DateTime, default=datetime.now)
  

    
class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    roll_no = Column(Integer)
    link = Column(String)
    Submitted_at = Column(DateTime, nullable=True)
    is_late = Column(Integer)
    marks = Column(Float, nullable=True)
    feedback = Column(String)
    status = Column(Boolean)

Base.metadata.create_all(engine)
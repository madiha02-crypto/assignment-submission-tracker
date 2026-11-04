from fastapi import HTTPException
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH="assignments.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Assignments (Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True )
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
    link = Column(String  )
    Submitted_at = Column(DateTime,nullable=True )  
    is_late = Column(Integer)  
    marks = Column(Float,nullable=True)  
    feedback =Column(String)
    status = Column(Boolean)

Base.metadata.create_all(engine)


def get_all_assignments(course:str):
    session = Session(engine)
    
    assignments = Session.query(assignments).all()
    response = []
    for assignments in Assignments:
            temp_event= {
                "id": Assignments.id,
                "course" :Assignments. course,
                "title": Assignments.title,
                "max_marks":Assignments.  max_marks,
                " due_at": Assignments. due_at,
                "late_until":Assignments.late_until,
                "created_on":Assignments.  created_on
            }
            response.append(temp_event)
            
    Session.close 
    return response

def get_assignments( assignments_id:int):
    session= Session(engine)
    assignments= session.get(Assignments, Assignments.id)
    if not assignments:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )
    response = {   "id":Assignments.id,
                "course" :Assignments. course,
                "title": Assignments.title,
                "max_marks":Assignments.  max_marks,
                " due_at":Assignments. due_at,
                "late_until":Assignments.late_until,
                "created_on":Assignments.  created_on
            }
    
    session.close() 
    return response

def add_new_assignments(course:str ,title: str, max_marks:int, due_at:datetime,late_until: datetime ):

    session = Session(engine)
    new_assigments =Assignments(
    course=course,
    title=title,
    max_marks=max_marks,
    due_at=due_at,
    late_until=late_until

    )
    
    session.add(new_assigments)
    session.commit()

    session.refresh(Assignments)

    response = {"id":Assignments.id,
                "course" :Assignments. course,
                "title": Assignments.title,
                "max_marks":Assignments.  max_marks,
                " due_at":Assignments. due_at,
                "late_until":Assignments.late_until,
                "created_on":Assignments.  created_on
            }
               

    session.close()
    return response

def update_assigments_deadline(assignments_id: int, new_due_at: datetime, new_late_until: datetime):
    with Session(engine) as session:
        assignment = session.get(assignment, assignments_id)
        if assignment is None:
            return None

        assignment.due_at = new_due_at
        assignment.late_until = new_late_until
        session.commit()
        session.refresh(assignment)

        return {
            "id": assignment.id,
            "due_at": assignment.due_at,
            "late_until": assignment.late_until,
        }

    def delete_assignments(assignments_id):
        Session = Session(engine)  
        events = session.get(Assignments,assignments_id)

    if events:
        
        session.delete(assignments)
    session.commit
    session.close

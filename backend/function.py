from fastapi import HTTPException
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime , date

DB_PATH="assignments.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class assigments (Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True )
    course = Column(String)
    title = Column(String)
    max_marks = Column(Integer)
    due_at = Column(DateTime , default=datetime.now)
    late_until = Column(DateTime , default=datetime.now)  
    created_on= Column(DateTime , default=datetime.now)
  

     
class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    assigmentss_id = Column(Integer, ForeignKey("assigments.id"))
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
  assignments = session.query(assignments).all()
   
    response = []
    for assignments in assigments:
        temp_event= {
            "id": assigments.id,
            "course" :assigments. course,
            "title": assigments.title,
            "max_marks":assigments.  max_marks,
            " due_at": assigments. due_at,
            "late_until":assigments.late_until,
            "created_on":assigments.  created_on
        }
        response.append(temp_event)
        
    session.close()
    return response

def get_assigmentss( assigments_id:int):
    session= Session(engine)
    assigments= session.get(assignments, assignments_id)
    if not assignments:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )
    response = {   "id":assignments.id,
                "course" :assignments. course,
                "title": assignments.title,
                "max_marks":assignments.  max_marks,
                " due_at":assignments. due_at,
                "late_until":assignments.late_until,
                "created_on":assignments.  created_on
            }
    
    session.close() # type: ignore
    return response

def add_new_assignments(course:str ,title: str, max_marks:int, due_at:datetime,late_until: datetime ):

    session = Session(engine)
    new_assigments =assigments(
    course=course,
    title=title,
    max_marks=max_marks,
    due_at=due_at,
    late_until=late_until

    )
       
    session.add(new_assignments)
    session.commit()
    session.refresh(assignments)

    response = {
                 "id": assignments.id,
                 "course" :assignments. course,
                 "title": assignments.title,
                 "max_marks":assignments.  max_marks,
                 " due_at": assignments. due_at,
                 "late_until":assignments.late_until,
                 "created_on":assignments.  created_on
             }

    session.close()
    return response

def update_assignments_deadline(assignments_id: int,new_due_at: datetime,new_late_until: datetime):
     session = Session(engine)
     assignments = session.get(assignments, assignments_id)
    
response = {
        "id": assignments.id,
        "due_at":assignments.due_at,
        "late_until": assignments.late_until
    }


Session.close()

     


def delete_assignments(assignments_id):
 session = Session(engine)  
 events = session.get(assigments,assignments_id)

 if events:
    session.delete(assignments)
    session.commit
    session.close

from ctypes import alignment

from fastapi import HTTPException
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH="assignments.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Assigments (Base):
    __tablename__ = "assigments"
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
    assigments_id = Column(Integer, ForeignKey("assigments.id"))
    roll_no = Column(Integer)
    link = Column(String  )
    submitted_at = Column(DateTime,nullable=True )  
    is_late = Column(Boolean, default=False)
    marks = Column(Float,nullable=True)  
    feedback =Column(String)
    status = Column(Boolean)

Base.metadata.create_all(engine)

def get_all_assignments():
        session = Session(engine)
        asssigments = session.query(assigments).all()
    
        response = []
        for assigments in asssigments:
            Submission.assignment_id == asssigments.id + 1
            current_time = datetime.now()

        if current_time < asssigments.due_at:
                say = "open"
        elif current_time <= assigments.late_until:
                say = "late"             
        else:
                say = "closed"
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

def get_assignments( assignments_id:int):
    session= Session(engine)
    assigments= session.get( assigments, assignments_id)
    if not assigments:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"

        )
           
        for submission in submissions:{
        
            "id": submission.id,
            "roll_no": submission.roll_no,
            "link": submission.link,
            "submitted_at": submission.submitted_at,
            "is_late": submission.is_late,
            "marks": submission.marks,
            "feedback": submission.feedback,
            "status": submission.status }
        

        
    response = {   "id": assigments.id,
                "course" :assigments. course,
                "title": assigments.title,
                "max_marks":assigments.  max_marks,
                " due_at": assigments. due_at,
                "late_until":assigments.late_until,
                "created_on":assigments.  created_on
            }
    
    session.close() 
    return response

def add_new_assignments(course:str ,title: str, max_marks:int, due_at:datetime,late_until: datetime ):

    session = Session(engine)
    new_assigments =Assigments(
    course=course,
    title=title,
    max_marks=max_marks,
    due_at=due_at,
    late_until=late_until

    )
       
    session.add(new_assigments)
    session.commit()
    session.refresh(Assigments)

    response = {
                 "id": Assigments.id,
                 "course" :Assigments. course,
                 "title": Assigments.title,
                 "max_marks":Assigments.  max_marks,
                 " due_at": Assigments. due_at,
                 "late_until":Assigments.late_until,
                 "created_on":Assigments.  created_on
             }

    session.close()
    return response





def update_assigments_deadline(assignments_id: int, new_due_at: datetime, new_late_until: datetime):

    session = Session(engine)

    assignment = session.get(Assigments, assignments_id)

    if assignment is None:
        session.close()
        return None

    assignment.due_at = new_due_at
    assignment.late_until = new_late_until

    session.commit()
    session.refresh(assignment)

    response = {
        "id": assignment.id,
        "due_at": assignment.due_at,
        "late_until": assignment.late_until
    }

    session.close()
    return response
       

    
def delete_assigments(assigments_id):
 session = Session(engine)  
 Assigments = session.get(Assigments,assigments_id)

 if Assigments:
    session.delete(Assigments)
    session.commit
    session.close


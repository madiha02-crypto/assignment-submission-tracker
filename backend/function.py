from fastapi import HTTPException
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH="assignments.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class assigments (Base):
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
    assigmentss_id = Column(Integer, ForeignKey("assigments.id"))
    roll_no = Column(Integer)
    link = Column(String  )
    submitted_at = Column(DateTime,nullable=True )  
    is_late = Column(Boolean, default=False)
    marks = Column(Float,nullable=True)  
    feedback =Column(String)
    status = Column(Boolean)

Base.metadata.create_all(engine)


def get_all_assignments(course:str):
    session = Session(engine)
    asssigments = session.query(assigments).all()
   
    response = []
    for assigments in asssigments:
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
    assigments= session.get( assigments, assigments_id)
    if not assigments:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )
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
    new_assigments =assigments(
    course=course,
    title=title,
    max_marks=max_marks,
    due_at=due_at,
    late_until=late_until

    )
       
    session.add(new_assigments)
    session.commit()
    session.refresh(assigments)

    response = {
                 "id": assigments.id,
                 "course" :assigments. course,
                 "title": assigments.title,
                 "max_marks":assigments.  max_marks,
                 " due_at": assigments. due_at,
                 "late_until":assigments.late_until,
                 "created_on":assigments.  created_on
             }

    session.close()
    return response

def update_assigments_deadline(assignments_id: int, new_due_at: datetime, new_late_until: datetime):
    with Session(engine) as session:
        assignment = session.get(Assignment, assignments_id)
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

def delete_assigments(assigments_id):
 session = Session(engine)  
 events = session.get(assigments,assigments_id)

 if events:
    session.delete(assigments)
    session.commit
    session.close

def add_submission(assignment_id, roll_no, link,):

    session = Session(engine) 

    submitted_at = datetime.now()

    is_late = submitted_at > assignment.due_at

    new_submission = Submission(assignment_id=assignment_id,roll_no=roll_no,link=link,submitted_at=submitted_at,is_late=is_late)

    session.add(new_submission)
    session.commit()

    response = {
        "id": new_submission.id,
        "roll_no": new_submission.roll_no,
        "link": new_submission.link,
        "submitted_at": new_submission.submitted_at,
        "is_late": new_submission.is_late
    }

    session.close()
    return response 

# EC9
def get_student_submission(roll_no):

    session = Session(engine)

    submissions = session.query(Submission).filter(Submission.roll_no == roll_no).all()

    if not submissions:
        session.close()
        return None

    assignment = session.query(Assignment).filter(Assignment.id == Submission.assignments_id).first()

    response = {
        "id": Submission.id,
        "roll_no": Submission.roll_no,
        "title": assignment.title,
        "marks": Submission.marks,
        "max_marks": assignment.max_marks,
        "feedback": Submission.feedback
    }

    session.close()   
    return response


# EC10
def get_assignment_report(assignment_id):
    session = Session(engine)

    assignment = session.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment is None:
        session.close()
        return {"message": "Assignment not found"}

    submissions = session.query(Submission).filter(Submission.assignments_id == assignment_id).all()

    number_submitted = len(submissions)

    number_late = sum(1 for submission in submissions if submissions.is_late)

    number_graded = sum(1 for submission in submissions if submissions.marks is not None)

    if number_graded > 0:
        average_marks = sum(submissions.marks for submission in submissions if submissions.marks is not None) / number_graded
    else:
        average_marks = 0

    session.close()

    return {
        "number_submitted": number_submitted,
        "number_late": number_late,
        "number_graded": number_graded,
        "average_marks": average_marks
    }

  
def get_student_submissions(roll_no):

    session = Session(engine)

    student = session.query(Students).filter(Students.roll_no == roll_no).first()

    if student is None:
        session.close()
        return {"message": "Student not found"}

    submissions = session.query(Submission).filter(Submission.roll_no == roll_no).all()

    if not submissions:
        session.close()
        return {"message": "No submissions found"}

    response = []

    for submission in submissions:

        assignment = session.query(Assignment).filter(Assignment.id == submission.assignments_id).first()

        if assignment:
            result = {
                "title": assignment.title,
                "marks": submission.marks,
                "final_marks": submission.marks,
                "feedback": submission.feedback
            }

            response.append(result)

    session.close()
    return response


# EC8

def grade_submission(submission_id: int, marks: float, feedback: str):

        session = Session(engine)

        submission = session.get(Submission, submission_id)

        if submission is None:
            return None

        submission.marks = marks
        submission.feedback = feedback
        submission.status = True

        session.commit()
        session.refresh(submission)

        return {
            "id": submission.id,
            "marks": submission.marks,
            "feedback": submission.feedback,
            "status": submission.status
        }
    



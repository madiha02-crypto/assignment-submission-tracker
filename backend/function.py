from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "assignments.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Assignments(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    course = Column(String)
    title = Column(String)
    max_marks = Column(Integer)
    due_at = Column(DateTime, default=datetime.now)
    late_until = Column(String)
    created_on = Column(DateTime, default=datetime.now)


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    assignments_id = Column(Integer, ForeignKey("assignments.id"))
    roll_no = Column(Integer)
    link = Column(String)
    submitted_at = Column(DateTime, nullable=True)
    is_late = Column(Boolean, default=False)
    marks = Column(Float, nullable=True)
    feedback = Column(String)
    status = Column(Boolean)


Base.metadata.create_all(engine)


# E1
def get_all_assignments(course=None):

    session = Session(engine)

    assignments = session.query(Assignments).all()

    response = []

    for assignment in assignments:

        if course is not None and assignment.course != course:
            continue

        current_time = datetime.now()

        if current_time < assignment.due_at:
            say = "open"
        elif current_time.strftime("%Y-%m-%d") <= assignment.late_until:
            say = "late"
        else:
            say = "closed"

        submission_count = session.query(Submission).filter(
            Submission.assignments_id == assignment.id
        ).count()

        temp_event = {
            "id": assignment.id,
            "course": assignment.course,
            "title": assignment.title,
            "max_marks": assignment.max_marks,
            "due_at": assignment.due_at,
            "late_until": assignment.late_until,
            "created_on": assignment.created_on,
            "submission_count": submission_count,
            "status": say
        }

        response.append(temp_event)

    session.close()

    return response


# E2
def get_assignments(assignments_id: int):

    session = Session(engine)

    assignment = session.get(Assignments, assignments_id)

    if not assignment:
        session.close()
        return None

    submissions = session.query(Submission).filter(
        Submission.assignments_id == assignments_id
    ).all()

    submission_response = []

    for submission in submissions:

        temp_submission = {
            "id": submission.id,
            "roll_no": submission.roll_no,
            "link": submission.link,
            "submitted_at": submission.submitted_at,
            "is_late": submission.is_late,
            "marks": submission.marks,
            "feedback": submission.feedback,
            "status": submission.status
        }

        submission_response.append(temp_submission)

    response = {
        "id": assignment.id,
        "course": assignment.course,
        "title": assignment.title,
        "max_marks": assignment.max_marks,
        "due_at": assignment.due_at,
        "late_until": assignment.late_until,
        "created_on": assignment.created_on,
        "submissions": submission_response
    }

    session.close()

    return response


# E3
def add_new_assignments(course: str, title: str, max_marks: int, late_until: str):

    session = Session(engine)

    new_assignment = Assignments(
        course=course,
        title=title,
        max_marks=max_marks,
        late_until=late_until
    )

    session.add(new_assignment)

    session.commit()

    response = {
        "id": new_assignment.id,
        "course": new_assignment.course,
        "title": new_assignment.title,
        "max_marks": new_assignment.max_marks,
        "due_at": new_assignment.due_at,
        "late_until": new_assignment.late_until,
        "created_on": new_assignment.created_on
    }

    session.close()

    return response


# E4
def update_assignments_deadline(assignments_id: int, new_due_at: datetime, new_late_until: str):

    session = Session(engine)

    assignment = session.get(Assignments, assignments_id)

    if assignment is None:
        session.close()
        return None

    assignment.due_at = new_due_at
    assignment.late_until = new_late_until

    session.commit()

    response = {
        "id": assignment.id,
        "due_at": assignment.due_at,
        "late_until": assignment.late_until
    }

    session.close()

    return response


# E5
def delete_assignments(assignments_id: int):

    session = Session(engine)

    assignment = session.get(Assignments, assignments_id)

    if assignment:

        session.delete(assignment)
        session.commit()
        session.close()

        return {"message": "Assignment deleted successfully"}

    session.close()

    return None


#E6

def submit_work(assignments_id: int, roll_no: int, link: str):

    session = Session(engine)

    assignment = session.get(Assignments, assignments_id)

    if not assignment:
        session.close()
        return None

    current_time = datetime.now()

    if current_time > assignment.due_at:
        say = True
    else:
        say = False

    new_submission = Submission(
        assignments_id=assignments_id,
        roll_no=roll_no,
        link=link,
        submitted_at=current_time,
        is_late=say,
        status=False
    )

    session.add(new_submission)
    session.commit()

    response = {
        "id": new_submission.id,
        "assignments_id": new_submission.assignments_id,
        "roll_no": new_submission.roll_no,
        "link": new_submission.link,
        "submitted_at": new_submission.submitted_at,
        "is_late": new_submission.is_late,
        "status": new_submission.status
    }

    session.close()

    return response

#E7
def resubmit_work(assignments_id: int, roll_no: int, new_link: str):

    session = Session(engine)

    submissions = session.query(Submission).filter(Submission.assignments_id == assignments_id).all()

    submission = None

    for temp in submissions:
        if temp.roll_no == roll_no:
            submission = temp
            break

    if submission is None:
        session.close()
        return None

    assignment = session.get(Assignments, assignments_id)

    if not assignment:
        session.close()
        return None

    current_time = datetime.now()

    if current_time > assignment.due_at:
        say = True
    else:
        say = False

    submission.link = new_link
    submission.submitted_at = current_time
    submission.is_late = say

    session.commit()

    response = {
        "id": submission.id,
        "assignments_id": submission.assignments_id,
        "roll_no": submission.roll_no,
        "link": submission.link,
        "submitted_at": submission.submitted_at,
        "is_late": submission.is_late
    }

    session.close()

    return response

#E8
def grade_submission(submission_id: int, marks: float, feedback: str):

    session = Session(engine)

    submission = session.get(Submission, submission_id)

    if not submission:
        session.close()
        return None

    submission.marks = marks
    submission.feedback = feedback
    submission.status = True

    session.commit()

    response = {
        "id": submission.id,
        "roll_no": submission.roll_no,
        "marks": submission.marks,
        "feedback": submission.feedback,
        "status": submission.status
    }

    session.close()

    return response

#E9

def get_student_submissions(roll_no: int):

    session = Session(engine)

    submissions = session.query(Submission).filter(Submission.roll_no == roll_no).all()

    response = []

    for submission in submissions:

        assignment = session.get(Assignments,submission.assignments_id)

        if assignment:

            temp_event = {
                "assignment_id": assignment.id,
                "title": assignment.title,
                "marks": assignment.max_marks,
                "final_marks": submission.marks,
                "feedback": submission.feedback
            }

            response.append(temp_event)

    session.close()

    return response

#E10

def get_assignment_report(assignments_id: int):

    session = Session(engine)

    assignment = session.get(Assignments, assignments_id)

    if not assignment:
        session.close()
        return None

    submissions = session.query(Submission).filter(Submission.assignments_id == assignments_id).all()

    submitted = 0
    late = 0
    graded = 0
    total_marks = 0

    for submission in submissions:

        submitted += 1

        if submission.is_late:
            late += 1

        if submission.status:
            graded += 1

            if submission.marks is not None:
                total_marks += submission.marks

    if graded > 0:
        average_marks = total_marks / graded
    else:
        average_marks = 0

    response = {
        "assignment_id": assignment.id,
        "title": assignment.title,
        "number_submitted": submitted,
        "number_late": late,
        "number_graded": graded,
        "average_final_marks": average_marks
    }

    session.close()

    return response
    



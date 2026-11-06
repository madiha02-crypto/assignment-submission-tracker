
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import function


app = FastAPI(
    title = "Assignment-Tracker"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# E1
@app.get("/assignments")
def get_all_assignments(course: str = None):

    return function.get_all_assignments(course=course)


# E2
@app.get("/assignments/{assignment_id}")
def get_assignment(assignment_id: int):

    response = function.get_assignments(assignments_id=assignment_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return response


# E3
@app.post("/assignments")
def create_assignment(assignment: int):
    return function.create_assignment(assignment)

    return function.add_new_assignments(
        course=course,
        title=title,
        max_marks=max_marks,
        late_until=late_until
    )


# E4
@app.patch("/assignments/{assignment_id}/deadline")
def extend_deadline(assignment_id: int, due_time: datetime, late_until: str):

    response = function.update_assignments_deadline(
        assignments_id=assignment_id,
        new_due_at=due_time,
        new_late_until=late_until
    )

    if response is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return response


# E5
@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int):

    response = function.delete_assignments(assignments_id=assignment_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return response




# sanika functions api
@app.post("/assignments/{assignment_id}/submissions")
def submit_work(assignment_id: int, roll_number: int, link: str):

    response = function.submit_work(
        assignments_id=assignment_id,
        roll_no=roll_number,
        link=link
    )

    if response is None:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return response

@app.patch("/assignments/{assignment_id}/submissions")
def resubmit_work(
    assignment_id: int,
    roll_number: str,
    link: str
):
    return function.resubmit_work(
        assignment_id=assignment_id,
        roll_number=roll_number,
        link=link
    )

@app.patch("/submissions/{submission_id}/grade")
def grade_submission(
    submission_id: int,
    marks: float,
    feedback: str
):
    return function.grade_submission(
        submission_id=submission_id,
        marks=marks,
        feedback=feedback
    )

@app.get("/students/{roll_number}/submissions")
def get_student_submissions(roll_number: int):
    return function.get_student_submissions(
        roll_number=roll_number
    )

@app.get("/assignments/{assignment_id}/report")
def get_assignment_report(assignment_id: int):
    return function.get_assignment_report(
        assignment_id=assignment_id
    )

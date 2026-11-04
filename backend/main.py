from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from backend import function

app = FastAPI(
    title = "Assignment-Tracker"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)
@app.get("/assignments")
def get_all_assignments(course_id: int):
    return function.get_all_assignments(course_id=course_id)

@app.get("/assignments/{assignment_id}")
def get_assignment(assignment_id: int):
    return function.get_assignment(assignment_id=assignment_id)

@app.post("/assignments")
def create_assignment(assignment: dict):
    return function.create_assignment(assignment)

@app.patch("/assignments/{assignment_id}/deadline")
def extend_deadline(
    assignment_id: int,
    due_time: datetime,
    late_until: datetime
):
    return function.extend_deadline(
        assignment_id=assignment_id,
        due_time=due_time,
        late_until=late_until
    )
@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int):
    return function.delete_assignment(assignment_id=assignment_id)

@app.post("/assignments/{assignment_id}/submissions")
def submit_work(
    assignment_id: int,
    roll_number: str,
    link: str,
):
    return function.submit_work(
        assignment_id=assignment_id,
        roll_number=roll_number,
        link=link
    )

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
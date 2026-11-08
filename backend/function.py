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


def resubmit_work(assignments_id: int, roll_no: int, new_link: str):

    session = Session(engine)

    submissions = session.query(Submission).filter(
        Submission.assignments_id == assignments_id
    ).all()

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


def get_student_submissions(roll_no: int):

    session = Session(engine)

    submissions = session.query(Submission).filter(
        Submission.roll_no == roll_no
    ).all()

    response = []

    for submission in submissions:

        assignment = session.get(
            Assignments,
            submission.assignments_id
        )

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


def get_assignment_report(assignments_id: int):

    session = Session(engine)

    assignment = session.get(Assignments, assignments_id)

    if not assignment:
        session.close()
        return None

    submissions = session.query(Submission).filter(
        Submission.assignments_id == assignments_id
    ).all()

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

import { useState } from 'react'

function App() {
}import { useState, useEffect } from "react";
import BrowseAssignments from "./components/BrowseAssignments";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [assignments, setAssignments] = useState([]);
  const [assignment, setAssignment] = useState(null);
  const [mySubmissions, setMySubmissions] = useState([]);
  const [report, setReport] = useState(null);

  // Use this to display API error and success messages
  const [message, setMessage] = useState("");

  // E1 gets all assignments, with optional course filter
  function getAssignments(course) {
    setMessage("");

    const courseFilter = course ? "?course=" + course : "";

    fetch(API_URL + "/assignments" + courseFilter)
      .then((response) => response.json())
      .then((data) =>
        data.detail ? setMessage(data.detail) : setAssignments(data)
      );
  }

  // E1 shows all assignments when page loads
  useEffect(() => {
    getAssignments();
  }, []);

  // E2 gets one assignment with its submissions
  function getAssignment(id) {
    setMessage("");

    fetch(API_URL + "/assignments/" + id)
      .then((response) => response.json())
      .then((data) =>
        data.detail ? setMessage(data.detail) : setAssignment(data)
      );
  }

  // E3 creates a new assignment
  function addAssignment(course, title, maxMarks, dueAt, lateUntil) {
    setMessage("");

    fetch(API_URL + "/assignments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course: course,
        title: title,
        max_marks: Number(maxMarks),
        due_at: dueAt,
        late_until: lateUntil,
      }),
    })
      .then((response) => response.json())
      .then((data) =>
        data.detail
          ? setMessage(data.detail)
          : setMessage("Assignment created successfully!")
      )
      .then(() => getAssignments());
  }

  // E4 extends assignment deadline
  function extendDeadline(id, newDueAt, newLateUntil) {
    setMessage("");

    fetch(API_URL + "/assignments/" + id + "/deadline", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        new_due_at: newDueAt,
        new_late_until: newLateUntil,
      }),
    })
      .then((response) => response.json())
      .then((data) =>
        data.detail ? setMessage(data.detail) : getAssignment(id)
      )
      .then(() => getAssignments());
  }

  // E5 deletes an assignment
  function deleteAssignment(id) {
    setMessage("");

    fetch(API_URL + "/assignments/" + id, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) =>
        data.detail
          ? setMessage(data.detail)
          : setMessage("Assignment deleted successfully!")
      )
      .then(() => {
        setAssignment(null);
        getAssignments();
      });
  }

  // E6 submits work
  function submitWork(assignmentId, rollNo, link) {
    setMessage("");

    fetch(API_URL + "/assignments/" + assignmentId + "/submissions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        roll_no: Number(rollNo),
        link: link,
      }),
    })
      .then((response) => response.json())
      .then((data) =>
        data.detail
          ? setMessage(data.detail)
          : setMessage("Work submitted successfully!")
      )
      .then(() => {
        getAssignments();
        getAssignment(assignmentId);
      });
  }

  // E7 resubmits work with a new link
  function resubmitWork(submissionId, rollNo, link) {
    setMessage("");

    fetch(API_URL + "/submissions/" + submissionId + "/resubmit", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        roll_no: Number(rollNo),
        link: link,
      }),
    })
      .then((response) => response.json())
      .then((data) =>
        data.detail
          ? setMessage(data.detail)
          : setMessage("Work resubmitted successfully!")
      )
      .then(() => getMyWork(rollNo));
  }

  // E8 grades a submission
  function gradeSubmission(submissionId, marks, feedback) {
    setMessage("");

    fetch(API_URL + "/submissions/" + submissionId + "/grade", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        marks: Number(marks),
        feedback: feedback,
      }),
    })
      .then((response) => response.json())
      .then((data) =>
        data.detail
          ? setMessage(data.detail)
          : setMessage("Submission graded successfully!")
      )
      .then(() => {
        if (assignment) {
          getAssignment(assignment.id);
          getReport(assignment.id);
        }
      });
  }

  // E9 gets one student's submissions
  function getMyWork(rollNo) {
    setMessage("");

    fetch(API_URL + "/students/" + rollNo + "/submissions")
      .then((response) => response.json())
      .then((data) =>
        data.detail ? setMessage(data.detail) : setMySubmissions(data)
      );
  }

  // E10 gets assignment report
  function getReport(id) {
    setMessage("");

    fetch(API_URL + "/assignments/" + id + "/report")
      .then((response) => response.json())
      .then((data) =>
        data.detail ? setMessage(data.detail) : setReport(data)
      );
  }

  return (
    <div>
      <h1>Assignment Submission Tracker</h1>

      {message && <p>{message}</p>}

      <BrowseAssignments
        assignments={assignments}
        getAssignments={getAssignments}
        getAssignment={getAssignment}
        submitWork={submitWork}
      />

      {/* 
        Other components will be added here:

        MyWork
        TeacherDashboard

        Pass the functions as props to those components.
      */}
    </div>
  );
}

export default App;


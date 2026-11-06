
import { useState, useEffect } from "react";


const API_URL = "http://127.0.0.1:8001";

function App() {
  const [assignments, setAssignments] = useState([]);
  const [assignment, setAssignment] = useState(null);
  const [mySubmissions, setMySubmissions] = useState([]);
  const [report, setReport] = useState(null);
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
      body: JSON.stringify({
        course: course,
        title: title,
        max_marks:(maxMarks),
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
  <>
    <h1>Assignment Submission Tracker</h1>
    <p>{message}</p>

    <assignments
      assignments={assignments}
      getAssignments={getAssignments}
      getAssignment={getAssignment}
    />

    <Teacher
      assignments={assignments}
      assignment={assignment}
      addAssignment={addAssignment}
      extendDeadline={extendDeadline}
      deleteAssignment={deleteAssignment}
    />
  </>
}

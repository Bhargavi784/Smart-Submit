// js/classroom.js

const urlParams = new URLSearchParams(window.location.search);
const classroomId = urlParams.get("id");

document.addEventListener("DOMContentLoaded", () => {
  if (!classroomId) {
    alert("No classroom selected.");
    window.location.href = "dashboard.html";
    return;
  }
  loadClassroom();
  loadAssignments();
});

async function loadClassroom() {
  // we don't have /classrooms/{id}, so we re-use /classrooms/joined and filter
  const res = await apiFetch("/classrooms/joined");
  if (!res.ok) {
    alert("Error loading classroom");
    return;
  }
  const list = await res.json();
  const classroom = list.find(c => String(c.id) === String(classroomId));
  if (!classroom) {
    alert("Classroom not found.");
    window.location.href = "dashboard.html";
    return;
  }

  document.getElementById("classroom-title").innerText = classroom.name || "Classroom";

  const role = localStorage.getItem("role");
  if (role === "teacher") {
    document.getElementById("teacher-actions").classList.remove("hidden");
  } else {
    document.getElementById("student-actions").classList.remove("hidden");
  }
}

async function loadAssignments() {
  const container = document.getElementById("assignments");
  container.innerHTML = "<p class='text-gray-500'>Loading assignments...</p>";

  const role = localStorage.getItem("role");
  let endpoint;
  if (role === "teacher") {
    endpoint = `/assignments/teacher/${classroomId}`;
  } else {
    endpoint = `/assignments/classroom/${classroomId}`;
  }

  const res = await apiFetch(endpoint);
  if (!res.ok) {
    container.innerHTML = "<p>No assignments found.</p>";
    return;
  }

  const list = await res.json();
  window._currentAssignments = list; // for student "Submit Report" button

  if (!list.length) {
    container.innerHTML = "<p>No assignments posted yet.</p>";
    return;
  }

  container.innerHTML = "";
  list.forEach(a => {
    const div = document.createElement("div");
    div.className = "p-4 border rounded-lg shadow";

    const role = localStorage.getItem("role");
    let actionBtn = "";

    if (role === "student") {
      // student: go to submission page for this assignment
      actionBtn = `
<button onclick="openAssignment(${a.id})"

  class="mt-2 bg-blue-600 text-white px-3 py-1 rounded">
  View Submissions
</button>
`;

    } else {
      // teacher: later can use for viewing submissions
      actionBtn = `
        <button onclick="viewSubmissions(${a.id})"
          class="mt-2 bg-blue-600 text-white px-3 py-1 rounded">
          View Submissions
        </button>
      `;
    }

    div.innerHTML = `
      <h3 class="font-semibold">${a.title}</h3>
      <p class="text-sm text-gray-600">${a.description || ""}</p>
      ${actionBtn}
    `;

    container.appendChild(div);
  });
}

function showCreateAssignment() {
  // you can make a separate page or modal; for now just redirect with classroomId
  window.location.href = `create_assignment.html?id=${classroomId}`;
}

// Student "Submit Report" button at top
function goToSubmissionPage() {
  const list = window._currentAssignments || [];
  if (!list.length) {
    alert("No assignments available yet.");
    return;
  }
  if (list.length > 1) {
    alert("Please use the 'Submit / View feedback' button under the specific assignment.");
    return;
  }
  const aId = list[0].id;
  openAssignment(aId);
}

function openAssignment(assignmentId) {
  window.location.href = `submission.html?assignmentId=${assignmentId}&classroomId=${classroomId}`;
}

// placeholder for teacher action
function viewSubmissions(assignmentId) {
  alert(`Later you can show submissions list for assignment ${assignmentId}`);
}
function goToTeacherSubmissions(assignmentId) {
  window.location.href = `teacher_submissions.html?classroomId=${classroomId}&assignmentId=${assignmentId}`;
}
function showAssignments() {
  loadAssignments();
}

function viewSubmissionsPage() {
  window.location.href = `teacher_submissions.html?classroomId=${classroomId}`;
}

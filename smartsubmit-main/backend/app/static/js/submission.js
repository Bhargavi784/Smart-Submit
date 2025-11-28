// js/submission.js

async function uploadSubmission() {
  const assignmentId = new URLSearchParams(window.location.search).get("assignmentId");
  const classroomId = new URLSearchParams(window.location.search).get("classroomId");

  if (!assignmentId || !classroomId) {
    alert("Assignment or classroom missing.");
    return;
  }

  const fileInput = document.getElementById("pdfFile");
  if (!fileInput.files.length) {
    alert("Please select a PDF file.");
    return;
  }

  const formData = new FormData();
  formData.append("assignment_id", assignmentId);
  formData.append("classroom_id", classroomId);
  formData.append("file", fileInput.files[0]);

  const res = await fetch(`${API_BASE}/submissions/submit`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
    body: formData
  });

  if (!res.ok) {
    document.getElementById("status").innerText = "Upload failed.";
    return;
  }

  const data = await res.json();
  document.getElementById("feedback").classList.remove("hidden");
  document.getElementById("status").innerText = "Submitted successfully! AI feedback generated.";

  renderFeedback(data);

  // 👉 Enable submit-to-teacher button after AI check
  document.getElementById("submitToTeacher").classList.remove("hidden");
  localStorage.setItem("latest_submission_id", data.id);
}



function renderFeedback(data) {
  // ---------- Margin Check ----------
  const marginDiv = document.getElementById("marginResult");
  marginDiv.innerHTML = `
    <p class="font-semibold">Formatting Status: 
      <span class="${data.margin_report.format_ok ? 'text-green-600' : 'text-red-600'}">
        ${data.margin_report.format_ok ? "PASS ✔️" : "FAILED ❌"}
      </span>
    </p>
    <ul class="list-disc ml-6 mt-2">
      ${(data.margin_report.report || []).map(r => `<li>${r}</li>`).join("")}
    </ul>
  `;

  // ---------- Grammar Check ----------
  const grammarBox = document.getElementById("grammarList");
  let feedback = data.feedback;

  if (!feedback) {
    grammarBox.innerHTML = "<li>No feedback available.</li>";
    return;
  }

  if (typeof feedback === "string") {
    try { feedback = JSON.parse(feedback); } catch {}
  }

  let grammarIssues = [];

  if (Array.isArray(feedback)) grammarIssues = feedback;
  else if (feedback.summary && Array.isArray(feedback.summary)) grammarIssues = feedback.summary;
  else grammarIssues = ["⚠️ Unexpected feedback format."];

  grammarBox.innerHTML = grammarIssues.map(issue => `<li>${issue}</li>`).join("");

  // Show Teacher Grade if available
  if (data.grade || data.teacher_feedback) renderTeacherGrade(data);
}



// ---------------- STUDENT FINAL SUBMIT -----------------

async function submitToTeacher() {
  const submissionId = localStorage.getItem("latest_submission_id");
  if (!submissionId) {
    alert("Please upload assignment first.");
    return;
  }

  alert("✔️ Submitted to teacher successfully!");
}



// ---------------- SHOW TEACHER'S RESPONSE -----------------
async function loadTeacherResponse() {
  const assignmentId = new URLSearchParams(window.location.search).get("assignmentId");

  const res = await apiFetch(`/submissions/my`);
  if (!res.ok) return;

  const submissions = await res.json();
  const match = submissions.find(s => s.assignment_id == assignmentId);

  if (match && (match.grade || match.feedback)) {
    document.getElementById("teacherResponse").classList.remove("hidden");
    renderTeacherGrade(match);
  }
}

function renderTeacherGrade(data) {
  const box = document.getElementById("teacherGradeBox");
  box.innerHTML = `
    <p><b>Grade:</b> ${data.grade ?? "Not graded yet"}</p>
    <p><b>Teacher Feedback:</b> ${data.feedback ?? "-"}</p>
  `;
}
document.addEventListener("DOMContentLoaded", loadExistingSubmission);

async function loadExistingSubmission() {
  const assignmentId = new URLSearchParams(window.location.search).get("assignmentId");

  const res = await apiFetch(`/submissions/student/${assignmentId}`);
  if (!res.ok) return; // means no submission exists yet

  const data = await res.json();
  document.getElementById("feedback").classList.remove("hidden");
  document.getElementById("status").innerText = "You already submitted. Below is your report:";

  renderFeedback(data);

  if (data.grade !== null) {
    document.getElementById("teacher-feedback").innerHTML = `
      <p class="font-semibold text-blue-600">Teacher Feedback</p>
      <p><strong>Grade:</strong> ${data.grade}</p>
      <p><strong>Comment:</strong> ${data.feedback}</p>
    `;
    document.getElementById("teacher-feedback").classList.remove("hidden");
  }
}

const urlParams = new URLSearchParams(window.location.search);
const classroomId = urlParams.get("classroomId");

document.addEventListener("DOMContentLoaded", loadSubmissions);

async function loadSubmissions() {
  const container = document.getElementById("submissions-container");

  const res = await apiFetch(`/submissions/classroom/${classroomId}`);
  if (!res.ok) {
    container.innerHTML = "<p class='text-red-500'>Failed to load submissions</p>";
    return;
  }

  const list = await res.json();
  if (!list.length) {
    container.innerHTML = "<p class='text-gray-500'>No submissions yet.</p>";
    return;
  }

  container.innerHTML = "";
  list.forEach(s => {
    const div = document.createElement("div");
    div.className = "bg-white p-4 rounded-lg shadow";

    div.innerHTML = `
      <p><b>Student ID:</b> ${s.student_id}</p>
      <p><b>Submitted:</b> ${new Date(s.submitted_at).toLocaleString()}</p>
      <p><b>Margin Result:</b> ${JSON.stringify(s.margin_report)}</p>
      <p><b>AI Feedback:</b> ${typeof s.feedback === "object" ? JSON.stringify(s.feedback, null, 2) : s.feedback}</p>

      <div class="mt-3 flex gap-4">
        <a href="${API_BASE}/submissions/download/${s.id}" 
           class="bg-blue-600 text-white px-3 py-1 rounded"
           target="_blank">
          📎 Download File
        </a>
      </div>

      <div class="mt-4">
        <label class="block text-gray-600 text-sm">Grade</label>
        <input id="grade-${s.id}" type="number" min="0" max="100" class="border p-2 rounded w-32">

        <label class="block text-gray-600 text-sm mt-2">Feedback</label>
        <textarea id="feedback-${s.id}" class="border p-2 rounded w-full" rows="3"></textarea>

        <button onclick="submitGrade(${s.id})" 
          class="mt-3 bg-green-600 text-white px-4 py-2 rounded">
          Submit Grade
        </button>
      </div>
    `;

    container.appendChild(div);
  });
}

async function submitGrade(submissionId) {
  const grade = document.getElementById(`grade-${submissionId}`).value;
  const feedback = document.getElementById(`feedback-${submissionId}`).value;

  if (!grade) return alert("Enter grade");

  const formData = new FormData();
  formData.append("grade", grade);
  formData.append("feedback", feedback);

  const res = await fetch(`${API_BASE}/submissions/grade/${submissionId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    },
    body: formData
  });

  if (res.ok) alert("Grade submitted successfully!");
  else alert("Failed to submit grade");
}

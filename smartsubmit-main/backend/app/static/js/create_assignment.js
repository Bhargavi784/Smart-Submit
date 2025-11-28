const urlParams = new URLSearchParams(window.location.search);
const classroomId = urlParams.get("id");

async function createAssignment() {
  const title = document.getElementById("title").value.trim();
  const description = document.getElementById("description").value.trim();

  if (!title) return alert("Title required");

  const res = await apiFetch("/assignments/create", {
    method: "POST",
    body: {
      classroom_id: Number(classroomId),
      title,
      description
    }
  });

  const msgBox = document.getElementById("msg");

  if (!res.ok) {
    msgBox.innerHTML = "❌ Failed: " + await res.text();
    msgBox.className = "mt-3 text-red-600";
    return;
  }

  msgBox.innerHTML = "✅ Assignment created!";
  msgBox.className = "mt-3 text-green-600";

  setTimeout(() => {
    window.location.href = `classroom.html?id=${classroomId}`;
  }, 1000);
}

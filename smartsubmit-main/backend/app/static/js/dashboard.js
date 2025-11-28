// js/dashboard.js
document.addEventListener("DOMContentLoaded", initDashboard);

function initDashboard(){
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");
  if (!token) {
    window.location.href = "index.html";
    return;
  }
  document.getElementById("role-badge").innerText = role?.toUpperCase() || "";
  document.getElementById("welcome").innerText = (role === "teacher") ? "Teacher Dashboard" : "Student Dashboard";

  if (role === "teacher") document.getElementById("createBtn").classList.remove("hidden");
  else document.getElementById("joinBtn").classList.remove("hidden");

  // wire buttons
  document.getElementById("createBtn").addEventListener("click", ()=> {
    document.getElementById("createForm").classList.toggle("hidden");
    document.getElementById("joinForm").classList.add("hidden");
  });
  document.getElementById("joinBtn").addEventListener("click", ()=> {
    document.getElementById("joinForm").classList.toggle("hidden");
    document.getElementById("createForm").classList.add("hidden");
  });

  document.getElementById("createSubmit").addEventListener("click", createClassroomHandler);
  document.getElementById("joinSubmit").addEventListener("click", joinClassroomHandler);

  loadClassrooms();
}

async function createClassroomHandler(){
  const name = document.getElementById("class-name").value.trim();
  const desc = document.getElementById("class-desc").value.trim();
  if (!name) { alert("Enter a class name"); return; }
  try {
    const res = await apiFetch("/classrooms/create", {
      method: "POST",
      body: { name, description: desc }
    });
    if (!res.ok) {
      const txt = await res.text();
      alert("Create failed: " + txt);
      return;
    }
    const data = await res.json();
    document.getElementById("createMsg").innerText = `Created. Join code: ${data.join_code}`;
    loadClassrooms();
  } catch (err) {
    console.error(err);
    alert("Error creating classroom");
  }
}

async function joinClassroomHandler(){
  const code = document.getElementById("join-code").value.trim();
  if (!code) return alert("Enter join code");
  try {
    const res = await apiFetch("/classrooms/join", { method: "POST", body: { join_code: code }});
    if (!res.ok) {
      const txt = await res.text();
      alert("Join failed: " + txt);
      return;
    }
    document.getElementById("joinMsg").innerText = "Joined classroom!";
    loadClassrooms();
  } catch (err) {
    console.error(err);
    alert("Error joining classroom");
  }
}

async function loadClassrooms() {
  const container = document.getElementById("classroom-container");
  container.innerHTML = "<p class='col-span-full text-center text-gray-500'>Loading classrooms...</p>";
  try {
    // ✅ correct endpoint from your backend
    const res = await apiFetch("/classrooms/joined");
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || "Failed to load");
    }

    const classes = await res.json();
    console.log("Classes:", classes);
    container.innerHTML = "";
    if (!Array.isArray(classes) || classes.length === 0) {
      container.innerHTML = "<p class='col-span-full text-center text-gray-500'>No classrooms yet.</p>";
      return;
    }

    classes.forEach(cls => {
      const card = document.createElement("div");
      card.className = "bg-white p-4 rounded shadow hover:shadow-md cursor-pointer";
      card.innerHTML = `
        <h3 class="font-semibold text-blue-600">${escapeHtml(cls.name)}</h3>
        <p class="text-sm text-gray-600">${escapeHtml(cls.description || "")}</p>
        <p class="text-sm text-gray-500 mt-2">
          ${cls.students_count ?? 0} students • ${cls.assignments_count ?? 0} assignments
        </p>
      `;
      card.addEventListener("click", ()=>{
  window.location.href = `classroom.html?id=${cls.id}`;
});

      container.appendChild(card);
    });
  } catch (err) {
    console.error("loadClassrooms error:", err);
    container.innerHTML = "<p class='col-span-full text-center text-red-500'>Failed to load classrooms. Check console.</p>";
  }
}
// small helper to avoid injecting dangerous HTML
function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str).replace(/[&<>"']/g, (s) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[s]));
}

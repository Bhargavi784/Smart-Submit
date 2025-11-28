// js/auth.js
// depends on utils.js being loaded first
async function login() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;

  if (!email || !password) { alert("Email and password required"); return; }

  try {
    const res = await apiFetch("/auth/login", {
      method: "POST",
      body: { email, password }
    });

    if (!res.ok) {
      const txt = await res.text();
      alert("Login failed: " + txt);
      return;
    }

    const data = await res.json();
    if (!data.access_token) { alert("Login returned no token"); return; }
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", role);
    window.location.href = "dashboard.html";
  } catch (err) {
    console.error("Error during login:", err);
    alert("Could not reach server. Make sure backend is running.");
  }
}

function showSignup(){
  document.getElementById("login-card").classList.add("hidden");
  document.getElementById("signup-card").classList.remove("hidden");
}
function showLogin(){
  document.getElementById("signup-card").classList.add("hidden");
  document.getElementById("login-card").classList.remove("hidden");
}

async function signup() {
  const name = document.getElementById("su-name").value.trim();
  const email = document.getElementById("su-email").value.trim();
  const password = document.getElementById("su-password").value;
  const role = document.getElementById("su-role").value;

  if (!name || !email || !password) { alert("All fields required"); return; }

  try {
    const res = await apiFetch("/auth/signup", {
      method: "POST",
      body: { name, email, password, role }
    });

    if (!res.ok) {
      const txt = await res.text();
      alert("Signup failed: " + txt);
      return;
    }
    alert("Signup successful — please login.");
    showLogin();
  } catch (err) {
    console.error("Error during signup:", err);
    alert("Error connecting to server. Make sure backend is running.");
  }
}

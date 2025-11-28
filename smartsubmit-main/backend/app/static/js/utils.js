// js/utils.js
// Single place for API base — update if your backend runs on a different host/port
const API_BASE = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}
function getRole() {
  return localStorage.getItem("role");
}

// wrapper that always logs and returns Response
async function apiFetch(path, opts = {}) {
  const token = getToken();
  opts.headers = opts.headers || {};

  if (token) opts.headers["Authorization"] = `Bearer ${token}`;

  // If body present and not FormData, JSON stringify it
  if (opts.body && !(opts.body instanceof FormData)) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(opts.body);
  }

  const url = `${API_BASE}${path}`;
  console.debug("apiFetch:", url, opts);
  try {
    const res = await fetch(url, opts);
    return res;
  } catch (err) {
    console.error("Network error fetching", url, err);
    throw err;
  }
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("classroom_id");
  localStorage.removeItem("assignment_id");
  window.location.href = "index.html";
}

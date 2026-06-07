const API_BASE = "http://localhost:8000/api/v1";

function logResponse(data) {
    const logDiv = document.getElementById("response-log");
    logDiv.innerText = JSON.stringify(data, null, 2) + "\n\n" + logDiv.innerText;
}

function updateUI() {
    const token = localStorage.getItem("access_token");
    if (token) {
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("dashboard-section").classList.remove("hidden");
    } else {
        document.getElementById("auth-section").classList.remove("hidden");
        document.getElementById("dashboard-section").classList.add("hidden");
    }
}

async function register() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, full_name: "Test User" })
        });
        const data = await res.json();
        logResponse({ endpoint: "/auth/register", status: res.status, data });
        
        if (res.ok && data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            updateUI();
        }
    } catch (err) {
        logResponse({ error: err.message });
    }
}

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        logResponse({ endpoint: "/auth/login", status: res.status, data });
        
        if (res.ok && data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            updateUI();
        }
    } catch (err) {
        logResponse({ error: err.message });
    }
}

async function getUserProfile() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/users/me`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${token}` 
            }
        });
        const data = await res.json();
        logResponse({ endpoint: "/users/me", status: res.status, data });
    } catch (err) {
        logResponse({ error: err.message });
    }
}

function logout() {
    localStorage.removeItem("access_token");
    updateUI();
    logResponse({ message: "Logged out" });
}

// Initial UI state
updateUI();

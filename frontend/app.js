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
        
        let data;
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            data = await res.json();
        } else {
            data = await res.text();
        }

        logResponse({ endpoint: "/auth/register", status: res.status, data });
        
        if (res.ok && data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            updateUI();
        }
    } catch (err) {
        console.error("Fetch error:", err);
        logResponse({ error: err.message, note: "Check if the backend is running at " + API_BASE });
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

        let data;
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            data = await res.json();
        } else {
            data = await res.text();
        }

        logResponse({ endpoint: "/auth/login", status: res.status, data });
        
        if (res.ok && data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            updateUI();
        }
    } catch (err) {
        console.error("Fetch error:", err);
        logResponse({ error: err.message, note: "Check if the backend is running at " + API_BASE });
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

async function listUsers() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/users/`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/users/", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

// Sustainability
async function getSustainabilityScore() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/sustainability/score`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/sustainability/score", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function getSustainabilityHistory() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/sustainability/history`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/sustainability/history", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function logPrompt() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/sustainability/log`, {
            method: "POST",
            headers: { 
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                original_prompt: "Can you help me reduce my carbon footprint?",
                optimized_prompt: "Reduced carbon footprint advice.",
                token_count: 50,
                impact_reduction: 0.2
            })
        });
        const data = await res.json();
        logResponse({ endpoint: "/sustainability/log", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

// Forest
async function getForest() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/forest/`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/forest/", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function listTrees() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/forest/trees`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/forest/trees", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function plantTree() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/forest/plant`, {
            method: "POST",
            headers: { 
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ tree_type: "Oak", position_x: 0, position_y: 0 })
        });
        const data = await res.json();
        logResponse({ endpoint: "/forest/plant", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

// Gamification
async function getXP() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/gamification/xp`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/gamification/xp", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function getAchievements() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/gamification/achievements`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/gamification/achievements", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function getLeaderboard() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/gamification/leaderboard`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/gamification/leaderboard", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

// Prompt Coach
async function analyzePrompt() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/prompt-coach/analyze`, {
            method: "POST",
            headers: { 
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt: "Write a short poem about sustainability." })
        });
        const data = await res.json();
        logResponse({ endpoint: "/prompt-coach/analyze", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function getPromptHistory() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/prompt-coach/history`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/prompt-coach/history", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

// Wellness
async function getWellnessGoals() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/wellness/goals`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/wellness/goals", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

async function getWellnessLimits() {
    const token = localStorage.getItem("access_token");
    try {
        const res = await fetch(`${API_BASE}/wellness/limits`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        logResponse({ endpoint: "/wellness/limits", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

// System
async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health/readiness`, { method: "GET" });
        const data = await res.json();
        logResponse({ endpoint: "/health/readiness", status: res.status, data });
    } catch (err) { logResponse({ error: err.message }); }
}

function logout() {
    localStorage.removeItem("access_token");
    updateUI();
    logResponse({ message: "Logged out" });
}

// Initial UI state
updateUI();

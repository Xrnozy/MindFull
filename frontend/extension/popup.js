const API_BASE = "http://localhost:8000/api/v1";

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const authView = document.getElementById('auth-view');
    const mainView = document.getElementById('main-view');
    const loginBtn = document.getElementById('login-btn');
    const testApiBtn = document.getElementById('test-api-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const statusDiv = document.getElementById('status');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    function showStatus(msg) {
        statusDiv.innerText = typeof msg === 'object' ? JSON.stringify(msg, null, 2) : msg;
    }

    function updateUI(token) {
        if (token) {
            authView.classList.add('hidden');
            mainView.classList.remove('hidden');
        } else {
            authView.classList.remove('hidden');
            mainView.classList.add('hidden');
        }
    }

    // Check token on load
    chrome.storage.local.get(['access_token'], function(result) {
        updateUI(result.access_token);
    });

    loginBtn.addEventListener('click', async () => {
        const email = emailInput.value;
        const password = passwordInput.value;
        showStatus("Logging in...");
        
        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            
            if (res.ok && data.access_token) {
                chrome.storage.local.set({ access_token: data.access_token }, () => {
                    updateUI(data.access_token);
                    showStatus("Login successful");
                });
            } else {
                showStatus(`Error: ${data.detail || 'Login failed'}`);
            }
        } catch (err) {
            showStatus(`Error: ${err.message}`);
        }
    });

    logoutBtn.addEventListener('click', () => {
        chrome.storage.local.remove(['access_token'], () => {
            updateUI(null);
            showStatus("Logged out");
        });
    });

    testApiBtn.addEventListener('click', async () => {
        chrome.storage.local.get(['access_token'], async function(result) {
            const token = result.access_token;
            if (!token) return;
            
            showStatus("Fetching profile...");
            try {
                const res = await fetch(`${API_BASE}/users/me`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}` }
                });
                const data = await res.json();
                showStatus(data);
            } catch (err) {
                showStatus(`Error: ${err.message}`);
            }
        });
    });
});

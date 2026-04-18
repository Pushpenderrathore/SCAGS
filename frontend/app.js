const API = "http://127.0.0.1:5000";

// ── Token helpers ──────────────────────────────────────────────────────────────
function getToken() { return localStorage.getItem("scags_token"); }
function getUser()  { return localStorage.getItem("scags_user"); }

function setSession(token, username) {
    localStorage.setItem("scags_token", token);
    localStorage.setItem("scags_user", username);
}

function clearSession() {
    localStorage.removeItem("scags_token");
    localStorage.removeItem("scags_user");
}

// ── Boot ──────────────────────────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
    if (getToken()) {
        showApp();
    }
});

function showApp() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("app-section").classList.remove("hidden");
    document.getElementById("btn-logout").classList.remove("hidden");
    document.getElementById("nav-user").textContent = `👤 ${getUser()}`;
}

function showAuth() {
    document.getElementById("app-section").classList.add("hidden");
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("btn-logout").classList.add("hidden");
    document.getElementById("nav-user").textContent = "";
}

function logout() {
    clearSession();
    showAuth();
}

// ── Tab switch ─────────────────────────────────────────────────────────────────
function switchTab(tab) {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    event.target.classList.add("active");

    document.getElementById("login-form").classList.toggle("hidden", tab !== "login");
    document.getElementById("register-form").classList.toggle("hidden", tab !== "register");
}

// ── Register ──────────────────────────────────────────────────────────────────
async function register() {
    const username = document.getElementById("reg-username").value.trim();
    const email    = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;
    const errEl    = document.getElementById("reg-error");
    const okEl     = document.getElementById("reg-success");

    errEl.textContent = "";
    okEl.textContent  = "";

    if (!username || !email || !password) {
        errEl.textContent = "All fields are required.";
        return;
    }

    try {
        const res = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });
        const data = await res.json();

        if (!res.ok) {
            errEl.textContent = data.error || "Registration failed.";
        } else {
            okEl.textContent = "Account created! You can now login.";
            document.getElementById("reg-username").value = "";
            document.getElementById("reg-email").value    = "";
            document.getElementById("reg-password").value = "";
        }
    } catch (e) {
        errEl.textContent = "Cannot reach server. Is Flask running?";
    }
}

// ── Login ─────────────────────────────────────────────────────────────────────
async function login() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;
    const errEl    = document.getElementById("login-error");

    errEl.textContent = "";

    if (!username || !password) {
        errEl.textContent = "Enter username and password.";
        return;
    }

    try {
        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();

        if (!res.ok) {
            errEl.textContent = data.error || "Login failed.";
        } else {
            setSession(data.token, data.username);
            showApp();
        }
    } catch (e) {
        errEl.textContent = "Cannot reach server. Is Flask running?";
    }
}

// ── Recommend ─────────────────────────────────────────────────────────────────
async function getRecommendations() {
    const percentile = parseFloat(document.getElementById("percentile").value);
    const branch     = document.getElementById("branch").value;
    const maxFees    = document.getElementById("max-fees").value;
    const location   = document.getElementById("location").value.trim();

    const errEl = document.getElementById("api-error");
    errEl.classList.add("hidden");

    if (isNaN(percentile) || percentile < 0 || percentile > 100) {
        errEl.textContent = "Enter a valid percentile between 0 and 100.";
        errEl.classList.remove("hidden");
        return;
    }

    // Show loading
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("results-section").classList.add("hidden");
    document.getElementById("empty-state").classList.add("hidden");

    const body = { percentile, branch };
    if (maxFees)  body.max_fees = parseInt(maxFees);
    if (location) body.location = location;

    try {
        const res = await fetch(`${API}/recommend`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(body)
        });

        if (res.status === 401) {
            clearSession();
            showAuth();
            return;
        }

        const data = await res.json();
        document.getElementById("loading").classList.add("hidden");

        if (!res.ok) {
            errEl.textContent = data.error || "Something went wrong.";
            errEl.classList.remove("hidden");
            return;
        }

        renderResults(data);

    } catch (e) {
        document.getElementById("loading").classList.add("hidden");
        errEl.textContent = "Cannot reach server. Is Flask running?";
        errEl.classList.remove("hidden");
    }
}

// ── Render Results ────────────────────────────────────────────────────────────
function renderResults(data) {
    if (!data.results || data.results.length === 0) {
        document.getElementById("empty-state").classList.remove("hidden");
        return;
    }

    document.getElementById("results-count").textContent =
        `${data.count} college${data.count !== 1 ? "s" : ""} found`;

    document.getElementById("results-query").textContent =
        `Percentile: ${data.percentile} | Branch: ${data.branch}`;

    const grid = document.getElementById("results-grid");
    grid.innerHTML = "";

    data.results.forEach((college, i) => {
        const rank = i + 1;
        const scorePercent = Math.min(college.score, 100).toFixed(0);

        const card = document.createElement("div");
        card.className = "college-card";
        card.innerHTML = `
            <div class="card-rank ${rank <= 3 ? 'top3' : ''}">
                ${rank <= 3 ? '🏆' : '#'}${rank}
            </div>
            <div class="card-name">${college.name}</div>
            <div class="card-branch">${college.branch}</div>
            <div class="card-stats">
                <div class="stat">
                    <div class="stat-label">Cutoff</div>
                    <div class="stat-value">${college.cutoff}%ile</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Placement</div>
                    <div class="stat-value">${college.placement}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Annual Fees</div>
                    <div class="stat-value">₹${college.fees.toLocaleString('en-IN')}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">NIRF Rank</div>
                    <div class="stat-value">#${college.ranking || 'N/A'}</div>
                </div>
            </div>
            <div class="card-location">📍 ${college.location}</div>
            <div class="score-bar-wrap">
                <div class="score-bar-label">
                    <span>SCAGS Score</span>
                    <span>${scorePercent}/100</span>
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width: ${scorePercent}%"></div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    document.getElementById("results-section").classList.remove("hidden");
}

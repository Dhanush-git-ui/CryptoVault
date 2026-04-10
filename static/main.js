/* ===============================
   CryptoVault — Main JS
   =============================== */

async function secureLogin() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorEl  = document.getElementById("errorMsg");
    const btn      = document.getElementById("loginBtn");

    // Reset state
    errorEl.textContent = "";

    // Validation
    if (!username || !password) {
        showError("Please enter both username and password.");
        return;
    }

    // Loading state
    btn.textContent = "Authenticating…";
    btn.disabled    = true;

    try {
        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(`${username}:${password}`)
        });

        const result = await res.json();

        if (result.session_token) {
            // Store and redirect
            localStorage.setItem("session_token", result.session_token);
            btn.textContent = "✓ Success";
            btn.style.background = "linear-gradient(135deg, #059669, #10b981)";

            setTimeout(() => {
                window.location.href = "/success";
            }, 700);

        } else {
            showError("Invalid username or password.");
            resetBtn();
        }

    } catch (err) {
        console.error(err);
        showError("Server error. Please try again.");
        resetBtn();
    }

    function showError(msg) {
        errorEl.innerHTML = `
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            ${msg}
        `;
    }

    function resetBtn() {
        btn.textContent = "Sign In";
        btn.disabled    = false;
        btn.style.background = "";
    }
}

/* ── Toggle Password Visibility ── */
function togglePassword() {
    const input = document.getElementById("password");
    const icon  = document.getElementById("eyeIcon");

    if (input.type === "password") {
        input.type = "text";
        icon.innerHTML = `
            <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12a21.8 21.8 0 0 1 4.06-5.94"/>
            <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
            <line x1="1" y1="1" x2="23" y2="23"/>
        `;
    } else {
        input.type = "password";
        icon.innerHTML = `
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
        `;
    }
}

/* ── Allow Enter key to submit ── */
document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const btn = document.getElementById("loginBtn");
            if (btn) secureLogin();
        }
    });
});
/* ===============================
   Research Page Logic
   =============================== */

function switchTab(tabName) {

    // Remove active
    document.querySelectorAll(".research-tab").forEach(t => {
        t.classList.remove("active");
    });

    document.querySelectorAll(".research-content").forEach(c => {
        c.style.display = "none";
    });

    // Activate selected
    document.getElementById(tabName).style.display = "block";
    document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");
}
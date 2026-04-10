/* ===============================
   CryptoVault — Simulation JS
   =============================== */

let attackMode = false;

function toggleAttack(el) {
    attackMode = el.checked;
}

/* Add step with animation */
function addStep(text, type = "normal") {
    const container = document.getElementById("steps");

    const div = document.createElement("div");
    div.className = "sim-step";

    if (type === "success") div.classList.add("sim-success");
    if (type === "error")   div.classList.add("sim-error");

    div.innerHTML = `
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/>
        </svg>
        ${text}
    `;

    container.appendChild(div);
    div.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/* Delay helper */
function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/* MAIN SIMULATION — calls real Flask /simulate API */
async function startSimulation() {

    const steps = document.getElementById("steps");
    steps.innerHTML = "";

    // Disable button while running
    const btn = document.querySelector(".btn-primary");
    btn.disabled = true;
    btn.textContent = "Running…";

    // ── Call the backend ──────────────────────────────
    const msg = document.getElementById("simMessage").value;
    let data;
    try {
        const res = await fetch("/simulate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ attack: attackMode, message: msg })
        });
        data = await res.json();
    } catch (e) {
        addStep("⚠ Could not connect to server. Is Flask running?", "error");
        btn.disabled = false;
        btn.textContent = "Start Simulation";
        return;
    }

    const mdh = data.mdh;
    const rsa = data.rsa;

    // ── MDH Phase ────────────────────────────────────

    addStep(`User A generates prime <strong>P = <span class="sim-highlight">${mdh.P}</span></strong>`);
    await wait(600);

    addStep(`User A sends obfuscated <strong>Pn = <span class="sim-highlight">${mdh.Pn}</span></strong> (P × 2)`);
    await wait(600);

    addStep(`User B generates prime <strong>Q = <span class="sim-highlight">${mdh.Q}</span></strong>`);
    await wait(600);

    addStep(`User B sends combined <strong>Qn = <span class="sim-highlight">${mdh.Qn}</span></strong> (P + Q)`);
    await wait(600);

    addStep(`User A recovers Q = Qn − P = <span class="sim-highlight">${mdh.Qn} − ${mdh.P} = ${mdh.Q}</span>`);
    await wait(600);

    addStep(`Public Key A = P<sup>Pa</sup> mod Q = <span class="sim-highlight">${mdh.PubA}</span>`);
    await wait(600);

    addStep(`Public Key B = P<sup>Pb</sup> mod Q = <span class="sim-highlight">${mdh.PubB}</span>`);
    await wait(600);

    addStep(`Secret Key A = PubB<sup>Pa</sup> mod Q = <span class="sim-highlight">${mdh.SecA}</span>`);
    await wait(600);

    if (attackMode) {
        addStep(`⚠ MITM Attack Active — Secret Key B was tampered! (+1 injected)`, "error");
        await wait(600);
    }

    addStep(`Secret Key B = PubA<sup>Pb</sup> mod Q = <span class="sim-highlight">${mdh.SecB}</span>`);
    await wait(600);

    // ── Validation ───────────────────────────────────

    if (mdh.secure) {
        addStep(`✓ Keys match (${mdh.SecA} == ${mdh.SecB}) — Secure channel established!`, "success");
        await wait(800);

        // ── RSA Phase ────────────────────────────────
        if (rsa) {
            addStep(`RSA: n = P × Q = <span class="sim-highlight">${rsa.n}</span>,  φ(n) = <span class="sim-highlight">${rsa.phi}</span>`);
            await wait(600);

            addStep(`Public exponent e = <span class="sim-highlight">${rsa.e}</span>,  Private exponent d = <span class="sim-highlight">${rsa.d}</span>`);
            await wait(600);

            addStep(`Original message = "<span class="sim-highlight">${rsa.message}</span>"`);
            await wait(600);

            addStep(`Integer Encoding (m) = <span class="sim-highlight">${rsa.encrypted < rsa.n ? "(m < n checked)" : "(truncated)"}</span>`);
            await wait(600);

            addStep(`Ciphertext (c) = m<sup>e</sup> mod n = <span class="sim-highlight">${rsa.encrypted}</span>`);
            await wait(600);

            addStep(`Decrypted Integer = c<sup>d</sup> mod n`, "success");
            await wait(400);

            addStep(`Decoded Message = "<span class="sim-highlight">${rsa.decrypted}</span>"`, "success");
        }

    } else {
        addStep(`✗ Key mismatch! SecA=${mdh.SecA} ≠ SecB=${mdh.SecB} — MITM Attack Detected!`, "error");
    }

    btn.disabled = false;
    btn.textContent = "Start Simulation";
}

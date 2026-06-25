function logToTerminal(message) {
    const logBox = document.getElementById("term-log");
    if (!logBox) return;
    
    const timestamp = new Date().toISOString().slice(11, 19);
    const newEntry = document.createElement("div");
    newEntry.className = "log-entry";
    newEntry.innerText = `[${timestamp}] ${message}`;
    logBox.appendChild(newEntry);
    
    while (logBox.children.length > 4) {
        logBox.removeChild(logBox.firstChild);
    }
}

async function fetchData() {
    try {
        const metricsRes = await fetch('/api/v1/metrics');
        const metrics = await metricsRes.json();

        const healthRes = await fetch('/api/v1/health');
        const health = await healthRes.json();

        updateUI(metrics, health);
        logToTerminal("SUCCESS: Telemetry batch parsing complete.");
    } catch (err) {
        const statusEl = document.getElementById("status");
        if (statusEl) {
            statusEl.innerText = "[SYS_ERR]";
            statusEl.className = "status-text bad";
        }
        logToTerminal("ERROR: Connection interrupt on telemetry fetch sync.");
    }
}

function updateUI(metrics, health) {
    document.getElementById("uptime").innerText = Math.floor(metrics.uptime_seconds) + "s";
    document.getElementById("requests").innerText = metrics.requests_total;
    document.getElementById("overall-status").innerText = `[${health.status.toUpperCase()}]`;
    document.getElementById("database-status").innerText = `[${health.database.toUpperCase()}]`;
    document.getElementById("redis-status").innerText = `[${health.redis.toUpperCase()}]`;

    const statusEl = document.getElementById("status");
    if (statusEl) {
        if (health.status === "healthy" || health.status === "LIVE") {
            statusEl.innerText = "[LIVE]";
            statusEl.className = "status-text live";
        } else {
            statusEl.innerText = "[DEGRADED]";
            statusEl.className = "status-text bad";
        }
    }
}

// System Contrast / Theme Toggle Handler
function toggleTheme() {
    const body = document.body;
    const toggleBtn = document.getElementById("theme-toggle");
    
    if (body.classList.contains("dark-theme")) {
        body.classList.remove("dark-theme");
        toggleBtn.innerText = "MODE: BINARY";
        localStorage.setItem("theme", "light");
        logToTerminal("CONFIG: Ambient paper tone active.");
    } else {
        body.classList.add("dark-theme");
        toggleBtn.innerText = "MODE: LEDGER";
        localStorage.setItem("theme", "dark");
        logToTerminal("CONFIG: High contrast binary matrix mode active.");
    }
}

// Core initialization routine
document.addEventListener("DOMContentLoaded", () => {
    // Check local storage configuration history
    const savedTheme = localStorage.getItem("theme");
    const toggleBtn = document.getElementById("theme-toggle");
    
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        if (toggleBtn) toggleBtn.innerText = "MODE: LEDGER";
    }

    if (toggleBtn) {
        toggleBtn.addEventListener("click", toggleTheme);
    }

    fetchData();
    setInterval(fetchData, 5000);
});

let previousRequests = 0;
const trafficHistory = [];

function logToTerminal(message) {
    const logBox = document.getElementById("term-log");
    if (!logBox) return;
    
    const timestamp = new Date().toISOString().slice(11, 19);
    const newEntry = document.createElement("div");
    newEntry.className = "log-entry";
    newEntry.innerText = `[${timestamp}] ${message}`;
    logBox.appendChild(newEntry);
    
    while (logBox.children.length > 4) {
        logBox.removeChild(logBox.firstChild);
    }
}

// Generates structural terminal sparklines based on request differentials
function generateSparkline(currentCount) {
    if (previousRequests === 0) {
        previousRequests = currentCount;
        return "[ ▄ ]";
    }
    const diff = currentCount - previousRequests;
    previousRequests = currentCount;

    // Map delta to an ASCII block scale character
    const blocks = [" ", " ", "▄", "▅", "▆", "▇", "█"];
    const blockIndex = Math.min(Math.floor(diff / 2), blocks.length - 1);
    
    trafficHistory.push(blocks[blockIndex]);
    if (trafficHistory.length > 12) trafficHistory.shift();
    
    return `[ ${trafficHistory.join("")} ]`;
}

async function fetchData() {
    try {
        const startTime = performance.now();
        
        const metricsRes = await fetch('/api/v1/metrics');
        const metrics = await metricsRes.json();

        const healthRes = await fetch('/api/v1/health');
        const health = await healthRes.json();
        
        const rtt = Math.round(performance.now() - startTime);

        updateUI(metrics, health, rtt);
    } catch (err) {
        const statusEl = document.getElementById("status");
        if (statusEl) {
            statusEl.innerText = "[SYS_ERR]";
            statusEl.className = "status-text bad";
        }
        logToTerminal("ERROR: Connection interrupt on telemetry fetch sync.");
    }
}

function updateUI(metrics, health, rtt) {
    document.getElementById("uptime").innerText = Math.floor(metrics.uptime_seconds) + "s";
    
    // Append the sparkline graph directly right next to the request counter value
    const spark = generateSparkline(metrics.requests_total);
    document.getElementById("requests").innerText = `${spark} ${metrics.requests_total}`;
    
    document.getElementById("ping-latency").innerText = `${rtt}ms`;
    document.getElementById("overall-status").innerText = `[${health.status.toUpperCase()}]`;
    document.getElementById("database-status").innerText = `[${health.database.toUpperCase()}]`;
    document.getElementById("redis-status").innerText = `[${health.redis.toUpperCase()}]`;

    const statusEl = document.getElementById("status");
    if (statusEl) {
        if (health.status === "healthy" || health.status === "LIVE") {
            statusEl.innerText = "[LIVE]";
            statusEl.className = "status-text live";
        } else {
            statusEl.innerText = "[DEGRADED]";
            statusEl.className = "status-text bad";
        }
    }
}

// Theme Handling Logic
function toggleTheme() {
    const body = document.body;
    const toggleBtn = document.getElementById("theme-toggle");
    if (body.classList.contains("dark-theme")) {
        body.classList.remove("dark-theme");
        toggleBtn.innerText = "MODE: BINARY";
        localStorage.setItem("theme", "light");
    } else {
        body.classList.add("dark-theme");
        toggleBtn.innerText = "MODE: LEDGER";
        localStorage.setItem("theme", "dark");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    const toggleBtn = document.getElementById("theme-toggle");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        if (toggleBtn) toggleBtn.innerText = "MODE: LEDGER";
    }
    if (toggleBtn) toggleBtn.addEventListener("click", toggleTheme);

    fetchData();
    setInterval(fetchData, 5000);
});
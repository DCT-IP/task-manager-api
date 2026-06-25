let previousRequests = 0;
const trafficHistory = [];

function logToTerminal(message) {
    const logBox = document.getElementById("term-log");
    if (!logBox) return;

    const timestamp = new Date().toISOString().slice(11, 19);

    const entry = document.createElement("div");
    entry.className = "log-entry";
    entry.innerText = `[${timestamp}] ${message}`;

    logBox.appendChild(entry);

    while (logBox.children.length > 4) {
        logBox.removeChild(logBox.firstChild);
    }
}

function generateSparkline(currentCount) {

    if (previousRequests === 0) {
        previousRequests = currentCount;
        return "[ ▄ ]";
    }

    const diff = currentCount - previousRequests;
    previousRequests = currentCount;

    const blocks = [
        " ",
        " ",
        "▄",
        "▅",
        "▆",
        "▇",
        "█"
    ];

    const index = Math.min(
        Math.floor(diff / 2),
        blocks.length - 1
    );

    trafficHistory.push(
        blocks[index]
    );

    if (trafficHistory.length > 12) {
        trafficHistory.shift();
    }

    return `[ ${trafficHistory.join("")} ]`;
}

async function fetchData() {

    try {

        const startTime = performance.now();

        const metricsRes = await fetch(
            "/api/v1/metrics"
        );

        const metrics = await metricsRes.json();

        const healthRes = await fetch(
            "/api/v1/health"
        );

        const health = await healthRes.json();

        const rtt = Math.round(
            performance.now() - startTime
        );

        updateUI(
            metrics,
            health,
            rtt
        );

        logToTerminal(
            "SUCCESS: Telemetry batch parsing complete."
        );

    } catch (err) {

        const statusEl =
            document.getElementById("status");

        if (statusEl) {
            statusEl.innerText = "[SYS_ERR]";
            statusEl.className =
                "status-text bad";
        }

        logToTerminal(
            "ERROR: Connection interrupt on telemetry fetch sync."
        );
    }
}

function updateUI(
    metrics,
    health,
    rtt
) {

    document.getElementById(
        "uptime"
    ).innerText =
        Math.floor(
            metrics.uptime_seconds
        ) + "s";

    const spark =
        generateSparkline(
            metrics.requests_total
        );

    document.getElementById(
        "requests"
    ).innerText =
        `${spark} ${metrics.requests_total}`;

    document.getElementById(
        "ping-latency"
    ).innerText =
        `${rtt}ms`;

    const overall =
        health.database === "up"
            ? "HEALTHY"
            : "DEGRADED";

    document.getElementById(
        "overall-status"
    ).innerText =
        `[${overall}]`;

    document.getElementById(
        "database-status"
    ).innerText =
        `[${health.database.toUpperCase()}]`;

    const statusEl =
        document.getElementById("status");

    if (!statusEl) return;

    if (health.database === "up") {

        statusEl.innerText =
            "[LIVE]";

        statusEl.className =
            "status-text live";

    } else {

        statusEl.innerText =
            "[DEGRADED]";

        statusEl.className =
            "status-text bad";
    }
}

function toggleTheme() {

    const body = document.body;

    const toggleBtn =
        document.getElementById(
            "theme-toggle"
        );

    if (
        body.classList.contains(
            "dark-theme"
        )
    ) {

        body.classList.remove(
            "dark-theme"
        );

        toggleBtn.innerText =
            "MODE: BINARY";

        localStorage.setItem(
            "theme",
            "light"
        );

        logToTerminal(
            "CONFIG: Ambient paper tone active."
        );

    } else {

        body.classList.add(
            "dark-theme"
        );

        toggleBtn.innerText =
            "MODE: LEDGER";

        localStorage.setItem(
            "theme",
            "dark"
        );

        logToTerminal(
            "CONFIG: High contrast binary matrix mode active."
        );
    }
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const savedTheme =
            localStorage.getItem(
                "theme"
            );

        const toggleBtn =
            document.getElementById(
                "theme-toggle"
            );

        if (
            savedTheme === "dark"
        ) {

            document.body.classList.add(
                "dark-theme"
            );

            if (toggleBtn) {
                toggleBtn.innerText =
                    "MODE: LEDGER";
            }
        }

        if (toggleBtn) {
            toggleBtn.addEventListener(
                "click",
                toggleTheme
            );
        }

        fetchData();

        setInterval(
            fetchData,
            5000
        );
    }
);
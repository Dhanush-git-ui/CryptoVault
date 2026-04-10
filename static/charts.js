/* ===============================
   CryptoVault — Charts JS
   =============================== */

document.addEventListener("DOMContentLoaded", () => {

    const ctx = document.getElementById("performanceChart");

    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["64-bit", "128-bit", "512-bit"],

            datasets: [
                {
                    label: "MDH Time (sec)",
                    data: [27.7, 66.7, 271],
                    borderWidth: 2,
                    tension: 0.4
                },
                {
                    label: "CDH Time (sec)",
                    data: [88.5, 165.5, 603],
                    borderWidth: 2,
                    tension: 0.4
                }
            ]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        color: "#cbd5f5"
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: "#94a3b8"
                    },
                    grid: {
                        color: "rgba(99,102,241,0.1)"
                    }
                },
                y: {
                    ticks: {
                        color: "#94a3b8"
                    },
                    grid: {
                        color: "rgba(99,102,241,0.1)"
                    }
                }
            }
        }
    });

});
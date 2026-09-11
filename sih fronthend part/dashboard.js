const BASE_URL = "http://127.0.0.1:8000";

async function fetchData(endpoint) {
  try {
    const res = await fetch(`${BASE_URL}/${endpoint}`);
    return await res.json();
  } catch {
    alert("Backend connection unavailable. Please start the FastAPI server.");
  }
}

// Initialize bands
function renderBands() {
  const bandsDiv = document.getElementById("bands");
  bandsDiv.innerHTML = "";
  for (let i = 1; i <= 10; i++) {
    const div = document.createElement("div");
    div.className = "band";
    div.textContent = `Band ${i}`;
    bandsDiv.appendChild(div);
  }
}

// Update metrics dynamically
async function updateMetrics() {
  const metrics = await fetchData("metrics");
  document.getElementById("detectRate").textContent = `Detection Rate: ${metrics.detectionRate}%`;
  document.getElementById("falseRate").textContent = `False Alarm Rate: ${metrics.falseAlarmRate}%`;
  document.getElementById("interceptRate").textContent = `Interception Rate: ${metrics.interceptionRate}%`;
  document.getElementById("avgTime").textContent = `Average Intercept Time: ${metrics.avgInterceptTime} sec`;
  document.getElementById("accuracy").textContent = `Prediction Accuracy: ${metrics.predictionAccuracy}%`;
  document.getElementById("totalIntercepts").textContent = `Total Intercepts: ${metrics.totalIntercepts}`;
}

// Charts
const probChart = new Chart(document.getElementById("probChart"), {
  type: 'bar',
  data: {
    labels: Array.from({ length: 10 }, (_, i) => `Band ${i + 1}`),
    datasets: [{ label: 'Predicted Probability', data: [], backgroundColor: '#4a90e2' }]
  },
  options: { scales: { y: { beginAtZero: true } } }
});

const compareChart = new Chart(document.getElementById("compareChart"), {
  type: 'bar',
  data: {
    labels: ['Detection Rate', 'Interception Rate', 'Intercept Time', 'Missed Signals', 'False Alarms'],
    datasets: [
      { label: 'Traditional', data: [65, 60, 5.2, 12, 15], backgroundColor: '#f39c12' },
      { label: 'Smart', data: [89, 87, 2.1, 4, 4], backgroundColor: '#27ae60' }
    ]
  },
  options: { responsive: true }
});

document.getElementById("startBtn").onclick = () => fetchData("simulation/start");
document.getElementById("pauseBtn").onclick = () => fetchData("simulation/stop");
document.getElementById("resetBtn").onclick = () => fetchData("simulation/reset");

renderBands();
updateMetrics();

<script>
  // Dropdown handlers for demonstration
  const metricSelect = document.getElementById('metricSelect');
  const map = document.getElementById('map');
  metricSelect.addEventListener('change', () => {
    const value = metricSelect.value;
    if (value === 'AQI') {
      map.style.background = 'linear-gradient(180deg, #eaf8f0, #e4f1ff)';
    } else if (value === 'Temperature') {
      map.style.background = 'linear-gradient(180deg, #fff3e6, #ffecec)';
    } else {
      map.style.background = 'linear-gradient(180deg, #e6fff2, #efffed)';
    }
  });

  // Refresh + last updated
  const lastUpdate = document.getElementById('lastUpdate');
  const btnRefresh = document.getElementById('btnRefresh');

  function updateTimestamp() {
    const now = Date.now();
    lastUpdate.dataset.timestamp = now; // store reference time
    lastUpdate.textContent = "just now";
    tick(); // immediate update
  }

  function tick() {
    const last = Number(lastUpdate.dataset.timestamp);
    if (!last) return;

    const diffMs = Date.now() - last;
    const diffMin = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

    if (diffMin < 1) {
      lastUpdate.textContent = "just now";
    } else if (diffMin < 60) {
      lastUpdate.textContent = rtf.format(-diffMin, "minute");
    } else if (diffHours < 24) {
      lastUpdate.textContent = rtf.format(-diffHours, "hour");
    } else if (diffDays === 1) {
      lastUpdate.textContent = "yesterday";
    } else {
      lastUpdate.textContent = new Date(last).toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric"
      });
    }
  }

  btnRefresh.addEventListener("click", updateTimestamp);

  // Run tick every 30s
  setInterval(tick, 30000);

  // Export stub
  document.getElementById('btnExport').addEventListener('click', () => {
    const blob = new Blob([document.documentElement.outerHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'vitalsphere-dashboard.html';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  });

  // Filter simulation
  document.getElementById('btnFilter').addEventListener('click', () => {
    alert('Filter panel coming soon. This is a visual prototype.');
  });

  // Initialize timestamp
  updateTimestamp();
</script>
const $ = (id) => document.getElementById(id);
const api = async (path, options = {}) => {
  const response = await fetch(path, {headers: {'Content-Type': 'application/json'}, ...options});
  const data = await response.json();
  if (!data.ok) throw new Error(data.error?.message || 'Request failed');
  return data;
};
const post = (path, body = {}) => api(path, {method: 'POST', body: JSON.stringify(body)});

function showError(message = '') { $('error').textContent = message; $('error').hidden = !message; }
function renderConfig(config) {
  $('config').innerHTML = Object.entries(config).map(([key, value]) => `<div><dt>${key.replaceAll('_', ' ')}</dt><dd>${value}</dd></div>`).join('');
}
function renderMetrics(metrics) {
  const values = [['Samples', metrics.samples_received], ['Chunks', metrics.chunks_received], ['Windows', metrics.windows], ['Inferences', metrics.inferences], ['Throughput', `${(metrics.throughput_samples_per_second || 0).toFixed(2)} /s`], ['Latency', `${average(metrics.latencies_seconds).toFixed(4)} s`], ['Drops', metrics.drops], ['Buffers', bufferText(metrics.buffer)]];
  $('metrics').innerHTML = values.map(([label, value]) => `<div><span>${label}</span><strong>${value ?? 0}</strong></div>`).join('');
}
function average(values) { return values?.length ? values.reduce((a, b) => a + b, 0) / values.length : 0; }
function bufferText(buffer) { return buffer ? `${buffer.raw?.depth || 0}/${buffer.raw?.capacity || 0} raw · ${buffer.processed?.depth || 0}/${buffer.processed?.capacity || 0} processed` : '0'; }
function renderPredictions(items) {
  $('predictions').innerHTML = items.slice().reverse().map(item => `<tr><td>${item.timestamp || '-'}</td><td>${item.label || '-'}</td><td>${Number(item.confidence || 0).toFixed(3)}</td><td>${item.sample_start ?? '-'}</td></tr>`).join('') || '<tr><td colspan="4">No predictions yet</td></tr>';
}
async function refresh() {
  try {
    const [status, metrics, predictions, config] = await Promise.all([api('/api/status'), api('/api/metrics'), api('/api/predictions?limit=20'), api('/api/config')]);
    const current = status.status || {};
    $('state').textContent = current.status || 'unknown'; $('state').className = `badge ${current.status || ''}`;
    renderConfig(config.config || {}); renderMetrics(metrics.metrics || {}); renderPredictions(predictions.predictions || []); showError(current.error || '');
  } catch (error) { showError(error.message); }
}
$('configure').onclick = async () => { try { await post('/api/configure', {}); await refresh(); } catch (error) { showError(error.message); } };
$('start').onclick = async () => { try { await post('/api/start'); await refresh(); } catch (error) { showError(error.message); } };
$('stop').onclick = async () => { try { await post('/api/stop'); await refresh(); } catch (error) { showError(error.message); } };
$('fixture').onclick = async () => { try { await post('/api/fixture'); await refresh(); } catch (error) { showError(error.message); } };
refresh(); setInterval(refresh, 1000);

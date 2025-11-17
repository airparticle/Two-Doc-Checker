const invoiceInput = document.getElementById('invoice'); 
const governingInput = document.getElementById('governing'); 
const forceInput = document.getElementById('force'); 
const compareBtn = document.getElementById('compare'); 
const statusEl = document.getElementById('status'); 
const resultsEl = document.getElementById('results'); 
const exportsEl = document.getElementById('exports'); 
const exportJsonBtn = document.getElementById('export-json'); 
const exportCsvBtn = document.getElementById('export-csv'); 
function enableIfReady() { 
compareBtn.disabled = !(invoiceInput.files[0] && governingInput.files[0]); 
} 
invoiceInput.addEventListener('change', enableIfReady); 
governingInput.addEventListener('change', enableIfReady); 
compareBtn.addEventListener('click', async () => { 
resultsEl.innerHTML = ''; 
exportsEl.style.display = 'none'; 
statusEl.textContent = 'Comparing…'; 
const fd = new FormData(); 
fd.append('invoice', invoiceInput.files[0]); 
fd.append('governing', governingInput.files[0]); 
fd.append('force', forceInput.checked ? 'true' : 'false'); 
try { 
const res = await fetch('http://localhost:8000/compare', { method: 'POST', body: fd }); 
const data = await res.json(); 
if (!res.ok || data.error) { 
statusEl.textContent = data.error || 'Comparison failed.'; 
return; 
} 
statusEl.textContent = `Relatedness: ${data.relatedness.label} (${(data.relatedness.score||0).toFixed(2)}) — ${data.relatedness.explain?.join('; ') || ''}`; 
// Findings table 
const findings = data.findings || []; 
if (findings.length === 0) { 
resultsEl.innerHTML = '<p><strong>No discrepancies found.</strong></p>'; 
} else { 
const rows = findings.map(f => ` 
<tr> 
<td>${f.code}</td> 
<td>${f.severity}</td> 
<td>${f.expected||''}</td> 
<td>${f.actual||''}</td> 
<td>${f.a_location||''}</td> 
<td>${f.b_location||''}</td> 
</tr>`).join(''); 
resultsEl.innerHTML = ` 
<table> 
<thead><tr><th>Code</th><th>Severity</th><th>Expected</th><th>Actual</th><th>Invoice Loc</th><th>Gov Loc</th></tr></thead> 
<tbody>${rows}</tbody> 
</table>`; 
} 
// Exports 
exportsEl.style.display = 'block'; 
exportJsonBtn.onclick = () => download('result.json', JSON.stringify(data, null, 2)); 
exportCsvBtn.onclick = () => download('findings.csv', toCsv(findings)); 
} catch (e) { 
statusEl.textContent = 'Error contacting server.'; 
} 
}); 
function download(name, text) { 
const a = document.createElement('a'); 
a.href = URL.createObjectURL(new Blob([text], {type: 'text/plain'})); 
a.download = name; a.click(); 
URL.revokeObjectURL(a.href); 
} 
function toCsv(findings) { 
const headers = ['code','type','severity','confidence','expected','actual','a_excerpt','b_excerpt','a_location','b_location','suggested_resolution']; 
const lines = [headers.join(',')]; 
for (const f of findings) { 
const row = headers.map(k => `"${String(f[k] ?? '').replace(/"/g,'""')}"`).join(','); 
lines.push(row); 
} 
return lines.join('\n'); 
} 
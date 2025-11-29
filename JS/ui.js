// ui.js - Funciones de UI: render de tabla, export CSV, animaciones
function renderTicketsTable() {
const rows = Storage.load();
const tbody = document.querySelector('#tableTickets tbody');
tbody.innerHTML = '';
rows.forEach((t, i) => {
const tr = document.createElement('tr');
tr.innerHTML = `
<td>${i+1}</td>
<td>${escapeHtml(t.cliente||'—')}</td>
<td>${escapeHtml(t.tipoCliente||'—')}</td>
<td>${escapeHtml(t.tipoMante||'—')}</td>
<td>${t.phishing? 'Sí':'No'}</td>
<td>${t.churn}%</td>
<td>${escapeHtml(t.texto.slice(0,120))}</td>
`;
tbody.appendChild(tr);
});
}

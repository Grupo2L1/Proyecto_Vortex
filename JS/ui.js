// ui.js - funciones de UI: render tabla, render resultado, charts
(function () {
  // util
  function escapeHtml(str) {
    if (!str && str !== 0) return '';
    return String(str).replace(/[&<>"']/g, s => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[s]);
  }

  // Render resultado en tarjeta
  function renderResultado(obj = {}) {
    const elPhish = document.getElementById('r-phishing');
    const elTipo = document.getElementById('r-tipo');
    const elAnon = document.getElementById('r-anon');
    const elSent = document.getElementById('r-sentimiento');

    if (elPhish) elPhish.textContent = obj.phishing ? '⚠ Phishing detectado' : 'No — Seguro';
    if (elTipo) elTipo.textContent = obj.tipoMante || (obj.mantenimiento || '—');
    if (elAnon) elAnon.textContent = obj.anonimizado || obj.texto || '—';
    if (elSent) elSent.textContent = (typeof obj.sentimiento === 'number') ? obj.sentimiento.toFixed(2) : (obj.sentimiento || '—');
  }

  // Render tabla con tickets guardados (ok con TicketStore.load())
  function renderTabla() {
    const tbody = document.querySelector('#tablaTickets');
    if (!tbody) return;
    const rows = (window.TicketStore && TicketStore.load()) || [];
    tbody.innerHTML = '';

    rows.forEach((r, i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${escapeHtml(r.cliente || '—')}</td>
        <td>${escapeHtml(r.tipoCliente || '—')}</td>
        <td>${escapeHtml(r.tipoMante || r.mantenimiento || '—')}</td>
        <td>${r.phishing ? 'Sí' : 'No'}</td>
        <td>${r.churn ?? '—'}</td>
        <td>${escapeHtml((r.texto || '').slice(0, 120))}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  // Charts: Sentimiento (line) y Phishing (doughnut)
  let chartSentiment = null;
  let chartPhishing = null;

  function initCharts() {
    // Sentiment chart
    const ctxS = document.getElementById('chartSentimiento');
    if (ctxS && typeof Chart !== 'undefined') {
      chartSentiment = new Chart(ctxS.getContext('2d'), {
        type: 'line',
        data: { labels: [], datasets: [{ label: 'Sentimiento', data: [], tension: 0.3, fill: true }]},
        options: { responsive: true, maintainAspectRatio: false }
      });
    }

    // Phishing chart
    const ctxP = document.getElementById('chartPhishing');
    if (ctxP && typeof Chart !== 'undefined') {
      chartPhishing = new Chart(ctxP.getContext('2d'), {
        type: 'doughnut',
        data: { labels: ['Phishing','Seguro'], datasets: [{ data: [0,0] }]},
        options: { cutout: '60%', responsive: true, maintainAspectRatio: false }
      });
    }
  }

  function updateChartsFromStore() {
    const rows = (window.TicketStore && TicketStore.load()) || [];
    if (!rows.length) {
      if (chartSentiment) { chartSentiment.data.labels = []; chartSentiment.data.datasets[0].data = []; chartSentiment.update(); }
      if (chartPhishing) { chartPhishing.data.datasets[0].data = [0,0]; chartPhishing.update(); }
      return;
    }

    // build sentiment array and phishing counts
    const labels = rows.map((_, i) => `T${i+1}`);
    const sentimentData = rows.map(r => (typeof r.sentimiento === 'number' ? r.sentimiento : 0));
    const phishingCount = rows.filter(r => r.phishing).length;
    const safeCount = rows.length - phishingCount;

    if (chartSentiment) {
      chartSentiment.data.labels = labels;
      chartSentiment.data.datasets[0].data = sentimentData;
      chartSentiment.update();
    }

    if (chartPhishing) {
      chartPhishing.data.datasets[0].data = [phishingCount, safeCount];
      chartPhishing.update();
    }
  }

  // Mostrar alerta (pequeña)
  function mostrarAlerta(msg, tipo = 'info') {
    // crea una alerta temporal si no hay un contenedor
    const id = 'tmp-alert-vortex';
    let cont = document.getElementById(id);
    if (!cont) {
      cont = document.createElement('div');
      cont.id = id;
      cont.style.position = 'fixed';
      cont.style.right = '20px';
      cont.style.top = '20px';
      cont.style.zIndex = 9999;
      document.body.appendChild(cont);
    }
    cont.textContent = msg;
    cont.style.padding = '10px 14px';
    cont.style.borderRadius = '8px';
    cont.style.color = '#042';
    cont.style.background = tipo === 'error' ? '#ffc7c7' : '#c7fff0';
    setTimeout(() => { if (cont) cont.textContent = ''; }, 2500);
  }

  // Exponer API UI
  window.VortexUI = {
    renderResultado,
    renderTabla,
    initCharts,
    updateChartsFromStore,
    mostrarAlerta
  };

  // Auto-init charts y tabla si DOM ya cargado
  document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    renderTabla();
    updateChartsFromStore();
  });
})();

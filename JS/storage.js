// storage.js - Encapsula persistencia en localStorage (sin colisiones)
(function () {
  const KEY = 'vortex_tickets_v1';

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || '[]');
    } catch (e) {
      console.error('Storage.load error:', e);
      return [];
    }
  }

  function save(list) {
    try {
      localStorage.setItem(KEY, JSON.stringify(list));
    } catch (e) {
      console.error('Storage.save error:', e);
    }
  }

  function add(ticket) {
    const list = load();
    list.push(ticket);
    save(list);
    return ticket;
  }

  function clear() {
    localStorage.removeItem(KEY);
  }

  function exportCSV(filename = 'tickets_export.csv') {
    const rows = load();
    if (!rows.length) {
      alert('No hay tickets para exportar');
      return;
    }
    const header = ['id','cliente','tipoCliente','tipoMante','phishing','churn','texto','fecha'];
    const csv = [
      header.join(','),
      ...rows.map((r, i) => {
        const textoEsc = `"${String(r.texto || '').replace(/"/g, '""')}"`;
        return [i+1, r.cliente || '', r.tipoCliente || '', r.tipoMante || '', r.phishing ? 'Sí' : 'No', r.churn || '', textoEsc, r.fecha || ''].join(',');
      })
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  // Exponer API limpia globalmente
  window.TicketStore = {
    load,
    save,
    add,
    clear,
    exportCSV
  };
})();

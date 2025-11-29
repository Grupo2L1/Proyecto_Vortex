// app.js - controlador principal; sin duplicados, usa TicketStore y VortexUI
(function () {

  // Heurísticas locales (puedes reemplazar por llamadas al backend)
  function detectarPhishing(texto) {
    const patrones = [/bit\.ly|t\.co/i, /haga clic aquí|click here/i, /urgente|caducado|expirará|inmediatamente/i, /credenciales|ingresar su pii|renovar/i];
    return patrones.some(p => p.test(texto));
  }

  function anonimizar(texto) {
    let out = texto;
    out = out.replace(/[\w.-]+@[\w.-]+\.\w+/gi, '[EMAIL_OCULTO]');
    out = out.replace(/pass\d+/gi, '[PASSWD_OCULTO]');
    out = out.replace(/\b\d{12,19}\b/g, '[NUM_OCULTO]');
    return out;
  }

  function detectarMantenimiento(texto) {
    const t = texto.toLowerCase();
    if (/\b(error|fallo|bug|crash|caída|no funciona)\b/.test(t)) return 'Correctivo';
    if (/\b(mejora|nueva feature|feature|mejorar|requerimiento|solicito)\b/.test(t)) return 'Evolutivo';
    return 'Otro';
  }

  function analizarSentimientoSimple(texto) {
    const pos = ['excelente','bien','mejoró','gracias','funcionó','perfecto','satisfecho'];
    const neg = ['fallo','error','crítico','urgente','mal','problema','insatisfecho','cancelar','no renovar'];
    let score = 0;
    const t = texto.toLowerCase();
    pos.forEach(w => { if (t.includes(w)) score += 1; });
    neg.forEach(w => { if (t.includes(w)) score -= 1; });
    if (score > 0) score = Math.min(score,3)/3;
    if (score < 0) score = Math.max(score,-3)/3;
    return Math.round(score * 100) / 100;
  }

  function calcularChurn(texto, tipoMante, sentimiento) {
    let score = 0;
    if (tipoMante === 'Correctivo') score += 25;
    if (sentimiento < -0.3) score += 40;
    if (/cambiar de proveedor|no renovar|cancelar/i.test(texto)) score += 50;
    return Math.min(100, score);
  }

  // DOM elements
  const btnProcesar = document.getElementById('procesar');
  const btnLimpiar = document.getElementById('limpiar');
  const btnExport = document.getElementById('exportar');
  const btnClearLS = document.getElementById('limpiarLS');
  const inputTexto = document.getElementById('inputTexto');
  const inputCliente = document.getElementById('cliente'); // si no existe, manejamos abajo

  // Safety: if cliente input doesn't exist, we'll use 'Desconocido'
  function obtenerCliente() {
    const el = document.getElementById('cliente');
    return el ? el.value.trim() || 'Desconocido' : 'Desconocido';
  }

  // Procesar ticket (intenta backend, si falla, guarda local)
  async function procesarTicket() {
    const textoRaw = inputTexto.value.trim();
    if (!textoRaw) {
      window.VortexUI.mostrarAlerta('Escribe el texto del ticket', 'error');
      return;
    }
    const cliente = obtenerCliente();
    // heurísticas locales
    const anonim = anonimizar(textoRaw);
    const esPhish = detectarPhishing(textoRaw);
    const tipoMante = detectarMantenimiento(textoRaw);
    const senti = analizarSentimientoSimple(textoRaw);
    const churn = calcularChurn(textoRaw, tipoMante, senti);

    // objeto de resultado (lo guardamos localmente siempre)
    const ticket = {
      cliente,
      tipoCliente: '—',
      texto: anonim,
      mantenimiento: tipoMante,
      tipoMante,
      phishing: !!esPhish,
      sentimiento: senti,
      churn,
      fecha: new Date().toISOString()
    };

    // Mostrar inmediatamente en UI
    window.VortexUI.renderResultado(ticket);

    // Intentar enviar al backend; si falla, lo guardamos localmente como fallback
    try {
      const res = await fetch('http://127.0.0.1:8000/procesar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: textoRaw, cliente })
      });

      if (res.ok) {
        const data = await res.json();
        // si el backend retorna campos (anonimizado, sentimiento numérico, churn), los usamos
        ticket.anonimizado = data.anonimizado || ticket.texto;
        ticket.sentimiento = (typeof data.sentimiento === 'number') ? data.sentimiento : ticket.sentimiento;
        ticket.churn = data.churn ?? ticket.churn;
        ticket.phishing = data.phishing ?? ticket.phishing;
        ticket.mantenimiento = data.mantenimiento || ticket.mantenimiento;
      } else {
        console.warn('Backend returned not OK, saving local fallback');
      }
    } catch (err) {
      console.warn('No se pudo conectar al backend, guardando localmente', err);
    } finally {
      // Guardar localmente y actualizar UI + charts
      if (window.TicketStore) {
        window.TicketStore.add(ticket);
        window.VortexUI.renderTabla();
        window.VortexUI.updateChartsFromStore();
        window.VortexUI.mostrarAlerta('Ticket procesado y guardado', 'info');
      } else {
        console.error('TicketStore no disponible');
      }
    }
  }

  // Listeners (solo uno por botón)
  if (btnProcesar) btnProcesar.addEventListener('click', procesarTicket);
  if (btnLimpiar) btnLimpiar.addEventListener('click', () => {
    inputTexto.value = '';
    const elCl = document.getElementById('cliente');
    if (elCl) elCl.value = '';
  });
  if (btnExport) btnExport.addEventListener('click', () => {
    if (window.TicketStore) TicketStore.exportCSV();
  });
  if (btnClearLS) btnClearLS.addEventListener('click', () => {
    if (!confirm('¿Borrar todos los tickets en localStorage?')) return;
    if (window.TicketStore) {
      TicketStore.clear();
      window.VortexUI.renderTabla();
      window.VortexUI.updateChartsFromStore();
      window.VortexUI.mostrarAlerta('localStorage limpiado', 'info');
    }
  });

  // Inicializar tabla y charts (por si el DOM ya cargó)
  document.addEventListener('DOMContentLoaded', () => {
    if (window.VortexUI) {
      window.VortexUI.initCharts && window.VortexUI.initCharts();
      window.VortexUI.renderTabla();
      window.VortexUI.updateChartsFromStore();
    }
  });

})();

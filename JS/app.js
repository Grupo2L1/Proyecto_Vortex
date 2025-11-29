// ------------------------------
// 1. Detectar phishing
// ------------------------------
function detectarPhishing(texto) {
    const patrones = [
        /bit\.ly|t\.co/i,
        /haga clic aquí|click here/i,
        /urgente|caducado|expirará|inmediatamente/i,
        /credenciales|ingresar su pii|renovar/i
    ];

    return patrones.some(p => p.test(texto));
}

// ------------------------------
// 2. Anonimizar datos sensibles
// ------------------------------
function anonimizar(texto) {
    let salida = texto;

    // Ocultar emails
    salida = salida.replace(/[\w.-]+@[\w.-]+\.\w+/gi, "[EMAIL_OCULTO]");

    // Ocultar contraseñas tipo Pass123
    salida = salida.replace(/pass\d+/gi, "[PASSWD_OCULTO]");

    return salida;
}

// ------------------------------
// 3. Análisis simple de sentimiento
// ------------------------------
function analizarSentimiento(texto) {
    const palabrasPos = ["excelente", "bien", "mejoró", "gracias", "funcionó", "perfecto"];
    const palabrasNeg = ["fallo", "error", "crítico", "urgente", "mal", "problema"];

    let score = 0;

    palabrasPos.forEach(p => { if (texto.includes(p)) score += 1 });
    palabrasNeg.forEach(p => { if (texto.includes(p)) score -= 1 });

    return score; // similitud con compuesto (-1 a 1)
}

// ------------------------------
// 4. Procesar ticket
// ------------------------------
document.getElementById("btnProcesar").addEventListener("click", () => {
    const texto = document.getElementById("inputTexto").value.trim();

    if (!texto) {
        alert("Ingresa un texto primero.");
        return;
    }

    const esPhishing = detectarPhishing(texto);
    const textoAnon = anonimizar(texto);
    const sentimiento = analizarSentimiento(texto);

    document.getElementById("resultado").classList.remove("hidden");

    document.getElementById("resPhishing").textContent =
        esPhishing ? "⚠ Phishing Detectado" : "No, es seguro";

    document.getElementById("resAnon").textContent = textoAnon;

    document.getElementById("resSentimiento").textContent =
        sentimiento > 0 ? "Positivo"
        : sentimiento < 0 ? "Negativo"
        : "Neutral";
});

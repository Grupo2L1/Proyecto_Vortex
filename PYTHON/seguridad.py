import re  # Biblioteca para expresiones regulares
import pandas as pd  # Librería pandas con alias pd
import os  # Biblioteca para operaciones del sistema operativo


class CiberResilienceProcessor:
    """Clase principal: Detección de Phishing y Anonimización."""

    def __init__(self):
        # Inicialización futura (carga de modelos, diccionarios, etc.)
        pass

    def _detectar_phishing(self, descripcion_caso: str) -> bool:
        """Aplica reglas básicas de detección de phishing."""

        # Patrones comunes
        if re.search(r'bit\.ly/|t\.co/|haga clic aquí|click here', descripcion_caso, re.IGNORECASE):
            return True

        # Señales compuestas
        if (
            re.search(r'urgente|caducado|expirará|inmediatamente', descripcion_caso, re.IGNORECASE)
            and re.search(r'ingresar su pii|renovar|credenciales', descripcion_caso, re.IGNORECASE)
        ):
            return True

        # Caso explícito
        if "bit.ly/malicious" in descripcion_caso.lower():
            return True

        return False

    def _anonimizar_datos(self, descripcion_caso: str) -> str:
        """Oculta datos sensibles: correos, contraseñas simuladas, etc."""
        texto_anonimo = descripcion_caso

        # Emails
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        texto_anonimo = re.sub(email_pattern, '[EMAIL_OCULTO]', texto_anonimo)

        # Contraseñas tipo "Pass123"
        password_pattern = r'pass\d+'  # case insensitive
        texto_anonimo = re.sub(password_pattern, '[PASSWD_OCULTO]', texto_anonimo, flags=re.IGNORECASE)

        return texto_anonimo

    def procesar_ticket(self, ticket: pd.Series) -> tuple:
        """
        Procesa un ticket:
        - Detecta phishing
        - Anonimiza si no es phishing
        Retorna:
        (es_phishing, texto_anonimizado_o_None, estado)
        """

        descripcion = ticket['Descripción_Caso']
        es_phishing = self._detectar_phishing(descripcion)

        if es_phishing:
            print(
                f"\033[31mTICKET {ticket['ID_Ticket']} DETENIDO:\033[0m "
                f"\033[4;37mDetectado Phishing Real. Aislado.\033[0m"
            )
            return True, None, "Phishing Detectado"

        # Anonimización
        descripcion_anonimizada = self._anonimizar_datos(descripcion)

        return False, descripcion_anonimizada, "Procesamiento y Anonimización Completados"


# -----------------------------------
# SIMULACIÓN / TEST (opcional)
# -----------------------------------
"""
ejemplos = [
    {
        'ID_Ticket': 1001,
        'Descripción_Caso': 'El botón de pago tiene un fallo crítico desde ayer. ¡Necesito una solución URGENTE! Mis credenciales son user@client.com y Pass123.',
        'Es_Phishing_Real': 'No'
    },
    {
        'ID_Ticket': 1002,
        'Descripción_Caso': 'Excelente servicio, la última mejora funcionó muy bien. Quisiéramos añadir una nueva feature de reporte en la sección A.',
        'Es_Phishing_Real': 'No'
    },
    {
        'ID_Ticket': 1003,
        'Descripción_Caso': 'Su cuenta ha caducado. Haga clic aquí: bit.ly/malicious para ingresar su Pll y renovar inmediatamente. Si no, su proyecto se eliminará.',
        'Es_Phishing_Real': 'Sí'
    }
]

processor = CiberResilienceProcessor()

print("--- Detección Phishing / Anonimización ---")
print("-" * 30)

for ticket_data in ejemplos:
    ticket = pd.Series(ticket_data)

    is_phishing, texto_limpio, estado = processor.procesar_ticket(ticket)

    if not is_phishing:
        print(f"TICKET {ticket['ID_Ticket']} - {estado}. Continuará el flujo.")
        print(f" Texto original (Fragmento): {ticket['Descripción_Caso'][:50]}...")
        print(f" Texto anonimizado: {texto_limpio}")
    print("-" * 30)
"""

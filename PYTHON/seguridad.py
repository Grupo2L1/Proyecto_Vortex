import re # biblioteca para expresiones regulares. raw string(cadena cruda).
import pandas as pd # librería pandas con alias pd
import os #Biblioteca para operaciones del SO

class CiberResilienceProcessor:
    #Clase principal Phishing y Anonimización.
    def __init__(self):
        # Inicialización, si se necesita cargar modelos o listas de palabras clave
        pass

    def _detectar_phishing(self, descripcion_caso: str) -> bool:
        #Lógica de Detección de Phishing con patrones comunes de ataque.
        
        if re.search(r'bit\.ly/|t\.co/|haga clic aquí|click here', descripcion_caso, re.IGNORECASE):
            return True

        if re.search(r'urgente|caducado|expirará|inmediatamente', descripcion_caso, re.IGNORECASE) and \
           re.search(r'ingresar su pii|renovar|credenciales', descripcion_caso, re.IGNORECASE):
            return True
                
        if "bit.ly/malicious" in descripcion_caso:
            return True
            
        return False
    
    def _anonimizar_datos(self, descripcion_caso: str) -> str:
        #Oculta PII (Informacion de identificación personal correos, contraseñas simuladas, etc.).
        texto_anonimo = descripcion_caso

        email_pattern = r'[\w\.-]+@[\w\.-]+(?:\.\w+)?'
        texto_anonimo = re.sub(email_pattern, '[EMAIL_OCULTO]', texto_anonimo)

        password_pattern = r'(Pass\d+)' # Patrón de ejemplo para Pass123
        texto_anonimo = re.sub(password_pattern, '[PASSWD_OCULTO]', texto_anonimo, flags=re.IGNORECASE)
               
        return texto_anonimo

    def procesar_ticket(self, ticket: pd.Series) -> tuple:
        #Detectar Pishing
        
        descripcion = ticket['Descripción_Caso']
        es_phishing = self._detectar_phishing(descripcion)
        
        if es_phishing:
            print(f"\033[31mTICKET {ticket['ID_Ticket']} DETENIDO:\033[0m \033[4;37mDetectado Phishing Real. Aislado.\033[0m")
            return True, None, "Phishing Detectado" 
        
        # 2. Anonimización/Enmascaramiento (PBD - Privacidad por Diseño)
        descripcion_anonimizada = self._anonimizar_datos(descripcion)
        
        # El texto modificado y limpio es la salida de la Etapa 1
        return False, descripcion_anonimizada, "Procesamiento y Anonimización Completados"
"""# Creación de una simulación de los tickets de entrada (como si fueran filas de un DataFrame)
ejemplos = [
    {'ID_Ticket': 1001, 'Descripción_Caso': 'El botón de pago tiene un fallo crítico desde ayer. ¡Necesito una solución URGENTE! Mis credenciales son user@client.com y Pass123.', 'Es_Phishing_Real': 'No'},
    {'ID_Ticket': 1002, 'Descripción_Caso': 'Excelente servicio, la última mejora funcionó muy bien. Quisiéramos añadir una nueva feature de reporte en la sección A.', 'Es_Phishing_Real': 'No'},
    {'ID_Ticket': 1003, 'Descripción_Caso': 'Su cuenta ha caducado. Haga clic aquí: bit.ly/malicious para ingresar su Pll y renovar inmediatamente. Si no, su proyecto se eliminará.', 'Es_Phishing_Real': 'Sí'}
]

processor = CiberResilienceProcessor()
#os.system('cls' if os.name == 'nt' else 'clear')
print("--- Detección Phishing / Anonimización ---")
print("-" * 30)
for ticket_data in ejemplos:
    ticket = pd.Series(ticket_data)
    
    is_phishing, texto_limpio, estado = processor.procesar_ticket(ticket)
    
    if not is_phishing:
        print(f"TICKET {ticket['ID_Ticket']} - {estado}. Continuará el flujo.")
        print(f" Texto original (Fragmento): {ticket['Descripción_Caso'][:50]}...")
        print(f" Texto anonimizado: {texto_limpio}")    
    print("-" * 30)"""
    
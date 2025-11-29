import pandas as pd
import re
import uuid
import os 
import numpy as np 
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List

# ---------------------------------------------------------------------
# --- VARIABLES GLOBALES Y CONFIGURACIÓN ---
# ---------------------------------------------------------------------

NOMBRE_CSV_OUTPUT = 'dataset_vortex.csv'      # Archivo de salida del procesamiento IA
NOMBRE_CSV_HISTORIAL = 'data_tickets.csv'    # Archivo de datos históricos
ID_BASE = 1000

COLUMNAS_CSV_OUTPUT = [
    'ID_Ticket', 'Descripción_Caso', 'Antigüedad_Contrato', 'Volumen_Tickets_Ult_Mes', 
    'Segmento_Cliente', 
    'Es_Phishing_Real', 'Anonimizado_Requerido', 
    'Sentimiento', 'Tipo_Mantenimiento', 'Riesgo_Churn_Real', 
    'Insight_Clave', 'Recomendacion_Accionable'
]

# ---------------------------------------------------------------------
# PARTE A: GENERACIÓN DE DATOS HISTÓRICOS (data_tickets.csv)
# ---------------------------------------------------------------------

def generate_historical_data(num_records=1000):
    """Genera el archivo de historial 'data_tickets.csv' con 1000 líneas."""
    
    # Generar IDs secuenciales desde ID_BASE
    ids = [ID_BASE + i for i in range(num_records)]
    
    # Generar fechas en los últimos 6 meses
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    
    dates = []
    for _ in range(num_records):
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        dates.append(random_date.strftime('%Y/%m/%d'))
        
    # Generar otros datos aleatorios
    tipo_mantenimiento = random.choices(['Correctivo', 'Evolutivo'], weights=[0.75, 0.25], k=num_records)
    antiguedad_choices = [3, 6, 12, 24, 36] 
    antiguedad_meses = random.choices(antiguedad_choices, weights=[0.2, 0.2, 0.3, 0.2, 0.1], k=num_records)
    
    # Riesgo Churn: Inversamente proporcional a la antigüedad (más joven, más riesgo)
    riesgo_churn = []
    for age in antiguedad_meses:
        # Base de riesgo: 90% para 3 meses, 20% para 36 meses
        risk = int(np.clip(100 - (age / max(antiguedad_choices)) * 80 + random.randint(-10, 10), 10, 95))
        riesgo_churn.append(risk)
        
    es_pishing = random.choices(['No', 'Sí'], weights=[0.99, 0.01], k=num_records)
    
    data = pd.DataFrame({
        'Fecha': dates,
        'ID ticket': ids,
        'Tipo_Mantenimiento': tipo_mantenimiento,
        'antiguedad_contrato': [f'{age} meses' for age in antiguedad_meses],
        'riesgo_churm': riesgo_churn,
        'es_pishing': es_pishing
    })
    
    # Ordenar y guardar
    data['Fecha'] = pd.to_datetime(data['Fecha'], format='%Y/%m/%d')
    data = data.sort_values(by='Fecha').reset_index(drop=True)
    data['Fecha'] = data['Fecha'].dt.strftime('%Y/%m/%d') 
    
    data.to_csv(NOMBRE_CSV_HISTORIAL, index=False)
    print(f"✅ Archivo de historial '{NOMBRE_CSV_HISTORIAL}' generado con {num_records} registros.")

# ---------------------------------------------------------------------
# FASE 1: SETUP (Funciones de Gestión de Archivos y Metadatos)
# ---------------------------------------------------------------------

def setup_csv_output():
    """Crea el archivo CSV de salida si no existe."""
    if not os.path.exists(NOMBRE_CSV_OUTPUT):
        df = pd.DataFrame(columns=COLUMNAS_CSV_OUTPUT)
        df.to_csv(NOMBRE_CSV_OUTPUT, index=False)
        print(f"✅ Archivo de salida '{NOMBRE_CSV_OUTPUT}' listo.")

def obtener_siguiente_id():
    """Calcula el siguiente ID ticket de 4 dígitos secuenciales."""
    max_id = ID_BASE - 1
    
    try:
        if os.path.exists(NOMBRE_CSV_HISTORIAL):
            df_hist = pd.read_csv(NOMBRE_CSV_HISTORIAL)
            if not df_hist.empty:
                max_id = max(max_id, df_hist['ID ticket'].max())
        
        if os.path.exists(NOMBRE_CSV_OUTPUT):
            df_out = pd.read_csv(NOMBRE_CSV_OUTPUT)
            if not df_out.empty:
                # El ID del output es una cadena, necesitamos convertirlo
                max_id_out = df_out['ID_Ticket'].apply(lambda x: int(x) if str(x).isdigit() else ID_BASE).max()
                max_id = max(max_id, max_id_out)
            
        return int(max_id) + 1
    except Exception:
        # En caso de error de lectura, garantiza que se use al menos el ID_BASE
        return ID_BASE

def generar_id():
    """Formatea el ID a 4 dígitos."""
    next_id = obtener_siguiente_id()
    return f"{next_id:04d}"

def obtener_metadatos_cliente():
    """
    Simula la obtención de Antigüedad del Contrato y calcula el Volumen de Tickets
    del último mes basándose en el historial.
    """
    
    # AJUSTE: Antigüedad del Contrato (Simulación de búsqueda de cliente)
    # Asignamos una antigüedad al azar de los valores comunes para el cálculo de riesgo.
    antiguedad_meses = random.choice([3, 12, 24]) 
    
    # AJUSTE: Cálculo de Volumen de Tickets (en el mes actual)
    if not os.path.exists(NOMBRE_CSV_HISTORIAL):
        return antiguedad_meses, 0, []
    
    try:
        df_hist = pd.read_csv(NOMBRE_CSV_HISTORIAL)
        df_hist['Fecha'] = pd.to_datetime(df_hist['Fecha'], format='%Y/%m/%d')
        
        fecha_referencia = datetime.now() 
        
        # Filtrar tickets del mes actual
        df_mes_actual = df_hist[
            (df_hist['Fecha'].dt.year == fecha_referencia.year) & 
            (df_hist['Fecha'].dt.month == fecha_referencia.month)
        ]
        
        volumen_tickets = len(df_mes_actual)
        tickets_mes = df_mes_actual['ID ticket'].tolist()
        
        return antiguedad_meses, volumen_tickets, tickets_mes
    except Exception:
        return antiguedad_meses, 0, []

def guardar_registro(registro: Dict[str, Any]):
    """Añade un registro al archivo CSV de salida."""
    df_nuevo_registro = pd.DataFrame([registro], columns=COLUMNAS_CSV_OUTPUT)
    
    if os.path.exists(NOMBRE_CSV_OUTPUT):
        df_nuevo_registro.to_csv(NOMBRE_CSV_OUTPUT, mode='a', header=False, index=False)
        print(f"Registro del Ticket {registro['ID_Ticket']} guardado en '{NOMBRE_CSV_OUTPUT}'.")
    else:
        print("Error: El archivo CSV de salida no se encuentra.")


# ---------------------------------------------------------------------
# FASE 2: MÓDULO DE SEGURIDAD Y PRE-PROCESAMIENTO
# ---------------------------------------------------------------------

# Patrones Phishing (2.1)
PATRONES_MALICIOSOS = [
    r'(?i)haga clic aqu[íi]|clic en este enlace', 
    r'bit\.ly/[\w\d]+|tinyurl\.com/[\w\d]+', 
    r'(?i)ingrese su pii|contraseña|credenciales', 
    r'(?i)su cuenta ha caducado|su proyecto se eliminar[áa]|actualice su informaci[óo]n'
]
PALABRAS_URGENCIA = ['URGENTE', 'INMEDIATAMENTE', 'CRÍTICO', 'AHORA', 'bloqueado', 'suspenderá']

def detectar_phishing(texto: str) -> bool:
    texto_lower = texto.lower()
    for patron in PATRONES_MALICIOSOS:
        if re.search(patron, texto_lower): return True
    contador_urgencia = sum(1 for palabra in PALABRAS_URGENCIA if palabra.lower() in texto_lower)
    return contador_urgencia >= 2

PATRONES_ANONIMIZACION = {
    r'[\w\.-]+@[\w\.-]+': '[EMAIL_MASKED]',                                              # Email
    r'(?i)(contraseña|credencial|clave)\s*:?\s*(\w+)?|pass\w+': '[PASS_MASKED]',         # Password/Credencial
    r'(\+\d{1,3}\s?[\d\s\(\)\-]{5,15}|\d{7,10})': '[PHONE_MASKED]',                      # Teléfono
    r'(?i)(calle|carrera|cll)\s\d+\s#\s?\d+-\d+': '[ADDRESS_MASKED]',                    # Dirección
}

def anonimizar_ticket(texto: str) -> tuple[str, str]:
    texto_anonimizado = texto
    anonimizado_requerido = 'No'
    
    for patron, token in PATRONES_ANONIMIZACION.items():
        if re.search(patron, texto_anonimizado, re.IGNORECASE):
            texto_anonimizado = re.sub(patron, token, texto_anonimizado, flags=re.IGNORECASE)
            anonimizado_requerido = 'Sí'
    
    return texto_anonimizado, anonimizado_requerido


# ---------------------------------------------------------------------
# FASE 3 Y 4: MÓDULO DE IA Y STORYTELLING
# ---------------------------------------------------------------------

# Sentimientos (3.1)
POLARIDAD_SENTIMIENTOS = {
    'excelente': 0.9, 'mejora': 0.7, 'funciona': 0.6, 'gracias': 0.5, 'bueno': 0.4,
    'crítico': -0.9, 'fallo': -0.8, 'error': -0.7, 'urgente': -0.6, 'problema': -0.5
}

def calcular_sentimiento(texto_anonimizado: str) -> float:
    """Calcula la métrica numérica de Sentimiento/Frustración (RF 2.1)."""
    texto_lower = texto_anonimizado.lower()
    puntuacion_neta = sum(valor for palabra, valor in POLARIDAD_SENTIMIENTOS.items() if palabra in texto_lower)
    sentimiento_score = np.tanh(puntuacion_neta)
    return round(float(sentimiento_score), 2)


def flujo_ia_simulado(registro_ticket: Dict[str, Any], texto_anonimizado: str, tickets_mes: List[int]):
    """
    Simula la ejecución de las Fases 3 (IA) y 4 (Insights y Recomendación).
    (RF 3.1, RF 3.2, RF 4.2, RF 5.1).
    """
    
    print("\n--- INICIO DE PROCESAMIENTO DE IA Y STORYTELLING ---")
    
    # Muestra los números de ticket en el mes
    print(f"Tickets en el Mes ({len(tickets_mes)}):")
    
    # FASE 3.1: Cálculo de Sentimiento
    sentimiento_score = calcular_sentimiento(texto_anonimizado)
    registro_ticket['Sentimiento'] = sentimiento_score
    print(f"NLP - Sentimiento Calculado: {sentimiento_score}")
    
    # FASE 3.3/3.4: Clasificación y Churn
    antiguedad = registro_ticket['Antigüedad_Contrato']
    volumen = registro_ticket['Volumen_Tickets_Ult_Mes']
    
    is_evolutivo = ('feature' in texto_anonimizado.lower() or 'mejora' in texto_anonimizado.lower())
    
    if is_evolutivo and sentimiento_score > 0.4:
        registro_ticket['Tipo_Mantenimiento'] = 'Evolutivo'
        riesgo_churn_base = 15 # Bajo riesgo para Evolutivo
    else:
        registro_ticket['Tipo_Mantenimiento'] = 'Correctivo'
        riesgo_churn_base = 25 # Base de Correctivo
        
    # Ajustes de Riesgo (Simulación de Pesos del Modelo - RF 3.2, RF 4.1)
    ajuste_sentimiento_peso = (1 - sentimiento_score) * 20 
    ajuste_antiguedad_peso = 30 if (antiguedad % 12 == 0 and antiguedad >= 12) or (antiguedad % 24 == 0 and antiguedad >= 24) else 0
    ajuste_volumen_peso = 25 if volumen > 10 else 0
    
    riesgo_final = int(np.clip(riesgo_churn_base + ajuste_sentimiento_peso + ajuste_antiguedad_peso + ajuste_volumen_peso, 0, 100))
    registro_ticket['Riesgo_Churn_Real'] = riesgo_final
    
    print(f"IA - Tipo: {registro_ticket['Tipo_Mantenimiento']}, Riesgo Churn: {riesgo_final}")
    
    
    # FASE 4.2: Generación del Insight Clave (RF 4.2)
    
    if registro_ticket['Tipo_Mantenimiento'] == 'Evolutivo':
        insight_clave = "El impulsor es una Oportunidad de Mantenimiento Evolutivo."
    elif ajuste_sentimiento_peso > max(ajuste_antiguedad_peso, ajuste_volumen_peso) and riesgo_final > 60:
        insight_clave = f"El riesgo es impulsado por una Frustración Crítica ({sentimiento_score}) en el ticket."
    elif ajuste_antiguedad_peso > ajuste_volumen_peso and riesgo_final > 50:
        insight_clave = f"El riesgo se relaciona con la Antigüedad del Contrato ({antiguedad} meses) y fin del ciclo de garantía."
    elif ajuste_volumen_peso > 0 and riesgo_final > 50:
        insight_clave = f"El riesgo se asocia al Alto Volumen de Tickets Correctivos ({volumen}) en el último mes."
    else:
        insight_clave = "El riesgo se asocia a fallas técnicas menores."
        
    registro_ticket['Insight_Clave'] = insight_clave
    print(f"💡 Insight Clave: {insight_clave}")

    if riesgo_final >= 80:
        recomendacion = "ACCIÓN INMEDIATA / RETENCIÓN URGENTE. Ofrecer una compensación financiera o descuento para mitigar el riesgo CRÍTICO."
    elif 50 <= riesgo_final < 80 and registro_ticket['Tipo_Mantenimiento'] == 'Evolutivo':
        recomendacion = "CONVERTIR EN VENTA / OFERTA PROACTIVA. Generar una propuesta comercial detallada de Mantenimiento Evolutivo."
    elif 50 <= riesgo_final < 80 and registro_ticket['Tipo_Mantenimiento'] == 'Correctivo':
        recomendacion = "ESCALAR A GERENCIA / VIP. El Account Manager debe contactar personalmente al cliente en menos de 4 horas."
    else: 
        recomendacion = "🔵 MONITOREO ACTIVO. Asegurar la solución rápida. El Account Manager debe enviar un correo de seguimiento personalizado."

    registro_ticket['Recomendacion_Accionable'] = recomendacion
    print(f"\nRECOMENDACIÓN FINAL para Account Manager: {recomendacion}")
    print("--- FIN DE PROCESAMIENTO DE IA Y STORYTELLING ---")
    
    return registro_ticket

# FUNCIÓN PRINCIPAL

def solicitar_datos():
    
    # 1. Obtener metadatos calculados (Antigüedad y Volumen)
    antiguedad, volumen, tickets_mes = obtener_metadatos_cliente()

    # 2. Generar ID secuencial
    ticket_id = generar_id()
    print("\n" + "="*80)
    print(f"Nuevo Ticket Creado - ID: {ticket_id}")
    print("="*80)

    # 3. Solo se solicita la descripción
    descripcion = input("1. Ingrese el texto del Nuevo Ticket (Descripción del Caso):\n> ")
    
    print(f"\n2. Antigüedad del Contrato (Asignada): {antiguedad} meses")
    print(f"3. Volumen de Tickets (Calculado): {volumen} en el mes actual")

    registro_ticket = {
        'ID_Ticket': ticket_id, 'Descripción_Caso': descripcion, 
        'Antigüedad_Contrato': antiguedad, 'Volumen_Tickets_Ult_Mes': volumen,
        'Segmento_Cliente': 'A', 'Es_Phishing_Real': 'No', 
        'Anonimizado_Requerido': 'No', 'Sentimiento': '', 
        'Tipo_Mantenimiento': '', 'Riesgo_Churn_Real': '', 
        'Insight_Clave': '', 'Recomendacion_Accionable': ''
    }
    
    # --- FASE 2.1: Detección de Phishing ---
    es_phishing = detectar_phishing(descripcion)
    registro_ticket['Es_Phishing_Real'] = 'Sí' if es_phishing else 'No'
    
    if es_phishing:
        print("ALERTA: Patrón de Phishing detectado.")
        print("FLUJO DETENIDO. El ticket ha sido aislado por riesgo de Phishing.")
        
    else:
        print("Detección de Phishing: Ningún riesgo de seguridad explícito.")
        
        # --- FASE 2.2: Anonimización/Enmascaramiento (PBD) ---
        texto_anonimizado, anonimizado_requerido = anonimizar_ticket(descripcion)
        registro_ticket['Anonimizado_Requerido'] = anonimizado_requerido
        
        if anonimizado_requerido == 'Sí':
            print(f"   Anonimización completa. Se enmascaró: SÍ (Patrones de PII/Credenciales)")
            print(f"   Texto Anonimizado: {texto_anonimizado}")
        else:
             print(f"Anonimización completa. Se enmascaró: NO")
        
        # --- FASES 3 y 4: Ejecución IA y Storytelling ---
        registro_ticket = flujo_ia_simulado(registro_ticket, texto_anonimizado, tickets_mes)
        
    guardar_registro(registro_ticket)
    print("----------------------------------------------------------------")


# --- PUNTO DE ENTRADA AL PROTOTIPO ---
def run_prototipo():
    """Orquesta la generación de datos y el procesamiento del nuevo ticket."""
    
    # 1. Genera el historial (solo si no existe)
    if not os.path.exists(NOMBRE_CSV_HISTORIAL):
        generate_historical_data()
        
    # 2. Prepara el archivo de salida
    setup_csv_output()
    
    # 3. Solicita el nuevo ticket y procesa
    solicitar_datos()

# Ejecutar el prototipo
if __name__ == "__main__":
    run_prototipo()
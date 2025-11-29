# analyzer.py - Clasificación y análisis de sentimiento
# Aquí puedes sustituir por modelos reales (transformers/spacy) luego.


def classify_maintenance(texto: str) -> str:
    """
    Clasifica el tipo de mantenimiento según palabras clave.
    - Correctivo: errores o fallos.
    - Evolutivo: mejoras o solicitudes nuevas.
    - Otro: no coincide con patrones conocidos.
    """
    t = texto.lower()

    if any(k in t for k in ["error", "fallo", "bug", "no funciona", "crash"]):
        return "Correctivo"

    if any(k in t for k in ["mejora", "feature", "nueva", "requerimiento", "solicito"]):
        return "Evolutivo"

    return "Otro"


def analyze_sentiment(texto: str) -> float:
    """
    Retorna un score entre -1.0 (muy negativo) y +1.0 (muy positivo).
    Implementación ligera basada en diccionario; se recomienda
    reemplazar por un modelo de HuggingFace para producción.
    """

    negatives = ["mal", "error", "problema", "urgente", "fatal", "insatisfecho", "cancelar"]
    positives = ["bien", "excelente", "gracias", "perfecto", "funcionó", "satisfecho"]

    score = 0
    t = texto.lower()

    # Sumar puntos positivos
    for w in positives:
        if w in t:
            score += 1

    # Restar puntos negativos
    for w in negatives:
        if w in t:
            score -= 1

    # Normalizar score entre -1.0 y 1.0
    if score == 0:
        return 0.0
    if score > 0:
        return min(score, 3) / 3.0
    return max(score, -3) / 3.0

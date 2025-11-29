# churn.py - heurística simple de score de fuga

def predict_churn(texto: str, mantenimiento: str, sentimiento: float) -> int:
    """
    Calcula un score de posible fuga (churn) basado en:
    - Tipo de mantenimiento
    - Sentimiento del ticket
    - Palabras clave críticas

    Retorna un número entre 0 y 100.
    """
    score = 0

    # Correctivo → mayor riesgo
    if mantenimiento == "Correctivo":
        score += 25

    # Sentimiento muy negativo
    if sentimiento < -0.3:
        score += 40

    # Indicios fuertes de fuga
    texto_lower = texto.lower()
    if "cancelar" in texto_lower or "no renovar" in texto_lower:
        score += 50

    return min(100, score)
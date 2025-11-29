import re

def clean_text(texto: str) -> str:
    """
    Limpia texto básico:
    - Maneja None o cadenas vacías
    - Remueve espacios múltiples
    - Normaliza espacios al inicio y final
    """
    if not texto:
        return ''

    # Reemplazar múltiples espacios por uno solo y recortar
    t = re.sub(r"\s+", " ", texto).strip()
    return t

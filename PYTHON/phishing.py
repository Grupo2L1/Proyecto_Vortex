# phishing.py - patrones simples; puede evolucionar a ML

def detect_phishing(texto: str) -> bool:
    """
    Detecta señales simples de phishing usando patrones estáticos.
    Retorna True si encuentra indicios sospechosos.
    """
    t = texto.lower()

    patterns = [
        "bit.ly/",
        "t.co/",
        "haga clic aquí",
        "click here",
        "ingresar sus credenciales",
        "verifica tu cuenta",
        "su cuenta será suspendida",
        "renovar"
    ]

    return any(p in t for p in patterns)

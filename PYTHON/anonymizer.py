import re

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}")
PASS_RE = re.compile(r"(pass|password|contraseña)[:= ]?\S+", re.IGNORECASE)
NUM_RE = re.compile(r"\b\d{10,19}\b")


def anonymize_text(texto: str) -> str:
    out = texto
    out = EMAIL_RE.sub('[EMAIL_OCULTO]', out)
    out = PASS_RE.sub('[PASS_OCULTO]', out)
    out = NUM_RE.sub('[NUM_OCULTO]', out)
    return out

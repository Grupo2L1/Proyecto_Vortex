from pydantic import BaseModel

class Ticket(BaseModel):
    texto: str
    cliente: str | None = "Desconocido"

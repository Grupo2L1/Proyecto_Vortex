from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.analyzer import classify_maintenance, analyze_sentiment
from services.anonymizer import anonymize_text
from services.phishing import detect_phishing
from services.churn import predict_churn
from utils.cleaner import clean_text


class TicketIn(BaseModel):
    texto: str
    cliente: str | None = "Desconocido"


app = FastAPI(title="Proyecto Vortex - API")


# Permitir llamadas desde frontend local. Ajusta orígenes según despliegue.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/procesar")
async def procesar_ticket(ticket: TicketIn):
    try:
        # 1. Limpieza de ruido
        texto = clean_text(ticket.texto)

        # 2. Módulos del pipeline
        phishing = detect_phishing(texto)
        mantenimiento = classify_maintenance(texto)
        sentimiento = analyze_sentiment(texto)
        anonimizado = anonymize_text(texto)
        churn = predict_churn(texto, mantenimiento, sentimiento)

        # 3. Respuesta JSON
        return {
            "cliente": ticket.cliente,
            "phishing": phishing,
            "mantenimiento": mantenimiento,
            "sentimiento": sentimiento,
            "anonimizado": anonimizado,
            "churn": churn
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar primero requirements para aprovechar la cache de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer puerto del backend
EXPOSE 8000

# Comando de arranque — IMPORTANTE:
# "main:app" debe coincidir con el nombre del archivo donde está FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

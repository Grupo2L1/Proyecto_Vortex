# 🚀 PROYECTO VORTEX  
**Plataforma de Soporte Inteligente**

---

## 🎯 Objetivo General
Crear una **IA** que genere **alertas de riesgo proactivas (churn)** y proteja la empresa mediante **ciberseguridad**.

---

## 📂 Fases del Proyecto

### 🔹 Fase 1: Planificación y Diseño del Dataset
**Objetivo:** Establecer la estructura de datos y el entorno de entrada.

| ID  | Paso Clave                  | Objetivo                                                   | RF Relacionado |
|-----|-----------------------------|-----------------------------------------------------------|----------------|
| 1.1 | Definición del Esquema CSV  | Crear el archivo `dataset.csv` con todos los campos.       | (Preparación)  |
| 1.2 | Configuración del Entorno   | Instalar librerías (Pandas, Re, TF, NLTK/SpaCy).           | (Preparación)  |
| 1.3 | Módulo de Entrada de Datos  | Desarrollar el script para solicitar inputs y generar ID.  | (Preparación)  |

---

### 🔹 Fase 2: Módulo de Seguridad y Pre-Procesamiento (Etapa 1)
**Objetivo:** Limpiar y proteger el ticket (**Ciberseguridad**).

| ID  | Paso Clave                          | Objetivo                                                   | RF Relacionado |
|-----|-------------------------------------|-----------------------------------------------------------|----------------|
| 2.1 | Detección de Phishing               | Analizar texto para patrones de ataque. Si 'Sí', AISLAR.   | RF 1.1         |
| 2.2 | Anonimización/Enmascaramiento (PBD) | Ocultar credenciales y PII simuladas (`[EMAIL_MASKED]`).   | RF 1.2         |

---

### 🔹 Fase 3: Análisis de IA y Predicción (Etapas 2 y 3)
**Objetivo:** Traducir el texto a métricas numéricas y ejecutar los modelos centrales.

| ID  | Paso Clave                     | Objetivo                                                                 | RF Relacionado |
|-----|--------------------------------|-------------------------------------------------------------------------|----------------|
| 3.1 | Análisis de Sentimientos       | Generar métrica numérica de Sentimiento/Frustración (-1.0 a +1.0).       | RF 2.1         |
| 3.2 | Vectorización de Texto         | Convertir texto anonimizado en vectores (Word Embeddings) para la IA.    | (Técnico)      |
| 3.3 | Clasificación de Mantenimiento | Ejecutar Modelo N° 1: Clasificar en 'Correctivo' o 'Evolutivo'.          | RF 3.1         |
| 3.4 | Predicción de Riesgo de Churn  | Ejecutar Modelo N° 2: Calcular puntuación `Riesgo_Churn_Real` (0-100).   | RF 3.2         |

---

### 🔹 Fase 4: Insights y Storytelling (Etapas 4 y 5)
**Objetivo:** Extraer la causa raíz del riesgo y generar la acción para el **Account Manager**.

| ID  | Paso Clave                   | Objetivo                                                                 | RF Relacionado |
|-----|------------------------------|-------------------------------------------------------------------------|----------------|
| 4.1 | Cálculo de Correlaciones     | Analizar el impacto de las variables de entrada en el Riesgo de Churn.   | RF 4.1         |
| 4.2 | Generación del Insight Clave | Identificar el factor principal que impulsa el riesgo de churn.          | RF 4.2         |
| 4.3 | Motor de Recomendación       | Generar una instrucción directa y clara (ej. "Ofrecer descuento").       | RF 5.1         |
| 4.4 | Informe Visual y CSV Final   | Presentar resultados en dashboard y registrar en el CSV.                 | (RNF/UX)       |

---

### 🔹 Fase 5: Pruebas y Documentación
**Objetivo:** Validar el prototipo y formalizar los entregables.

| ID  | Paso Clave             | Objetivo                                                   |
|-----|------------------------|-----------------------------------------------------------|
| 5.1 | Pruebas de Aceptación  | Ejecutar el flujo completo con los datos de prueba.        |
| 5.2 | Documentación Técnica  | Finalizar la documentación del código y los entregables.   |

---

## 📌 Notas Finales
- Este proyecto busca integrar **IA + Ciberseguridad** en un flujo reproducible y claro.  
- Cada fase está diseñada para ser **modular**, facilitando pruebas y escalabilidad.  
- La documentación se mantendrá actualizada conforme avance el desarrollo.  

---

## 👨‍💻 Autor
**Proyecto desarrollado por: **
                    Lorena Fonton
                    **Movil: ** +057 3174070511
                 **Contacto: ** linkedin.com/in/geidyponton-desarrolladora-fron-end
                    Ricardo Martínez
                    **Movil: ** 3157855136
                   **E-Mail: ** andresm2477@gmail.com

Gracias por visitar nuestro repositorio.

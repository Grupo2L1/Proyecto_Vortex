import pandas as pd
import numpy as np
import re

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class TextAnalyzer:
    """
    Etapa 2: Análisis de Texto
    - Preprocesamiento
    - Vectorización TF-IDF
    - Análisis de Sentimiento (Score numérico)
    """

    def __init__(self, language="spanish"):
        # 1. Inicializar Stemmer y Stopwords
        self.stemmer = SnowballStemmer(language)

        try:
            self.stop_words = set(stopwords.words(language))
        except LookupError:
            print(f"[WARN] No se encontraron stopwords para {language}.")
            self.stop_words = set()

        # 2. Sentiment Analyzer (VADER)
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except:
            raise ValueError(
                "VADER no encontrado. Ejecuta: nltk.download('vader_lexicon')"
            )

        # 3. TF-IDF
        self.tfidf_vectorizer = TfidfVectorizer()
        self.vectorizer_fitted = False  # ← control adicional

    # ---------------------------------------------------------
    # PREPROCESAMIENTO
    # ---------------------------------------------------------
    def _pre_procesar_texto(self, text: str) -> str:
        """Limpia, tokeniza y aplica stemming."""
        text = text.lower()
        tokens = word_tokenize(text)

        tokens_procesados = [
            self.stemmer.stem(w)
            for w in tokens
            if w.isalnum() and w not in self.stop_words
        ]

        return " ".join(tokens_procesados)

    # ---------------------------------------------------------
    # SENTIMIENTO
    # ---------------------------------------------------------
    def calcular_sentimiento(self, text: str) -> float:
        """Retorna score compuesto (-1 a 1)."""
        score = self.sentiment_analyzer.polarity_scores(text)
        return score["compound"]

    # ---------------------------------------------------------
    # VECTORIZACIÓN (ENTRENAMIENTO)
    # ---------------------------------------------------------
    def vectorizar_texto_batch(self, textos: list[str]):
        """Ajusta el TF-IDF con el dataset completo."""
        print("[INFO] Preprocesando textos...")
        textos_proc = [self._pre_procesar_texto(t) for t in textos]

        matriz = self.tfidf_vectorizer.fit_transform(textos_proc)
        self.vectorizer_fitted = True

        print("[OK] Vectorizador TF-IDF entrenado.")
        return matriz

    # ---------------------------------------------------------
    # VECTORIZACIÓN (NUEVO TICKET)
    # ---------------------------------------------------------
    def transformar_nuevo_ticket(self, descripcion_anonimizada: str):
        """Transforma un ticket ya que TF-IDF estaba entrenado."""
        if not self.vectorizer_fitted:
            raise ValueError(
                "ERROR: El vectorizador TF-IDF no está entrenado. "
                "Primero llama a vectorizar_texto_batch()."
            )

        texto_proc = self._pre_procesar_texto(descripcion_anonimizada)
        vector = self.tfidf_vectorizer.transform([texto_proc])
        return vector

    # ---------------------------------------------------------
    # PIPELINE INDIVIDUAL
    # ---------------------------------------------------------
    def procesar_texto_ticket(self, descripcion_anonimizada: str):
        """
        Calcula:
        - score numérico de sentimiento
        - texto preprocesado (para vectorizar)
        """
        sentimiento = self.calcular_sentimiento(descripcion_anonimizada)
        texto_proc = self._pre_procesar_texto(descripcion_anonimizada)

        return sentimiento, texto_proc

import pandas as pd
import numpy as np
import re
# Asegúrate de haber instalado: pip install nltk scikit-learn
# Y haber ejecutado: import nltk; nltk.download(['punkt', 'stopwords', 'vader_lexicon', 'rslp'])

# Se importan las herramientas necesarias para NLP
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer 

class TextAnalyzer:
    """
    Clase encargada de ejecutar la Etapa 2: Análisis de Texto.
    Realiza Vectorización y Análisis de Sentimientos, traduciendo el lenguaje natural
    en métricas numéricas para las Redes Neuronales. [cite: 88, 89]
    """

    def __init__(self, language='spanish'):
        # 1. Inicializar Stemmer y Stopwords en español
        self.stemmer = SnowballStemmer(language)
        # Usamos try-except ya que 'rslp' es el stemmer, pero 'spanish' es la lista de stopwords.
        try:
             self.stop_words = set(stopwords.words(language))
        except LookupError:
             print(f"Advertencia: No se encontraron stopwords para {language}. Asegúrate de ejecutar nltk.download('stopwords').")
             self.stop_words = set()

        # 2. Inicializar el Analizador de Sentimientos (VADER)
        # Nota: VADER está optimizado para inglés, su uso en español es una aproximación
        # a menos que se use un léxico específico en español.
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # 3. Inicializar el Vectorizador TF-IDF (se ajustará con el dataset completo más adelante)
        self.tfidf_vectorizer = TfidfVectorizer()


    def _pre_procesar_texto(self, text: str) -> str:
        """
        Limpia, tokeniza y aplica Stemming (lematización) al texto para la vectorización.
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Tokenización
        tokens = word_tokenize(text)
        
        # Eliminar Stop Words, caracteres no alfabéticos y aplicar Stemming
        processed_tokens = [
            self.stemmer.stem(w) for w in tokens 
            if w.isalnum() and w not in self.stop_words
        ]
        
        return " ".join(processed_tokens)

    def calcular_sentimiento(self, text: str) -> float:
        """
        Calcula la métrica numérica de Sentimiento/Nivel de Frustración del cliente. [cite: 91]
        Retorna la puntuación compuesta (escala de -1 a 1).
        """
        # Calcular los scores de polaridad
        vs = self.sentiment_analyzer.polarity_scores(text)
        # El score compuesto es la métrica numérica de sentimiento
        return vs['compound'] 

    def vectorizar_texto_batch(self, textos: list[str]):
        """
        Ajusta y transforma un conjunto de textos usando TF-IDF.
        Esta función se usa para entrenar/ajustar el modelo con el conjunto de datos completo.
        """
        print("Pre-procesando textos para Vectorización...")
        # Pre-procesamiento de todo el conjunto de textos
        textos_procesados = [self._pre_procesar_texto(t) for t in textos]
        
        # Vectorización (Ajustar y Transformar)
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(textos_procesados)
        
        # Retorna la matriz TF-IDF (representación numérica)
        return tfidf_matrix
    
    def transformar_nuevo_ticket(self, descripcion_anonimizada: str):
        """
        Transforma un ticket individual usando el vectorizador pre-ajustado.
        """
        texto_procesado = self._pre_procesar_texto(descripcion_anonimizada)
        # Usamos .transform() para aplicar el vocabulario aprendido
        vector_tfidf = self.tfidf_vectorizer.transform([texto_procesado])
        return vector_tfidf

    def procesar_texto_ticket(self, descripcion_anonimizada: str) -> tuple[float, str]:
        """
        Calcula la característica de Sentimiento para un ticket individual.
        """
        # Generar una métrica numérica de Sentimiento/Nivel de Frustración [cite: 91]
        sentimiento_score = self.calcular_sentimiento(descripcion_anonimizada)
        
        # Pre-procesar para usar con el vectorizador ajustado en la función de transformar_nuevo_ticket
        texto_pre_procesado = self._pre_procesar_texto(descripcion_anonimizada)
        
        # Retorna el score de sentimiento (característica numérica) y el texto pre-procesado
        return sentimiento_score, texto_pre_procesado
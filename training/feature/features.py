from enum import Enum
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from training.feature.tfidf_google_embedding_vectorizer import TfidfGoogleEmbeddingVectorizer
from training.feature.google_embedding_vectorizer import GoogleEmbeddingVectorizer
from training.feature.punctuation_feature import PunctuationVectorizer


class Features(Enum):
    TfidfVectorizer = TfidfVectorizer
    CountVectorizer = CountVectorizer
    TfidfGoogleEmbeddingVectorizer = TfidfGoogleEmbeddingVectorizer
    GoogleEmbeddingVectorizer = GoogleEmbeddingVectorizer
    PunctuationVectorizer = PunctuationVectorizer


from enum import Enum
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


class Features(Enum):
    TfidfVectorizer = TfidfVectorizer
    CountVectorizer = CountVectorizer

from enum import Enum
from training.feature.tfidf_feature import TfidfFeature
from training.feature.wordcount_feature import WordcountFeature


class Features(Enum):
    TfidfFeature = TfidfFeature
    WordcountFeature = WordcountFeature

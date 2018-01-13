from sklearn.feature_extraction.text import TfidfVectorizer
from training.feature.feature import Feature


class TfidfFeature(Feature):
    def process_corpus(self, corpus):
        self.featureModel = TfidfVectorizer()
        return self.featureModel.fit_transform(corpus)

    def process_single(self, document):
        return self.featureModel.transform(document)

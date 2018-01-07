from sklearn.feature_extraction.text import CountVectorizer
from training.feature.feature import Feature


class WordcountFeature(Feature):
    def process_corpus(self, corpus):
        self.featureModel = CountVectorizer()
        return self.featureModel.fit_transform(corpus)

    def process_single(self, document):
        return self.featureModel.transform([document])

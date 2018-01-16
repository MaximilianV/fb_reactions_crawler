import numpy as np
from training.feature.google_embedding_feature import GoogleEmbeddingFeature


class GoogleEmbeddingVectorizer(GoogleEmbeddingFeature):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in self.tokenize_doc(words) if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

import numpy as np
import training.feature.google_embedding_feature as gef


class GoogleEmbeddingVectorizer(gef.GoogleEmbeddingFeature):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([gef.w2v_model[w] for w in self.tokenize_doc(words) if w in gef.w2v_model]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

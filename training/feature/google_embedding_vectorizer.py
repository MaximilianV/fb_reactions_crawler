import numpy as np
import training.feature.google_embedding_feature as gef


class GoogleEmbeddingVectorizer(gef.GoogleEmbeddingFeature):
    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([1 + gef.w2v_model[word] for word in self.tokenize_doc(doc) if word in gef.w2v_model]
                    or [np.zeros(self.dim)], axis=0)
            for doc in X
        ])

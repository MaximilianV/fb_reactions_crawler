import numpy as np


class PunctuationFeature:
    def fit(self, X, y):
        return self

    def transform(self, X):
        output = np.array([[]])
        for doc in X:
            output = np.append(output, np.array([[doc.count('.'), doc.count('!'), doc.count('?')]]), axis=0)
        return output

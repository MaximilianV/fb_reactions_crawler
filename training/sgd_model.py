import logging
from sklearn.linear_model import SGDClassifier
from .model import Model


class SgdModel(Model):
    def set_model(self):
        self.model = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)

    """
    def train(self, features, classification):
        logging.debug("Training SVM model...")
        self.model = MultinomialNB()
        self.model.fit(features, classification)
        logging.debug("Finished training.")
    """

    def classify(self, document_features):
        return self.model.predict(document_features)

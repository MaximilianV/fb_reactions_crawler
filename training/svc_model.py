import logging
from sklearn import svm
from .model import Model


class SvcModel(Model):
    def set_model(self):
        self.model = svm.LinearSVC()

    """
    def train(self, features, classification):
        logging.debug("Training SVM model...")
        self.model = MultinomialNB()
        self.model.fit(features, classification)
        logging.debug("Finished training.")
    """

    def classify(self, document_features):
        return self.model.predict(document_features)

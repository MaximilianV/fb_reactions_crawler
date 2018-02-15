import logging
from sklearn.naive_bayes import BernoulliNB
from .model import Model


class BernoulliModel(Model):
    def set_model(self):
        self.model = BernoulliNB()

    """
    def train(self, features, classification):
        logging.debug("Training SVM model...")
        self.model = MultinomialNB()
        self.model.fit(features, classification)
        logging.debug("Finished training.")
    """

    def classify(self, document_features):
        return self.model.predict(document_features)

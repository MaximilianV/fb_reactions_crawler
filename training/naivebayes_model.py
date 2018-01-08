import logging
from sklearn.naive_bayes import MultinomialNB
from .model import Model


class NaiveBayesModel(Model):
    def train(self, features, classification):
        logging.debug("Training SVM model...")
        self.model = MultinomialNB()
        self.model.fit(features, classification)
        print(features)
        print(classification)
        logging.debug("Finished training.")

    def classify(self, document_features):
        return self.model.predict(document_features)

import logging
from sklearn.ensemble import RandomForestClassifier
from .model import Model


class RandomForestModel(Model):
    def set_model(self):
        self.model = RandomForestClassifier(max_depth=2, random_state=0)

    """
    def train(self, features, classification):
        logging.debug("Training SVM model...")
        self.model = MultinomialNB()
        self.model.fit(features, classification)
        logging.debug("Finished training.")
    """

    def classify(self, document_features):
        return self.model.predict(document_features)

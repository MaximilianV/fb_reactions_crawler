import logging
from sklearn import svm
from .model import Model


class SvmModel(Model):
    def train(self, features, classification):
        logging.debug("Training SVM model...")
        self.model = svm.SVC()
        self.model.fit(features, classification)
        print(features)
        print(classification)
        logging.debug("Finished training.")

    def classify(self, document_features):
        return self.model.predict(document_features)

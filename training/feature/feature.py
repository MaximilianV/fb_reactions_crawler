from sklearn.externals import joblib
import logging


class Feature:
    def __init__(self, feature_data=None):
        self.logger = logging.getLogger(__name__)
        if feature_data:
            self.logger.debug("Loading feature model")
            self.featureModel = joblib.load(feature_data)

    def process_corpus(self, corpus):
        pass

    def persist(self, path):
        self.logger.debug("Persisting feature model.")
        joblib.dump(self.featureModel, path)

    def process_single(self, document):
        pass

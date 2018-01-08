import logging
import json
from sklearn.externals import joblib


class Model:

    reactions = {"love": 0, "haha": 1, "wow": 2, "sad": 3, "angry": 4}
    reaction_ids = {0: "love", 1: "haha", 2: "wow", 3: "sad", 4: "angry"}

    def __init__(self, model_dump=None):
        self.features = []
        self.feature_objects = []
        self.model = None
        self.logger = logging.getLogger(__name__)

        Model.setup_logging()

        if model_dump:
            self.load(model_dump)

    def select_features(self, features):
        self.features = features

    def train_from_file(self, file):
        self.logger.debug("Loading posts from " + file)
        with open(file, 'r') as infile:
            posts = json.load(infile)
        self.logger.debug("Converting posts to corpus array.")
        corpus = map(lambda post: post['message'], posts)
        reactions = list(map(lambda post: Model.translate_reaction(post['reaction']), posts))
        self.train(self.extract_features(corpus), reactions)

    def train(self, features, classification):
        pass

    def extract_features(self, corpus):
        # TODO: Allow multiple features
        features = None
        for feature_class in self.features:
            feature_object = feature_class.value()
            features = feature_object.process_corpus(corpus)
            self.feature_objects.append(feature_object)
        return features

    def extract_features_from_document(self, document):
        # TODO: Allow multiple features
        features = None
        for feature_object in self.feature_objects:
            features = feature_object.process_single(document)
        return features

    def persist(self):
        self.logger.debug("Persisting model.")
        joblib.dump(self.model, "data/models/model.pkl")
        for feature_object in self.feature_objects:
            feature_object.persist()

    def load(self, model_dump):
        self.logger.debug("Loading model.")
        self.model = joblib.load(model_dump)

    def predict(self, document):
        return self.classify(self.extract_features_from_document(document))

    def classify(self, document_features):
        pass

    @staticmethod
    def translate_reaction(reaction):
        return Model.reactions[reaction]

    @staticmethod
    def translate_reaction_id(reaction_id):
        return Model.reaction_ids[reaction_id]

    @staticmethod
    def setup_logging():
        # Setup logger
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("{0}/{1}.log".format("logs", "training")),
                logging.StreamHandler()
            ])

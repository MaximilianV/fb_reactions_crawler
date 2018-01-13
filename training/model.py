import logging
import json
from sklearn.externals import joblib
from sklearn.pipeline import FeatureUnion


class Model:

    reactions = {"joy": 0, "surprise": 1, "sadness": 2, "anger": 3}
    reaction_ids = {0: "joy", 1: "surprise", 2: "sadness", 3: "anger"}

    def __init__(self, model_dump=None):
        self.features = []
        self.feature_union = None
        self.model = None
        self.logger = logging.getLogger(__name__)

        Model.setup_logging()

        if model_dump:
            self.load(model_dump)

    def select_features(self, features):
        self.features = features

    def create_feature_union(self):
        features = []
        self.ensure_is_set(self.features, "No features selected before training was started.")
        for feature in self.features:
            features.append((feature.name, feature.value()))
        self.feature_union = FeatureUnion(features)
        self.logger.debug("Created a FeatureUnion: \n" + str(self.feature_union))

    def train_from_file(self, file):
        self.create_feature_union()
        self.logger.debug("Loading posts from " + file)
        with open(file, 'r') as infile:
            posts = json.load(infile)
        self.logger.debug("Converting posts to corpus array.")
        corpus = map(lambda post: post['message'], posts)
        reactions = list(map(lambda post: Model.translate_reaction(post['reaction']), posts))
        self.train(self.feature_union.fit_transform(corpus), reactions)

    def train(self, features, classification):
        pass

    def extract_features_from_document(self, document):
        self.ensure_is_set(self.feature_union, "A feature union needs to be created before predicting a document.")
        return self.feature_union.transform(document)

    def persist(self, path):
        self.logger.debug("Persisting model.")
        joblib.dump(self.model, path + ".model")
        self.logger.debug("Persisting features.")
        joblib.dump(self.feature_union, path + ".features")

    def load(self, model_dump):
        self.logger.debug("Loading model.")
        self.model = joblib.load(model_dump + ".model")
        self.logger.debug("Loading features.")
        self.feature_union = joblib.load(model_dump + ".features")

    def predict(self, document):
        return self.classify(self.extract_features_from_document(document))

    def classify(self, document_features):
        pass

    def ensure_is_set(self, var, message=None):
        if not var:
            if message:
                self.logger.error(message)
            else:
                self.logger.error("Some variable is not set!")
            exit(1)

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

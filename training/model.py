import logging
import json
from sklearn.externals import joblib
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.model_selection import GridSearchCV


class Model:

    reactions = {"joy": 0, "surprise": 1, "sadness": 2, "anger": 3}
    reaction_ids = {0: "joy", 1: "surprise", 2: "sadness", 3: "anger"}
    reaction_labels = ["joy", "surprise", "sadness", "anger"]

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
        for feature_class in self.features:
            features.append((feature_class.name, feature_class.value()))
        self.feature_union = FeatureUnion(features)

    def train_from_array(self, x, y):
        self.create_feature_union()
        corpus = x
        reactions = y
        self.set_model()
        pipeline = Pipeline([("features", self.feature_union), ("model", self.model)])
        """param_grid = {'features__TfidfVectorizer__max_df': (0.5, 0.75, 1.0),
                      'features__TfidfVectorizer__max_features': (None, 5000, 10000, 50000),
                      'features__TfidfVectorizer__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
                      'features__TfidfVectorizer__use_idf': (True, False)}
                      # 'features__TfidfVectorizer__norm': ('l1', 'l2'),
                      # 'model__alpha': (0.00001, 0.000001)}
        """
        pipeline.set_params(features__TfidfVectorizer__max_df=0.5,
                            features__TfidfVectorizer__max_features=None,
                            features__TfidfVectorizer__ngram_range=(1,2),
                            features__TfidfVectorizer__use_idf=False)

        pipeline.fit(corpus, reactions)

    def train_from_file(self, file):
        self.create_feature_union()
        self.logger.debug("Loading posts from " + file)
        with open(file, 'r') as infile:
            posts = json.load(infile)
        self.logger.debug("Converting posts to corpus array.")
        corpus = list(map(lambda post: post['message'], posts))
        reactions = list(map(lambda post: Model.translate_reaction(post['reaction']), posts))
        self.set_model()
        pipeline = Pipeline([("features", self.feature_union), ("model", self.model)])
        """param_grid = {'features__TfidfVectorizer__max_df': (0.5, 0.75, 1.0),
                      'features__TfidfVectorizer__max_features': (None, 5000, 10000, 50000),
                      'features__TfidfVectorizer__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
                      'features__TfidfVectorizer__use_idf': (True, False)}
                      # 'features__TfidfVectorizer__norm': ('l1', 'l2'),
                      # 'model__alpha': (0.00001, 0.000001)}
        """
        pipeline.set_params(features__TfidfVectorizer__max_df=0.5,
                            features__TfidfVectorizer__max_features=None,
                            features__TfidfVectorizer__ngram_range=(1,2),
                            features__TfidfVectorizer__use_idf=False)

        pipeline.fit(corpus, reactions)

        """
        grid_search = GridSearchCV(pipeline, param_grid, verbose=1, n_jobs=-1)
        grid_search.fit(list(corpus), reactions)
        print("BEST MODEL:")
        print(grid_search.best_estimator_)
        print("Best score: %0.3f" % grid_search.best_score_)
        print("Best parameters set:")
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in sorted(best_parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))
        """

    def set_model(self):
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

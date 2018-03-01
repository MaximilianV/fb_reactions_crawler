from nltk import word_tokenize
import gensim

# Load Google's pre-trained Word2Vec model.
w2v_model = gensim.models.KeyedVectors.load_word2vec_format('data/models/GoogleNews-vectors-negative300.bin.gz', binary=True)


class GoogleEmbeddingFeature:
    # Classes inspired by http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
    def __init__(self):
        self.word2weight = None
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = 300

    def fit(self, X, y):
        pass

    def transform(self, X):
        pass

    @staticmethod
    def tokenize_doc(document):
        return word_tokenize(document)

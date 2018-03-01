from enum import Enum
from training.svm_model import SvmModel
from training.naivebayes_model import NaiveBayesModel
from training.bernoulli_model import BernoulliModel
from training.sgd_model import SgdModel
from training.svc_model import SvcModel
from training.randomforest_model import RandomForestModel


class Models(Enum):
    SvmModel = SvmModel
    NaiveBayesModel = NaiveBayesModel
    SgdModel = SgdModel
    SvcModel = SvcModel
    BernoulliModel = BernoulliModel
    RandomForestModel = RandomForestModel

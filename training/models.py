from enum import Enum
from training.svm_model import SvmModel
from training.naivebayes_model import NaiveBayesModel
from training.sgd_model import SgdModel


class Models(Enum):
    SvmModel = SvmModel
    NaiveBayesModel = NaiveBayesModel
    SgdModel = SgdModel

from enum import Enum
from training.svm_model import SvmModel
from training.naivebayes_model import NaiveBayesModel


class Models(Enum):
    SvmModel = SvmModel
    NaiveBayesModel = NaiveBayesModel

import argparse
from training.models import Models
from training.feature.features import Features
from training.model_manager import ModelManager
from os import path


def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a normalized json file')
    return parser.parse_args()


def main(run_args):
    # Train a SVM model with tfidf feature
    # model = SvmModel()

    # Train a Naive Bayes model with tfidf feature
    # See: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
    model = Models.NaiveBayesModel.value()

    model.select_features([Features.TfidfVectorizer])
    model.train_from_file(run_args.filename)
    model_manager = ModelManager()
    training_file = path.splitext(path.basename(run_args.filename))[0]
    model_name = model_manager.save(model, descriptive_name=True, name_appendix=training_file)
    print("Saved model to " + model_name)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

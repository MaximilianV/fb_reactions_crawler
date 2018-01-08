import argparse
from training.svm_model import SvmModel
from training.naivebayes_model import NaiveBayesModel
from training.feature.features import Features


def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a normalized json file')
    return parser.parse_args()


def main(run_args):
    # Train a SVM model with tfidf feature
    # model = SvmModel()

    # Train a Naive Bayes model with tfidf feature
    # See: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
    model = NaiveBayesModel()

    model.select_features([Features.Tfidf])
    model.train_from_file(run_args.filename)
    model.persist()

    while True:
        doc = input("What do you want me to analyse?\n")
        classification = model.predict(doc)
        print(str(classification) + " = " + model.translate_reaction_id(classification[0]))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

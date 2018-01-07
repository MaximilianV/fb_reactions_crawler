import argparse
from training.svm_model import SvmModel
from training.feature.features import Features


def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a normalized json file')
    return parser.parse_args()


def main(run_args):
    # Train a SVM model with tfidf feature
    svm_model = SvmModel()
    svm_model.select_features([Features.Wordcount])
    svm_model.train_from_file(run_args.filename)
    svm_model.persist()

    while True:
        doc = input("What do you want me to analyse?")
        classification = svm_model.predict(doc)
        print(str(classification) + " = " + svm_model.translate_reaction_id(classification[0]))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

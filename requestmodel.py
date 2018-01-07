import argparse
from sklearn.externals import joblib
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a trained model and place requests.')
    return parser.parse_args()


def main(run_args):
    # Setup logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format("logs", "requesting")),
            logging.StreamHandler()
        ])

    logging.debug("Loading vectorizer.")
    vectorizer = joblib.load("data/vectorizer.pkl")

    logging.debug("Loading model.")
    clf = joblib.load("data/model.pkl")

    while True:
        document = input("Which sentence should be estimated?\n")
        feature = vectorizer.transform([document])
        print(clf.predict(feature))
        print("\n")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

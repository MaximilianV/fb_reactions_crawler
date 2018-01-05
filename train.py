import argparse
import json
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a normalized json file')
    return parser.parse_args()


def main(run_args):
    #Setup logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format("logs", "training")),
            logging.StreamHandler()
        ])

    filename = run_args.filename
    
    posts = None
    logging.debug("Loading posts from " + filename)
    with open(filename, 'r') as infile:
        posts = json.load(infile)

    logging.debug("Converting posts to corpus array.")
    corpus = map(lambda post: post['message'], posts)

    logging.debug("Extracting BoW vectors.")
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus)

    logging.debug("Persisting vectorizer for later use.")
    joblib.dump(vectorizer, "data/vectorizer.pkl")

    logging.debug("Training model.")
    clf = svm.SVC()
    clf.fit(features, corpus)

    # print(clf.predict([[-1., -1.]]))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

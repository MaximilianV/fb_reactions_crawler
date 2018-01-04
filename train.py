import argparse
import json
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer

def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a normalized json file')
    return parser.parse_args()

def main(run_args):
    filename = run_args.filename
    
    posts = None
    with open(filename + '.json', 'r') as infile:
        posts = json.load(infile)
    
    corpus = map(lambda post: post['message'], posts)
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus)
    print(features)
    clf = svm.SVC()
    clf.fit(features, corpus)

    # print(clf.predict([[-1., -1.]]))

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
import argparse
from training.models import Models
from training.feature.features import Features
from training.model import Model
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from collections import Counter
import json
import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('datafolder', metavar='datafolder', help='a folder with normalized files')
    return parser.parse_args()


def main(run_args):
    files = os.listdir(run_args.datafolder)
    base_dir = run_args.datafolder + "/"


    files = ["CNN_TNYT_f_n.json"]
    base_dir = "data/datasets/"


    for file in files:
        print(str(datetime.datetime.now()))
        print("Processing" + base_dir + file)
        print("Load corpus.")
        with open(base_dir + file, 'r') as infile:
            posts = json.load(infile)
        print("Converting posts to corpus array.")
        corpus = list(map(lambda post: post['message'], posts))
        reactions = list(map(lambda post: Model.translate_reaction(post['reaction']), posts))

        print("Splitting up data set.")
        X_train, X_test, y_train, y_test = train_test_split(corpus, reactions, test_size=0.33, random_state=42)

        

        model = Models.NaiveBayesModel.value()
        model.select_features([Features.TfidfVectorizer, Features.CountVectorizer])
        model.train_from_array(X_train, y_train)
        print(str(datetime.datetime.now()))
        print("Training finished.")

        predicted_reactions = model.predict(X_test)

        # print(Counter(predicted_reactions))
        file_base = file.strip('.json')
        with open(base_dir + file_base + "_eval_split.txt", 'w') as outfile:
            outfile.write(metrics.classification_report(y_test, predicted_reactions, target_names=Model.reaction_labels))
        print(str(datetime.datetime.now()))
        print("Finished " + file + ".\n\n")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

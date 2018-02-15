import argparse
from training.models import Models
from training.feature.features import Features
from training.model import Model
import os
from sklearn import metrics
from collections import Counter
import json
import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description='Train model based on normalized facebook reactions.')
    parser.add_argument('datafolder', metavar='datafolder', help='a folder with normalized files')
    parser.add_argument('evaluation_file', metavar='evaluation_file', help='a model config json file')
    return parser.parse_args()


def main(run_args):
    files = os.listdir(run_args.datafolder)
    base_dir = run_args.datafolder + "/"

    with open(run_args.evaluation_file, 'r') as infile:
        posts = json.load(infile)
    corpus = list(map(lambda post: post['message'], posts))
    reactions = list(map(lambda post: Model.translate_reaction(post['reaction']), posts))

    for file in files:
        print(str(datetime.datetime.now()))
        print("Processing" + base_dir + file)

        model = Models.NaiveBayesModel.value()
        model.select_features([Features.TfidfVectorizer, Features.CountVectorizer, Features.GoogleEmbeddingVectorizer])
        model.train_from_file(base_dir + file)
        print(str(datetime.datetime.now()))
        print("Training finished.")

        predicted_reactions = model.predict(corpus)

        # print(Counter(predicted_reactions))
        file_base = file.strip('.json')
        with open(base_dir + file_base + "_eval_fairy_micro.txt", 'w') as outfile:
            # outfile.write(metrics.classification_report(reactions, predicted_reactions, target_names=Model.reaction_labels))
            outfile.write(str(metrics.precision_recall_fscore_support(reactions, predicted_reactions, average='micro')))
        with open(base_dir + file_base + "_eval_fairy.txt", 'w') as outfile:
            outfile.write(metrics.classification_report(reactions, predicted_reactions, target_names=Model.reaction_labels))
        print(str(datetime.datetime.now()))
        print("Finished " + file + ".\n\n")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

import argparse
from training.model_manager import ModelManager
from training.model import Model
from sklearn import metrics
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description='Loads a model based on a model configuration file.')
    parser.add_argument('model_config', metavar='model_config', help='a model config json file')
    parser.add_argument('evaluation_file', metavar='evaluation_file', help='a model config json file')
    return parser.parse_args()


def main(run_args):
    model = ModelManager.load(run_args.model_config)
    with open(run_args.evaluation_file, 'r') as infile:
        posts = json.load(infile)
    corpus = map(lambda post: post['message'], posts)
    reactions = list(map(lambda post: model.translate_reaction(post['reaction']), posts))

    predicted_reactions = model.predict(corpus)
    print(metrics.classification_report(reactions, predicted_reactions, target_names=Model.reaction_labels))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

import argparse
from training.modelManager import ModelManager


def parse_arguments():
    parser = argparse.ArgumentParser(description='Loads a model based on a model configuration file.')
    parser.add_argument('filename', metavar='filename', help='a model config json file')
    return parser.parse_args()


def main(run_args):
    model = ModelManager.load(run_args.filename)

    while True:
        doc = input("What do you want me to analyse?\n")
        classification = model.predict(doc)
        print(str(classification) + " = " + model.translate_reaction_id(classification[0]))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

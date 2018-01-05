import argparse
import operator
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.moses import MosesDetokenizer


def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize filtered facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a filtered json file')
    return parser.parse_args()


def get_most_common_reaction(reactions):
    return max(reactions.items(), key=operator.itemgetter(1))[0]


def normalize(post):
    reaction = get_most_common_reaction(post['reactions'])
    message = word_tokenize(post['message'])
    sw = stopwords.words('english')

    words_without_stopwords = [word for word in message if word not in sw]

    detokenizer = MosesDetokenizer()
    message_without_stopwords = detokenizer.detokenize(words_without_stopwords, return_str=True)

    return {'message': message_without_stopwords, 'reaction': reaction}


def main(run_args):
    filename = run_args.filename
    posts = None
    with open(filename, 'r') as infile:
        posts = json.load(infile)

    normalized_posts = list(map(normalize, posts))
    filename = filename.strip('.json')
    with open(filename + '_normalized.json', 'w') as outfile:
        json.dump(normalized_posts, outfile)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

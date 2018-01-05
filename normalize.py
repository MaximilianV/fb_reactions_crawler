import argparse
import operator
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize filtered facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a filtered json file')
    return parser.parse_args()

def get_most_common_reaction(reactions):
    return max(reactions.items(), key=operator.itemgetter(1))[0]

def normalize(post):
    reaction = get_most_common_reaction(post['reactions'])
    message = word_tokenize(post['message'])
    message_without_stopwords = []
    for word in post['message']:
        if word not in stopwords.words('english'):
            message_without_stopwords.append(word)
    return {'message': post['message'], 'reaction': reaction}

def main(run_args):
    filename = run_args.filename
    posts = None
    with open(filename, 'r') as infile:
        posts = json.load(infile)
    normalized_posts = list(map(normalize, posts))
    with open(filename + '_normalized.json', 'w') as outfile:
        json.dump(normalized_posts, outfile)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
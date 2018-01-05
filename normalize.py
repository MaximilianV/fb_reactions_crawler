import argparse
import operator
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize filtered facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a filtered json file')
    return parser.parse_args()

def get_most_common_reaction(reactions):
    return max(reactions.iteritems(), key=operator.itemgetter(1))[0]

def normalize(post):
    reaction = get_most_common_reaction(post['reactions'])
    return {'message': post['message'], 'reaction': reaction}

def main(run_args):
    filename = run_args.filename
    posts = None
    with open(filename + '.json', 'r') as infile:
        posts = json.load(infile)
    normalized_posts = map(normalize, posts)
    with open(filename + '_normalized.json', 'w') as outfile:
        json.dump(normalized_posts, outfile)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
import argparse
import json
import re
from functools import reduce


def parse_arguments():
    parser = argparse.ArgumentParser(description='Filter crawled facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a json file [{"id": xxxx, "name": "page_name"}]')
    return parser.parse_args()


def post_is_useful(post):
    # Filter posts including URLs
    url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    if re.match(url_regex, post.message):
        return False
    
    # Filter posts where the highest reaction is not dominant. 
    # Default: 10% higher then the secondary reaction.
    # TODO: make percentage a command line argument
    reactions = post.reactions.values()
    highgest_reaction = max(reactions)
    reactions.remove(highgest_reaction)
    second_highgest_reaction = max(reactions)
    if (100 - 100 * second_highgest_reaction / highgest_reaction) < 10:
        return False

    # TODO: Filter posts with less than X reactions
    # TODO: Filter posts with less than X characters

    return True


def clean_post_data(posts):
    return list(filter(post_is_useful, posts.values()))


def main(run_args):
    filename = run_args.filename
    posts = None
    with open(filename + '.json', 'r') as infile:
        posts = json.load(infile)
    clean_posts = clean_post_data(posts)
    # test dump
    print(json.dumps(clean_posts, sort_keys=True, indent=4))


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

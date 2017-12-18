import argparse
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description='Filter crawled facebook reactions.')
    parser.add_argument('filename', metavar='filename', help='a json file [{"id": xxxx, "name": "page_name"}]')
    return parser.parse_args()


def post_is_useful(post):
    return True


def clean_post_data(posts):
    return list(filter(post_is_useful, posts))


def main(run_args):
    filename = run_args.filename
    posts = None
    with open(filename + '.json', 'r') as infile:
        posts = json.load(infile)
    clean_post_data(posts)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

import argparse
import os
import operator
import json
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize the affective text dataset.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f, --file', dest='file', help='a emmood file containing emotions and text')
    group.add_argument('-d, --directory', dest='directory', help='a directory containing emmood files')
    return parser.parse_args()


def get_most_common_reaction(reactions):
    reaction = reactions[0]
    if reaction == 'N':
        reaction = reactions[1]

    if reaction == 'N':
        return None
    elif reaction == 'F':
        return None
    elif reaction == 'A':
        return 'anger'
    elif reaction == 'D':
        return 'anger'
    elif reaction == 'H':
        return 'joy'
    elif reaction == 'Sa':
        return 'sadness'
    elif reaction == 'Su':
        return 'surprise'
    elif reaction == 'Su+':
        return 'surprise'
    elif reaction == 'Su-':
        return 'surprise'
    print('wrong')
    return None


def normalize(textline):
    m = re.search('\d*:\d*\t(.*):(.*)\t.*:.*\t(.*)', textline)
    reactions = [m.group(1), m.group(2)]
    reaction = get_most_common_reaction(reactions)
    return {'message': m.group(3), 'reaction': reaction}


def main(run_args):
    files = []
    if run_args.directory:
        for textfile in os.listdir(run_args.directory):
            if textfile.endswith(".emmood"):
                files.append(os.path.join(run_args.directory, textfile))
    else:
        files = [run_args.file]
    
    textlines = []
    for textfile in files:
        with open(textfile, 'r') as infile:
            for line in infile:
                textlines.append(line)

    normalized_posts = list(map(normalize, textlines))
    filtered_posts = list(filter(lambda post: post['reaction'] != None, normalized_posts))

    with open(textfile + '_normalized.json', 'w') as outfile:
        json.dump(filtered_posts, outfile)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

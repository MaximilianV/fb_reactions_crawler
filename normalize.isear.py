import argparse
import operator
import json
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize the isear dataset.')
    parser.add_argument('csvfile', metavar='textfile', help='a csv file containing text and emotions')
    return parser.parse_args()


def get_most_common_reaction(reaction):
    if reaction == 'anger':
        return 'anger'
    elif reaction == 'disgust':
        return 'anger'
    elif reaction == 'fear':
        return None
    elif reaction == 'joy':
        return 'joy'
    elif reaction == 'sadness':
        return 'sadness'
    elif reaction == 'shame':
        return None
    elif reaction == 'guilt':
        return None
    print('wrong')
    return None


def normalize(textline):
    reaction = get_most_common_reaction(textline[1])
    return {'message': textline[0], 'reaction': reaction}


def main(run_args):
    textlines = []
    with open(run_args.csvfile) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for line in csvreader:
            textlines.append(line)

    normalized_posts = list(map(normalize, textlines))
    filtered_posts = list(filter(lambda post: ']' not in post['message'], normalized_posts))
    
    with open(run_args.csvfile + '_normalized.json', 'w') as outfile:
        json.dump(filtered_posts, outfile)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

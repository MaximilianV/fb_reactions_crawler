import argparse
import operator
import json
import xml.etree.ElementTree as ET


def parse_arguments():
    parser = argparse.ArgumentParser(description='Normalize the affective text dataset.')
    parser.add_argument('xmlfile', metavar='textfile', help='a xml file containing the text')
    parser.add_argument('goldfile', metavar='emotionfile', help='a gold file containing the emotions')
    return parser.parse_args()


def get_most_common_reaction(reactionline):
    reactionline = reactionline.strip('\n')
    reactions = list(map(int, reactionline.split(' ')[1:]))
    highest_reaction = max(reactions)
    highest_reaction_index = reactions.index(highest_reaction)
    if highest_reaction_index == 0:
        return 'anger'
    elif highest_reaction_index == 1:
        return 'anger'
    elif highest_reaction_index == 2:
        return None
    elif highest_reaction_index == 3:
        return 'joy'
    elif highest_reaction_index == 4:
        return 'sadness'
    elif highest_reaction_index == 5:
        return 'surprise'
    return None


def normalize(text, reactionline):
    reaction = get_most_common_reaction(reactionline)
    return {'message': text.text, 'reaction': reaction}


def main(run_args):
    textfile = run_args.xmlfile
    tree = ET.parse(textfile)
    textlines = tree.getroot()

    reactionfile = run_args.goldfile
    reactionlines = []
    with open(reactionfile, 'r') as infile:
        for line in infile:
            reactionlines.append(line)

    normalized_posts = list(map(normalize, textlines, reactionlines))
    filtered_posts = list(filter(lambda post: post['reaction'] != None, normalized_posts))

    textfile = textfile.strip('.xml')
    with open(textfile + '_normalized.json', 'w') as outfile:
        json.dump(filtered_posts, outfile)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

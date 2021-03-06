import argparse
import json
import re
from functools import reduce


eleminations = {
    'nonmessage': 0,
    'noreactions': 0,
    'url': 0,
    'min_char_count': 0,
    'min_reaction_count': 0,
    'top_reaction_gap': 0,
    'no_reactions': 0,
}


def parse_arguments():
    parser = argparse.ArgumentParser(description='Filter crawled facebook reactions.')
    parser.add_argument('-u, --filter-urls', dest='filter_urls', action='store', default=True, type=bool, metavar='filter_urls', help='whether to filter URLs')
    parser.add_argument('-c, --min-char', dest='min_char_count', action='store', default=20, type=int, metavar='min_char', help='a minimal character count')
    parser.add_argument('-r, --min-reactions', dest='min_reaction_count', action='store', default=50, type=int, metavar='min_reactions', help='a minimal reaction count')
    parser.add_argument('-g, --reaction-gap', dest='top_reaction_gap', action='store', default=10, type=int, metavar='reaction_gap', help='a percentage value the dominant reaction has to be above the secondary reaction')
    parser.add_argument('filename', metavar='filename', help='a crawled json file')
    return parser.parse_args()


def post_is_useful(post, filter_urls, min_char_count, min_reaction_count, top_reaction_gap):
    try:
        x = post["message"]
    except KeyError:
        eleminations['nonmessage'] += 1
        return False
    
    try:
        x = post["reactions"]
    except KeyError:
        eleminations['noreactions'] += 1
        return False

    if filter_urls: 
        #Filter based on post content
        # Filter posts including URLs
        url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        if re.match(url_regex, post['message']):
            eleminations['url'] += 1
            return False

    # TODO: Filter posts with less than X characters
    if len(post['message']) < min_char_count:
        eleminations['min_char_count'] += 1
        return False

	# Filter if no reactions (old posts)
    if not 'reactions' in post:
        eleminations['no_reactions'] += 1
        return False
	
    # Filter based on reactions without likes
    post['reactions'].pop('like', None)

    # TODO: Filter posts with less than X reactions 
    if sum(post['reactions'].values()) < min_reaction_count:
        eleminations['min_reaction_count'] += 1
        return False

    # Filter posts where the highest reaction is not dominant. 
    # Default: 10% higher then the secondary reaction.
    # TODO: make percentage a command line argument
    reaction_counts = list(post['reactions'].values())
    highgest_reaction = max(reaction_counts)
    reaction_counts.remove(highgest_reaction)
    second_highgest_reaction = max(reaction_counts)
    if (100 - 100 * second_highgest_reaction / highgest_reaction) < top_reaction_gap:
        eleminations['top_reaction_gap'] += 1
        return False

    return True


def clean_post_data(posts, filter_urls, min_char_count, min_reaction_count, top_reaction_gap):
    eleminations['nonmessage'] = 0
    eleminations['url'] = 0
    eleminations['min_char_count'] = 0
    eleminations['min_reaction_count'] = 0
    eleminations['top_reaction_gap'] = 0
    eleminations['no_reactions'] = 0
    return list(filter(lambda post: post_is_useful(post, filter_urls, min_char_count, min_reaction_count, top_reaction_gap), posts.values()))

	
def filter_data(filename, filter_urls, min_char_count, min_reaction_count, top_reaction_gap):
    posts = None
    with open(filename, 'r') as infile:
        posts = json.load(infile)
    print('Total posts before filter: ' + str(len(posts)))
    clean_posts = clean_post_data(posts, filter_urls, min_char_count, min_reaction_count, top_reaction_gap)
    print('Non-message posts filtered: ' + str(eleminations['nonmessage']))
    print('No reactions posts filtered: ' + str(eleminations['noreactions']))
    print('Posts filtered because of url: ' + str(eleminations['url']))
    print('Posts filtered by minimal character count: ' + str(eleminations['min_char_count']))
    print('Posts filtered by minimal reaction count: ' + str(eleminations['min_reaction_count']))
    print('Posts filtered by top reaction gap: ' + str(eleminations['top_reaction_gap']))
    print('Posts filtered because no reactions found: ' + str(eleminations['no_reactions']))
    print('Total posts after filter: ' + str(len(clean_posts)))
    filename = filename.strip('.json') + '_filtered.json'
    with open(filename, 'w') as outfile:
        json.dump(clean_posts, outfile)
    return filename

		
def main(run_args):
	filter_data(run_args.filename, run_args.filter_urls, run_args.min_char_count, run_args.min_reaction_count, run_args.top_reaction_gap)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)

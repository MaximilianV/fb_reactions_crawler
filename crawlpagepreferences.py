import argparse
import json
from collections import Counter
import matplotlib.pyplot as plt
from pagecrawler.facebookcrawler import FacebookCrawler
import filter
import normalize
import random
import crawl
import os.path
from datetime import datetime

REACTIONS_BITMASK = { 'joy': 1, 'surprise': 2, 'sadness': 4, 'anger': 8 }

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crawl facebook and represent page preferences.')
    parser.add_argument('access_token', metavar='access_token', help='a facebook access token')
    parser.add_argument('-c, --count', dest='count', action='store', default=5, type=int, metavar='page_count', help='amount of page to be fetched')
    parser.add_argument('-l, --limit', dest='limit', action='store', default=200, type=int, metavar='rate_limit', help='limit of API requests per hour')
    parser.add_argument('-e, --erase', dest='erase', action='store', default=False, type=bool, metavar='erase', help='erase existing files')
    parser.add_argument('-f, --file', dest='file', type=open, help='a json file [{"id": xxxx, "name": "page_name"}]')
    parser.add_argument('-sp, --specific', dest='specific', action='store', type=open, help='only crawl specific pages from category list')
    parser.add_argument('-s, --skip', dest='skip', action='count', help='skip steps 0-4')
    parser.add_argument('-v, --value', dest='value', action='store', default=0.5, type=float, metavar='value', help='how many difference between main and other reactions in %')
    parser.add_argument('-nj, --nojoy', dest='nojoy', action='count', help='show or not joy reaction')
    return parser.parse_args()


def crawl_facebook(access_token, count, limit, min_fan_count, specific):
	crawler = FacebookCrawler(access_token, min_fan_count, specific)
	pages = crawler.get_facebook_pages(count, limit)
	output_name = "data/" + "FacebookCrawl" + str( datetime.now().isoformat(timespec='seconds').replace(":","")  )
	if specific:
		output_name += "_specific"
	output_name += ".json"
	with open(output_name, 'w') as outfile:
		json.dump(pages, outfile)
	return output_name

def build_category_vector(cats):
	h = dict()
	i = 0
	for cat in cats:
		if not cat in h:
			h[cat] = i
			i += 1
	return h

def build_reaction_vector(reacts):
	h = dict()
	i = 0
	for react in reacts:
		temp = convert_reaction_to_bitmask(react)
		if not temp in h:
			h[temp] = i
			i += 1

	sorted_h = dict()
	for key in sorted(h):
		sorted_h[key] = h[key]
	return sorted_h

def convert_reaction_to_bitmask(dict):
	temp = 0
	for r, n in dict.items():
		temp |= REACTIONS_BITMASK[r]
	return temp
	
def convert_bitmask_to_react(bitm):
	temp = []
	for BITMASK, BITMASK_VALUE in REACTIONS_BITMASK.items():
		if bitm & BITMASK_VALUE:
			temp.append(BITMASK)
	return '/'.join(temp)
	
def main(run_args):
	
	if not run_args.skip:
		access_token = run_args.access_token
		
		if not run_args.file:
			print("\n# 0. Crawling Facebook...")
			if run_args.specific:
				specific = json.load(run_args.specific)
				print("Specific category to get :")
				print(specific)
				fb_crawlfile = crawl_facebook(access_token, run_args.count, run_args.limit, 10000, specific)
			else:
				fb_crawlfile = crawl_facebook(access_token, run_args.count, run_args.limit, 10000, [])
			pages = json.load(open(fb_crawlfile))
		else:
			pages = json.load(run_args.file)
			
		i = 0
		for page in pages:
			
			output = dict()
			i += 1
			
			print("\n# " + str(i) + ".1 Crawling page '"+page['name']+"'...")
			filename = "data/datasets/" + page['id']
			if not os.path.isfile(filename + ".json") or run_args.erase or os.path.getsize(filename + ".json") < 3:
				crawl.crawl_page(access_token, page['id'], 200, run_args.limit, output_name=page['id'])
			else:
				print("Skipped (-e to not skip)")
			
			print("# " + str(i) + ".2 Filtering content of the page...")
			if not os.path.isfile(filename + "_filtered.json") or run_args.erase or os.path.getsize(filename + "_filtered.json") < 3:
				filter.filter_data(filename + ".json", False, 1, 1, 1)
			else:
				print("Skipped (-e to not skip)")
			
			print("# " + str(i) + ".3 Normalizing content of the page...")
			if not os.path.isfile(filename + "_filtered_normalized.json") or run_args.erase or os.path.getsize(filename + "_filtered_normalized.json") < 3:
				normalize.normalize_data(filename + "_filtered.json")
			else:
				print("Skipped (-e to not skip)")
			
			print("# " + str(i) + ".4 Counting main reactions of the page...")
			if not os.path.isfile(filename + "_filtered_normalized_count.json") or run_args.erase or os.path.getsize(filename + "_filtered_normalized_count.json") < 3:
				posts = None
				with open(filename + "_filtered_normalized.json", 'r') as infile:
					posts = json.load(infile)
					count = Counter()
					for post in posts:
						count.update([post['reaction']])
						
				# Add category & fan_count
				output['id'] = page['id']
				output['name'] = page['name']
				output['category'] = page['category']
				output['fan_count'] = page['fan_count']
				output['reaction'] = count
				
				with open(filename + "_filtered_normalized_count.json", 'w') as outfile:
					json.dump(output, outfile)
			else:
				print("Skipped (-e to not skip)")
	
	cats = []
	reacts = []
	X = []
	Y = []
	for element in os.listdir('data/datasets'):
		if element.endswith('_count.json'):
			page = json.load(open('data/datasets/' + element))
			
			# Build dictionnary with main reactions
			if page['reaction']:
				max_key, max_value = max(page['reaction'].items(), key=lambda x:x[1])
				final_max = { max_key : max_value }
				for k,v in page['reaction'].items():
					if v >= max_value*(1-run_args.value):
						final_max[k] = v
						
				# Print a test
				if page['category'] == "Author":
					print(final_max)
					
				reacts.append(final_max)
				cats.append(page['category'])
			
	if run_args.nojoy:
		i_to_delete = []
		for i in range(0,len(cats)):
			
			if convert_reaction_to_bitmask(reacts[i]) == REACTIONS_BITMASK['joy']:
				i_to_delete.append(i)
			
		i_to_delete.sort(reverse=True)
		for i in i_to_delete:
			cats.pop(i)
			reacts.pop(i)
	
	reactions = build_reaction_vector(reacts)
	categories = build_category_vector(cats)
	print(categories)
	for i in range(0,len(cats)):
		
		# Create esthetical offset
		if convert_reaction_to_bitmask(reacts[i]) == REACTIONS_BITMASK['joy'] or run_args.nojoy:
			offset = random.uniform(-0.1, 0.1)
		else:
			offset = 0
		X.append(categories[cats[i]] + offset)
		
		if convert_reaction_to_bitmask(reacts[i]) == REACTIONS_BITMASK['joy'] or run_args.nojoy:
			offset = random.uniform(-0.1, 0.1)
		else:
			offset = 0
		Y.append(reactions[convert_reaction_to_bitmask(reacts[i])] + offset)
		
	plt.figure()
	plt.plot(X,Y,'+')
	plt.title('Reactions by categories\nPages with min.10000 fans')
	plt.figtext(0.9,0.9, str(len(categories)) + 'categories\n' + str(len(reacts)) + 'datas', fontsize=9, ha='right')
	bitmasks = []
	for bitmask in list(reactions.keys()):
		 bitmasks.append(convert_bitmask_to_react(bitmask))
	plt.yticks(range(len(list(reactions.keys()))), bitmasks, rotation=0)
	plt.xticks(range(len(list(categories.keys()))), list(categories.keys()), rotation=80)
	plt.show()
		
			

if __name__ == "__main__":
    args = parse_arguments()
    main(args)

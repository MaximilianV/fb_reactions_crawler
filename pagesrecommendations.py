import argparse
import json
from collections import Counter
import matplotlib.pyplot as plt
from operator import itemgetter
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
    parser.add_argument('-v, --value', dest='value', action='store', default=0.5, type=float, metavar='value', help='how many difference between main and other reactions in %')
    parser.add_argument('-r, --reaction', dest='reaction', action='store', help='main reaction')
    parser.add_argument('-m, --min_value', dest='min_value', action='store', default=0, type=int, help='min number of posts with the reaction')
    parser.add_argument('-s, --skipreaction', dest='skipreaction', action='store', help='remove results with this reaction')
    return parser.parse_args()


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
	
	if run_args.reaction in REACTIONS_BITMASK:
		
		cats = []
		names = []
		ids = []
		reacts = []
		result = []
		result2 = dict()
		X = []
		Y = []
		for element in os.listdir('data/datasets'):
			if element.endswith('_count.json'):
				page = json.load(open('data/datasets/' + element))
				
				# Build dictionnary with main reactions
				if page['reaction']:
					max_key, max_value = max(page['reaction'].items(), key=lambda x:x[1])
					final_max = { max_key : max_value }
					if max_value >= run_args.min_value:
						for k,v in page['reaction'].items():
							if v >= max_value*(1-run_args.value):
								final_max[k] = v
						
						insert = False
						for i in final_max:
							if i == run_args.skipreaction:
								insert = False
								break
							elif i == run_args.reaction:
								insert = True
							
						
						if insert:
							result.append({'id':page['id'],'name':page['name'],'reactions':final_max[run_args.reaction]})
							if page['category'] in result2:
								result2[page['category']] += final_max[run_args.reaction]
							else:
								result2[page['category']] = final_max[run_args.reaction]
							reacts.append(final_max)
							cats.append(page['category'])		
							ids.append(page['id'])		
							names.append(page['name'])		
					
		categories_sorted = sorted(cats, key=Counter(cats).get, reverse=True)		
		result2_sorted = sorted(result2, key=result2.get, reverse=True)		
		result_sorted = sorted(result, key=itemgetter('reactions'), reverse=True)
		
		filename = 'data/results/PageRecom-most_'+ run_args.reaction
		if run_args.skipreaction:
			filename += '-no_' + run_args.skipreaction
		if run_args.min_value:
			filename += '-min_' + str(run_args.min_value) + 'reactions'
		filename += '_Ordered.json'
		with open(filename, 'w') as outfile:
			json.dump(result_sorted, outfile)
			
		filename = 'data/results/CategoryRecom-most_'+ run_args.reaction
		if run_args.skipreaction:
			filename += '-no_' + run_args.skipreaction
		if run_args.min_value:
			filename += '-min_' + str(run_args.min_value) + 'reactions'
		filename += '_Ordered.json'
		with open(filename, 'w') as outfile:
			json.dump(result2_sorted, outfile)
				
		#print(reacts)
		#print(names)
		#print(ids)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)

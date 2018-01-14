import argparse
import json
from pagecrawler.facebookcrawler import FacebookCrawler
import crawl
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crawl facebook and represent page preferences.')
    parser.add_argument('access_token', metavar='access_token', help='a facebook access token')
    parser.add_argument('-c, --count', dest='count', action='store', default=5, type=int, metavar='page_count', help='amount of page to be fetched')
    parser.add_argument('-l, --limit', dest='limit', action='store', default=200, type=int, metavar='rate_limit', help='limit of API requests per hour')
    return parser.parse_args()


def crawl_facebook(access_token, count, limit):
	crawler = FacebookCrawler(access_token)
	pages = crawler.get_facebook_pages(count, limit)
	output_name = "data/" + "FacebookCrawl" + str( datetime.now().isoformat(timespec='seconds').replace(":","")  ) + ".json"
	with open(output_name, 'w') as outfile:
		json.dump(pages, outfile)
	return output_name

def main(run_args):
	access_token = run_args.access_token
	fb_crawlfile = crawl_facebook(access_token, run_args.count, run_args.limit)

	pages_config = json.load(open(fb_crawlfile))
	for page in pages_config:
		crawl.crawl_page(access_token, page['id'], 100, run_args.limit, output_name=page['name'])


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

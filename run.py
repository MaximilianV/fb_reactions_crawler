import argparse
import json
from pagecrawler import PageCrawler


def parse_arguments():
    parser = argparse.ArgumentParser(description='Crawl facebook reactions from pages.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('access_token', metavar='access_token', help='a facebook access token')
    parser.add_argument('-c, --count', dest='count', action='store', default=5, type=int, metavar='post_count', help='amount of posts to be fetched from each page')
    group.add_argument('-f, --file', dest='file', type=open, help='a file with newline separated page ids')
    group.add_argument('-i, --id', dest='page_id', help='a facebook page id')
    return parser.parse_args()


def crawl_page(access_token, page_id, count, output_name=None):
    crawler = PageCrawler(access_token, page_id)
    reactions = crawler.get_latest_posts_with_reactions(count)
    with open(output_name + '.json', 'w') as outfile:
        json.dump(reactions, outfile)


def main(run_args):
    access_token = run_args.access_token
    if run_args.file:
        pages_config = json.load(run_args.file)
        for page in pages_config:
            crawl_page(access_token, page['id'], run_args.count, output_name=page['name'])
    else:
        crawl_page(access_token, run_args.page_id, run_args.count)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)


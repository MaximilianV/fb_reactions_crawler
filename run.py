import argparse
import json
from pagecrawler import PageCrawler
from facebook import Facebook


def parse_arguments():
    parser = argparse.ArgumentParser(description='Crawl facebook reactions from pages.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('access_token', metavar='access_token', help='a facebook access token')
    parser.add_argument('-c, --count', dest='count', action='store', default=5, type=int, metavar='post_count', help='amount of posts to be fetched from each page')
    parser.add_argument('-l, --limit', dest='limit', action='store', default=200, type=int, metavar='rate_limit', help='limit of API requests per hour')
    group.add_argument('-f, --file', dest='file', type=open, help='a json file [{"id": xxxx, "name": "page_name"}]')
    group.add_argument('-i, --id', dest='page_id', help='a facebook page id')
    return parser.parse_args()


def crawl_page(access_token, page_id, count, limit, output_name=None):
    if not output_name:
        output_name = str(page_id)
    crawler = PageCrawler(access_token, page_id)
    reactions = crawler.get_latest_posts_with_reactions(count, limit)
    with open(output_name + '.json', 'w') as outfile:
        json.dump(reactions, outfile)


def main(run_args):
    access_token = run_args.access_token
    """if run_args.file:
        pages_config = json.load(run_args.file)
        for page in pages_config:
            crawl_page(access_token, page['id'], run_args.count, run_args.limit, output_name=page['name'])
    else:
        crawl_page(access_token, run_args.page_id, run_args.count, run_args.limit)"""
    fb = Facebook(access_token)
    fb.get_posts(289955244416, 55)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)


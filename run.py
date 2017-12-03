import facebook
import sys
from pagecrawler import PageCrawler

if len(sys.argv) != 3:
    print("Usage: [access_token] [page_id]")
    exit()

crawler = PageCrawler(sys.argv[1], sys.argv[2])

print(crawler.get_latest_posts())

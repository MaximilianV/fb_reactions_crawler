from pagecrawler.facebook import Facebook
import time


class FacebookCrawler:
    def __init__(self, access_token, min_fan_count=1000, specific=[]):
        self.fb_graph = Facebook(access_token=access_token, min_fan_count=min_fan_count, specific=specific)

    def get_facebook_pages(self, count=10, rate_limit_per_hour=200):
        pages = self.fb_graph.get_pages(count)
        return pages

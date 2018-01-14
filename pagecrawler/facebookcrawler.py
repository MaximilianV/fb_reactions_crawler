from pagecrawler.facebook import Facebook
import time


class FacebookCrawler:
    def __init__(self, access_token):
        self.fb_graph = Facebook(access_token=access_token)

    def get_facebook_pages(self, count=10, rate_limit_per_hour=200):
        pages = self.fb_graph.get_pages(count)
        return pages

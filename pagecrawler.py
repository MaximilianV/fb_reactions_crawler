import facebook


class PageCrawler:
    def __init__(self, access_token, page_id):
        self.page_id = page_id
        self.fb_graph = facebook.GraphAPI(access_token=access_token)

    def get_latest_posts(self, count=10):
        return self.fb_graph.get_object(id=self.page_id, fields='posts.limit(10)')
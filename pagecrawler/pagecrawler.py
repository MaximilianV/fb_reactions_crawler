from pagecrawler.facebook import Facebook
import time


class PageCrawler:
    def __init__(self, access_token, page_id):
        self.page_id = str(page_id)
        self.fb_graph = Facebook(access_token=access_token)

    def get_latest_posts_with_reactions(self, count=10, rate_limit_per_hour=200):
        posts = self.fb_graph.get_posts(self.page_id, count)
        post_dict = Facebook.transform_post_list_to_post_dict(posts)
        post_ids = list(post_dict.keys())
        reaction_dict = self.fb_graph.get_reactions_for_posts(post_ids)
        for reaction in reaction_dict:
            post_dict[reaction]["reactions"] = reaction_dict[reaction]
        return post_dict

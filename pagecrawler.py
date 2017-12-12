import facebook
import time


class PageCrawler:
    def __init__(self, access_token, page_id):
        self.page_id = str(page_id)
        self.fb_graph = facebook.GraphAPI(access_token=access_token, version="2.7")

    def get_latest_posts(self, count=10):
        return self.fb_graph.get_object(id=self.page_id, fields='posts.limit(' + str(count) + '){id, message}')

    def get_reaction_for_post(self, post_id):
        reactions = self.fb_graph.get_object(id=post_id, fields='reactions.type(LIKE).limit(0).summary(1).as(like),'
                                                                'reactions.type(LOVE).limit(0).summary(1).as(love),'
                                                                'reactions.type(HAHA).limit(0).summary(1).as(haha),'
                                                                'reactions.type(WOW).limit(0).summary(1).as(wow),'
                                                                'reactions.type(SAD).limit(0).summary(1).as(sad),'
                                                                'reactions.type(ANGRY).limit(0).summary(1).as(angry)')
        return PageCrawler.shorten_reactions_array(reactions)

    def get_latest_posts_with_reactions(self, count=10, rate_limit_per_hour=200):
        posts = self.get_latest_posts(count)
        chunked_posts = list(PageCrawler.chunks(posts["posts"]["data"], rate_limit_per_hour))
        enriched_posts = {}
        for chunk in chunked_posts:
            for post in chunk:
                enriched_posts[post["id"]] = {"message": post["message"],
                                          "reactions": self.get_reaction_for_post(post["id"])}
            # After crawling a chunk, wait until the next full hour
            time.sleep(-time.time() % 3600)
        return enriched_posts

    @staticmethod
    def shorten_reactions_array(reactions):
        compact_reactions = dict()
        reactions.pop("id", None)
        for reaction in reactions:
            compact_reactions[reaction] = reactions[reaction]["summary"]["total_count"]
        return compact_reactions

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
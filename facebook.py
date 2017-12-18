import requests
from facebookresponse import FacebookResponse


class Facebook:
    BASE_URL = "https://graph.facebook.com/v2.11"
    SINGLE_ID = "/{id}"
    MULTIPLE_IDS = "/?ids={ids}"

    GET_TOKEN_NAME = "access_token"
    GET_LIMIT_NAME = "limit"

    GET_LIMIT_MAX = 10

    def __init__(self, access_token):
        self.access_token = access_token
        self.session = requests.Session()
        self.default_args = {Facebook.GET_TOKEN_NAME: self.access_token}

    def place_request(self, url, limit):
        args = {Facebook.GET_LIMIT_NAME: str(limit)}
        args.update(self.default_args)
        # print(args)
        # print("Requesting: " + url + " with limit " + str(limit) + "\n")

        r = self.session.get(url, params=args)
        r.raise_for_status()
        return FacebookResponse(r.json())


    def get_posts(self, page_id, count):
        retrieved_posts = 0
        url = Facebook.get_singleid_url(page_id) + "/posts"
        limit = min(count, Facebook.GET_LIMIT_MAX)
        result = self.place_request(url, limit)
        retrieved_posts = result.count()

        print("Received " + str(retrieved_posts) + " objects.\n")

        while retrieved_posts < count:
            remaining_posts = count - retrieved_posts
            limit = min(remaining_posts, Facebook.GET_LIMIT_MAX)
            print("Collected " + str(retrieved_posts) + " posts from " + str(count) + "\n")
            print(str(remaining_posts) + " remaining. Preparing new request for " + str(limit) + " posts.\n")
            result = self.place_request(result.get_url_for_next_page(), limit)
            retrieved_posts += result.count()

        print("Finished get_posts")

    def get_reactions_for_post(self, post_id):
        pass

    def get_reactions_for_posts(self, post_ids):
        pass

    @staticmethod
    def get_singleid_url(object_id):
        return Facebook.BASE_URL + Facebook.SINGLE_ID.format(id=object_id)
    @staticmethod
    def get_multipleids_url(object_ids):
        list_of_ids = ','.join(map(str, object_ids))
        return Facebook.BASE_URL + Facebook.MULTIPLE_IDS.format(ids=list_of_ids)
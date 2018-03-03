import requests
from pagecrawler.facebookresponse import FacebookResponse
import time
import random


class Facebook:
    BASE_URL = "https://graph.facebook.com/v2.11"
    SINGLE_ID = "/{id}"
    MULTIPLE_IDS = "/?ids={ids}"

    GET_TOKEN_NAME = "access_token"
    GET_LIMIT_NAME = "limit"
    GET_FIELDS_NAME = "fields"

    GET_REACTION_FIELDS = 'reactions.type(LIKE).limit(0).summary(1).as(like),' \
                          + 'reactions.type(LOVE).limit(0).summary(1).as(love),'\
                          + 'reactions.type(HAHA).limit(0).summary(1).as(haha),'\
                          + 'reactions.type(WOW).limit(0).summary(1).as(wow),'\
                          + 'reactions.type(SAD).limit(0).summary(1).as(sad),'\
                          + 'reactions.type(ANGRY).limit(0).summary(1).as(angry)'

    GET_LIMIT_MAX = 100
    GET_LIMIT_PAGE_MAX = 1000

    def __init__(self, access_token, min_fan_count=10000, specific=[]):
        self.access_token = access_token
        self.session = requests.Session()
        self.default_args = {Facebook.GET_TOKEN_NAME: self.access_token}
        self.min_fan_count = min_fan_count
        self.retrieved_pages = 0
        self.specific = specific
		
		
    def place_request(self, url, limit, additional_fields=None):
        # Set limit for request
        args = {Facebook.GET_LIMIT_NAME: str(limit)}

        # If request fields are supplied, set them as parameter
        if additional_fields:
            args.update({Facebook.GET_FIELDS_NAME: additional_fields})

        # Merge default parameters
        args.update(self.default_args)

        # print(args)
        # print("Requesting: " + url + " with limit " + str(limit) + "\n")
        #time.sleep(random.randint(1,5))
        r = self.session.get(url, params=args)
        # Throw exception in case of error
        # r.raise_for_status()

        # Return FacebookResponse object
        return FacebookResponse(r.json())

	# Recursiv crawling
    def get_pages_r(self, page_id, count, depth, pages_data_to_test):
        pages_data = []
		
        if self.retrieved_pages < count and depth < 20:

            remaining_pages = count - self.retrieved_pages
            limit = min(remaining_pages, Facebook.GET_LIMIT_PAGE_MAX)
            # Print text
            print("= Collected " + str(self.retrieved_pages) + " / " + str(count) + "pages.")
            print("= " + str(remaining_pages) + " remaining. Preparing new request for " + str(limit) + " pages.")
			
            url = Facebook.get_singleid_url(page_id) + "/likes?fields=id,name,category,fan_count"
            result = self.place_request(url, limit)
            pages_data = result.data
            if pages_data:
                self.retrieved_pages += result.count()
                if result.count()>0:
                      for page in pages_data:
                          if page['fan_count'] < self.min_fan_count or ( len(self.specific) > 0 and not page['category'] in self.specific ):
                             pages_data.pop(pages_data.index(page))
                             self.retrieved_pages -= 1
                      if pages_data:
                          # Delete duplicates		
                          i_to_delete = []			
                          for i in range(0,len(pages_data)):
                             if pages_data[i] in pages_data_to_test:
                                 i_to_delete.append(i)
                                 self.duplicates += 1
                          i_to_delete.sort(reverse=True)
                          for i in i_to_delete:
                             pages_data.pop(i)
						  # Continue recursivity
                          for page in pages_data:
                             temp = self.get_pages_r(page['id'], count, depth + 1, pages_data_to_test)
                             if temp:
                                 pages_data.extend(temp)

        return pages_data
	
    def get_pages(self, count):
        self.retrieved_pages = 0
        self.duplicates = 0
        pages_data = []
        url = Facebook.get_base_url() + "/search?q=''&type=page&fields=id,name,category,fan_count"
        limit = min(count, Facebook.GET_LIMIT_PAGE_MAX)
        result = self.place_request(url, limit)
        pages_data = result.data
        self.retrieved_pages = result.count()
        for page in pages_data:
            if page['fan_count'] < self.min_fan_count or ( not self.specific or not page['category'] in self.specific ):
                pages_data.pop(pages_data.index(page))
                self.retrieved_pages -= 1

        temp = []
        for page in pages_data:
            temp.extend(self.get_pages_r(page['id'], count, 0,  pages_data))
            before = len(temp)
            s = []
            for i in temp:
                if i not in s:
                    s.append(i)
            temp = s
            self.duplicates += before - len(temp)
            if self.retrieved_pages >= count:
                break

        print("* Finished get_pages from Facebook, "+ str(self.duplicates) +" duplicates erased.*")
        pages_data.extend(temp)
        return pages_data
	
    def get_posts(self, page_id, count):
        retrieved_posts = 0
        posts_data = []
        url = Facebook.get_singleid_url(page_id) + "/posts"
        limit = min(count, Facebook.GET_LIMIT_MAX)
        result = self.place_request(url, limit)
        posts_data = result.data
        if not posts_data:
            return []
        retrieved_posts = result.count()

        while retrieved_posts < count:
            remaining_posts = count - retrieved_posts
            limit = min(remaining_posts, Facebook.GET_LIMIT_MAX)
            print("= Collected " + str(retrieved_posts) + " posts from " + str(count))
            print("= " + str(remaining_posts) + " remaining. Preparing new request for " + str(limit) + " posts.")
            url = result.get_url_for_next_page()
            if url:
                result = self.place_request(url, limit)
                posts_data += result.data
                retrieved_posts += result.count()
            else:
                break

        print("Finished get_posts from " + str(page_id))
        return posts_data

    def get_reactions_for_posts(self, post_ids):
        retrieved = 0
        count = len(post_ids)
        reaction_data = {}
        chunked_post_ids = list(Facebook.chunks(post_ids, 25))
        for id_chunk in chunked_post_ids:
            url = Facebook.get_multipleids_url(id_chunk)
            result = self.place_request(url, len(id_chunk), Facebook.GET_REACTION_FIELDS)
            reaction_data.update(result.data)
        return reaction_data

    # STATIC METHODS #
    @staticmethod
    def get_base_url():
        return Facebook.BASE_URL

    @staticmethod
    def get_singleid_url(object_id):
        return Facebook.get_base_url() + Facebook.SINGLE_ID.format(id=object_id)

    @staticmethod
    def get_multipleids_url(object_ids):
        list_of_ids = ','.join(map(str, object_ids))
        return Facebook.get_base_url() + Facebook.MULTIPLE_IDS.format(ids=list_of_ids)

    @staticmethod
    def chunks(long_list, chunk_size):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(long_list), chunk_size):
            yield long_list[i:i + chunk_size]
		
    @staticmethod
    def transform_post_list_to_post_dict(posts):
        post_dict = {}
        for post in posts:
            post_dict[post["id"]] = post
        return post_dict

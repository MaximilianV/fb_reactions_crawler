class FacebookResponse:
    def __init__(self, response):
        self.complete_response = response
        self.data = self.extract_content()
        self.next = FacebookResponse.extract_next_page(response)

    def extract_content(self):
        data = FacebookResponse.extract_key_value(self.complete_response, "data")

        # If it is a simple "data" array, return this
        if data:
            return data

        # Check if its a reaction response
        first_key = list(self.complete_response.keys())[0]
        if "like" in self.complete_response[first_key]:
            return self.extract_reaction_content()

        raise Exception("Couldn't identify response content.")

    def extract_reaction_content(self):
        reaction_response = {}
        for post in self.complete_response:
            reaction_response[post] = FacebookResponse.shorten_reactions_array(self.complete_response[post])
        return reaction_response

    def count(self):
        return len(self.data)

    def get_url_for_next_page(self):
        return self.next

    @staticmethod
    def extract_next_page(response):
        paging = FacebookResponse.extract_paging(response)
        return FacebookResponse.extract_key_value(paging, "next")

    @staticmethod
    def extract_previous_page(response):
        paging = FacebookResponse.extract_paging(response)
        return FacebookResponse.extract_key_value(paging, "previous")

    @staticmethod
    def extract_paging(response):
        return FacebookResponse.extract_key_value(response, "paging", {})

    @staticmethod
    def extract_key_value(dictionary, key, default=None):
        if key in dictionary:
            return dictionary[key]
        else:
            return default

    @staticmethod
    def shorten_reactions_array(reactions):
        compact_reactions = dict()
        reactions.pop("id", None)
        for reaction in reactions:
            compact_reactions[reaction] = reactions[reaction]["summary"]["total_count"]
        return compact_reactions

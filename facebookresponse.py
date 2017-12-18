class FacebookResponse:
    def __init__(self, response):
        self.data = FacebookResponse.extract_content(response)
        self.next = FacebookResponse.extract_next_page(response)

    def count(self):
        return len(self.data)

    def get_url_for_next_page(self):
        return self.next

    @staticmethod
    def extract_content(response):
        return FacebookResponse.extract_key_value(response, "data", {})

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

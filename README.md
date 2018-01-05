# Facebook Reactions Crawler
*A crawler for facebook posts and their reactions on public facebook pages.*

### 0. Installation
#### a. Prerequisites
Virtualenv can be used to simply the process.

    python3

#### b. Setup

    1. Clone the repository
    1. Run `python3 stup.py`

### 1. Facebook Reactions Crawler - Usage
The usage of the main script `run.py` is as follows:

    usage: run.py [-h] [-c, --count post_count]
                  (-f, --file FILE | -i, --id PAGE_ID)
                  access_token

    Crawl facebook reactions from pages.

    positional arguments:
      access_token          a facebook access token

    optional arguments:
      -h, --help            show this help message and exit
      -c, --count post_count
                            amount of posts to be fetched from each page
      -f, --file FILE       a json file [{"id": xxxx, "name": "page_name"}]
      -i, --id PAGE_ID      a facebook page id

You have to provide your *Facebook access token*, as well as either a *page id* or a file, containing ids.

If you choose to provide a file, e.g. for crawling multiple pages at once, use the following schema:
```json
[{
    "id": 12345678,
    "name": "a facebook page"
},{
    "id": 87654321,
    "name": "another facebook page"
}]
```

The output is written to a file for each provided page individually.

### 2. Post Entropy Filter - Usage

The usage of the main script `postfilter.py` is as follows:
```
    usage: postfilter.py [-h] [-u, --filter-urls filter_urls]
                         [-c, --min-char min_char_count]
                         [-r, --min-reactions min_reaction_count]
                         [-g, --reaction-gap top_reaction_min_gap]
                         filename

    Filter crawled facebook reactions.

    positional arguments:
      filename              a crawled json file

    optional arguments:
      -h, --help            show this help message and exit
      -u, --filter-urls filter_urls
                            Filter posts if they are URLs.
      -c, --min-char min_char_count
                            Filter posts by minimal character count.
      -r, --min-reactions min_reaction_count
                            Filter posts by minimal reaction count.
      -g, --reaction-gap top_reaction_min_gap
                            Filter posts where the dominant isnt X percent higher
                            then the secondary reaction.
```

### 3. FAQ

*How do I get a Facebook access token?*
> Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) and request an access token with your Facebook user on the top right corner.

*How do I get a page id?*
> Go to [Facebook](https://facebook.com) and navigate to the desired page. Now open the source code (e.g. `ctrl + u`) and search for `"uid":`.
> You just found your page id!

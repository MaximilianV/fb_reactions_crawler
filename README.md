# fb_reactions_crawler
*A crawler for facebook posts and their reactions on public facebook pages.*

### 0. Installation
#### a. Prerequisites
Virtualenv can be used to simply the process.

    python3
    facebook-sdk (requires requests)

The documentation for `facebook-sdk` can be found [here](http://facebook-sdk.readthedocs.io/en/latest/index.html).

#### b. Installing
Clone this repository.

### 1. Usage
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

### 2. FAQ

*How do I get a Facebook access token?*
> Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) and request an access token with your Facebook user on the top right corner.

*How do I get a page id?*
> Go to [Facebook](https://facebook.com) and navigate to the desired page. Now open the source code (e.g. `ctrl + u`) and search for `"uid":`.
> You just found your page id!

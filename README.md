# Reaction Prediction
*This project aims to predict the most frequently used facebook reaction for a given text.*

## 0. Installation
### a. Prerequisites
Virtualenv can be used to simply the process.

1. python3

### b. Setup

1. Clone the repository
1. Run `python3 stup.py`

## 1. Example Usage

Imagine you want to train your Model with facebook posts from CNN. This is the standard procedure you would do:
1. Find the id of the page you want to crawl. The fastest way to retrieve a page id is https://findmyfbid.com/. (e.G. For CNN it is 5550296508.)
1. Get yourself a facebook graph API access token using the graph API explorer https://developers.facebook.com/tools/explorer/.
1. Use the crawling script.
```
python3 crawl.py -i 5550296508 YOUR_FB_ACCESS_TOKEN
```

1. Filter the crawled data using the filter script.
```
python3 filter.py cnn.json
```

1. Normalize the filtered data using the normalize script.
```
python3 normalize.py cnn_filtered.json
```

1. Train the model using the train script.
```
python3 train.py cnn_filtered_normalized.json
```

1. Question the trained model using the requestmodel script.
```
python3 requestmodel.py "Your newest FB post!"
```

## 2. Documentation

### a. Crawling Data

The usage of the script `crawl.py` is as follows:
```
usage: crawl.py [-h] [-c, --count post_count] [-l, --limit rate_limit]
                (-f, --file FILE | -i, --id PAGE_ID)
                access_token

Crawl facebook reactions from pages.

positional arguments:
access_token              a facebook access token

optional arguments:
-h, --help                show this help message and exit
-c, --count post_count    amount of posts to be fetched from each page
-l, --limit rate_limit    limit of API requests per hour
-f, --file FILE           a json file [{"id": xxxx, "name": "page_name"}]
-i, --id PAGE_ID          a facebook page id
```

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

### b. Filtering Data

The usage of the script `filter.py` is as follows:
```
usage: filter.py [-h] [-u, --filter-urls filter_urls]
                [-c, --min-char min_char] [-r, --min-reactions min_reactions]
                [-g, --reaction-gap reaction_gap]
                filename

Filter crawled facebook reactions.

positional arguments:
filename                             a crawled json file

optional arguments:
-h, --help                           show this help message and exit
-u, --filter-urls filter_urls        whether to filter URLs
-c, --min-char min_char              a minimal character count
-r, --min-reactions min_reactions    a minimal reaction count
-g, --reaction-gap reaction_gap      a percentage value the dominant reaction has 
                                        to be above the secondary reaction
```

### c. Normalizing Data

The usage of the script `normalize.py` is as follows:
```
usage: normalize.py [-h] filename

Normalize crawled and filtered facebook reactions.

positional arguments:
filename      a filtered json file

optional arguments:
-h, --help    show this help message and exit
```

### d. Training a Model

The usage of the script `train.py` is as follows:
```
usage: train.py [-h] filename

Train model based on normalized facebook reactions.

positional arguments:
filename      a normalized json file

optional arguments:
-h, --help    show this help message and exit
```

### d. Question the Model

The usage of the script `requestmodel.py` is as follows:
```
usage: requestmodel.py [-h]

Load a trained model and place requests.

optional arguments:
-h, --help    show this help message and exit
```

## 3. FAQ

*How do I get a Facebook access token?*
> Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) and request an access token with your Facebook user on the top right corner.

*How do I get a page id?*
> Go to [Facebook](https://facebook.com) and navigate to the desired page. Now open the source code (e.g. `ctrl + u`) and search for `"uid":`.
> You just found your page id!

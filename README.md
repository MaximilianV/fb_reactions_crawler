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
Execute `run.py`, which accepts and also requires two arguments: a Facebook access token and a page id.

*How do I get a Facebook access token?*
> Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) and request an access token with your Facebook user on the top right corner.

*How do I get a page id?*
> Go to [Facebook](https://facebook.com) and navigate to the desired page. Now open the source code (e.g. `ctrl + u`) and search for `"uid":`.
> You just found your page id!

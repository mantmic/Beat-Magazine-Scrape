# Beat-Magazine-Scrape

## Overview ##
Beat Magazine has a great gig guide, serving as a repository of local gigs in Melbourne. The user experience of finding a gig on their website however leaves alot to be desired.

http://www.beat.com.au/gig-guide

The objective of these functions is to;
1. Scrape the gig guide to find events in Melbourne
2. Associate webpages containing artist music with Beat's artist pages

The end goal is to improve the user experience of finding a gig by;
1. Giving the user more search options (geospatial, price, etc)
2. Allowing a user to listen to an artist on the same screen as where they are searching for a gig

These python functions pull the data required to achieve this.

## Dependencies ## 

Python packages
* urllib 
* bs4 
* re (usually installed by default)
* fuzzywuzzy 
* dateutil 
* importlib (for importing functions from each file)

```bash
pip3 install urllib bs4 fuzzywuzzy dateutil importlib
```

# Beat Magazine Scrape

## Overview ##
Beat Magazine has a great gig guide, serving as a repository of local gigs in Melbourne. The user experience of finding a gig on their website however leaves alot to be desired.

http://www.beat.com.au/gig-guide


The end goal is to improve the user experience of finding a gig by;
1. Giving the user more search options (geospatial, price, etc)
2. Allowing a user to listen to an artist on the same screen as where they are searching for a gig

### Scrape ###
The objective of these functions is to;
1. Scrape the gig guide to find events in Melbourne
2. Associate webpages containing artist music with Beat's artist pages

These python functions pull the data required to achieve this.

#### Dependencies ####
* Python 3

* Python 3 libraries
  * urllib
  * bs4
  * re (usually installed by default)
  * fuzzywuzzy
  * dateutil
  * importlib (for importing functions from each file)
  * geopy

```bash
pip3 install urllib bs4 fuzzywuzzy dateutil importlib geopy
```

### DB ###
Simple storage for gig data.

Due to Heroku's 10,000 record limit the schema is a little strange. Gigs are stored as one record per day with a large JSON array containing all the gigs that day. The table can be accessed like a normal relational table using the view, beat.gig_vw.

#### Dependencies ####
* Postgres 9.5 +


### API ###
NodeJS API used for acccessing Postgres database. Operations that post data require an API key. Read operations are open to all.

#### Dependencies ####


### Frontend ###


#### Dependencies ####

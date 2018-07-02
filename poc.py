from urllib import request, parse
from bs4 import BeautifulSoup, Comment
import re

beat_url = "http://www.beat.com.au/"

gig_guide = "gig-guide/2018-07-01"

page = request.urlopen(beat_url + gig_guide)
soup = BeautifulSoup(page)

soup.prettify()

soup.title

#get the gigs

#you have to go by genre (uuuugh)
gigs=soup.find_all('div',{"class":"w-clearfix archive_node-summary-wrapper indie-rock-pop-metal-punk-covers"})

#loop through gigs
gig = gigs[9]

#link to the gig (to scrape more information)
gig_link = gig.find("a").get("href")

#try to get the location link
summaries = gig.find_all('h5',{"class":"gigguide_node-summary-detail"})
for i in range(len(summaries)):
    location_link=summaries[i].find("a")
    if(location_link != None):
        break

location_link = location_link.get("href")

#scrape location information 
page = request.urlopen(beat_url + location_link)
soup = BeautifulSoup(page)

soup.prettify()

location_detail=soup.find('div',{"class":"w-clearfix gigguide_gigdetail-details"})

location_name = None
location_address = None 
location_link = None

#get name 
location_name = soup.find('h1',{"class":"article_title"}).text

field_labels = location_detail.find_all('h5',{"class":"gigguide_gigdetail-field-label"})

for i in range(len(field_labels)):
	if 'address' in field_labels[i].text.lower():
		location_address = field_labels[i].findNext('h5').text
		if location_address != None:
			next
	
	if field_labels[i].find('a') != None:
		location_link = field_labels[i].find('a').get('href')
		next



#get gig info
page = request.urlopen(beat_url + gig_link)
soup = BeautifulSoup(page)
gig_info = soup.find('div',{"class":"w-clearfix gigguide_gigdetail-details"})

gig_details = gig_info.find_all('h5',{"class":"gigguide_node-summary-detail"})

gd_output = []
#determine what each thing is
for i in range(len(gig_details)): 
    gig_detail = gig_details[i]
    #initiate variable
    detail_type = None
    detail_value = None
    #classify detail
    gig_link = gig_detail.find("a")
    gig_span = gig_detail.find("span")
    
    if gig_link is None:
        #not a venue or artist
        #check if there is a date
        if gig_span is None:
            if "$" in gig_detail.text:
                detail_type = "gig-price"
                detail_value = gig_detail.text
        else:
            #this the date 
            detail_type = "gig-datetime"
            detail_value = gig_span.text
    else:
        href = gig_link.get("href")
        if "artist/" in href:
            detail_type = "artist-headline"
            detail_value = href
        elif "support" in href:
            detail_type = "artist-support"
            detail_value = href
        elif "venue" in href:
            detail_type = "venue"
            detail_value = href
    
    print(detail_type)
    print(detail_value)
    gd_output.append({"detail_type":detail_type,"detail_value":detail_value})

	
headline_artist_link = [x for x in gd_output if x.get('detail_type') == 'artist-headline'][0].get('detail_value')
#scrape headlinining artists 
page = request.urlopen(beat_url + headline_artist_link)
soup = BeautifulSoup(page)
 
artist_name = soup.find('h2', {"class":"node-title"}).text 


#scrape supporting artists 

#now we have a normalized artist scrape 

#find a bandcamp link 
from fuzzywuzzy import fuzz, process
#perform a query for the artist name on bandcamp 
min_match = 90
bandcamp_url = "https://bandcamp.com"

band_name = "ferla"

page = request.urlopen(bandcamp_url + "/search?q=" + parse.quote(band_name))
soup = BeautifulSoup(page)
#get the search response
results = soup.find_all('div', {"class":"result-info"})
#filter so we only get arist responses 
results = [x for x in results if "artist" in x.find("div",{"class":"itemtype"}).text.lower()]

artist_results = []

for i in range(len(results)):
	this_name = results[i].find('div', {"class":"heading"}).text.strip() 
	this_link = results[i].find('div', {"class":"itemurl"}).text.strip() 
	artist_results.append({"name":this_name, "link":this_link})

#get best match 
best_match = process.extractOne(band_name,map(lambda x: x.get("name"),artist_results))

if best_match[1] > min_match:
	artist_match = [x for x in artist_results if best_match[0] == x.get("name")][0]
	artist_url = artist_match.get("link")

#we got a result, now let's try get a track 
page = request.urlopen(artist_url)
soup = BeautifulSoup(page)

#check if there is a music link on the home page 
song_url = None
soup.find('div', {"class":"track-info"})

#otherwise find a link to album or ep
albums = soup.find_all('li', {"class":"music-grid-item square first-four "})
album_links = list(map(lambda x: x.find("a").get("href"),albums))

bandcamp_track_id = None
bandcamp_track_type = None

bandcamp_links = []

#loop through all the albums
for i in range(len(album_links)):
	album_link = artist_url + album_links[i]
	this_page = request.urlopen(album_link)
	s = BeautifulSoup(this_page)
	page_comments = s.findAll(text=lambda text:isinstance(text, Comment))
	for comments in page_comments:
		this_comment = comments.extract()
		if "album id" in this_comment:
			bandcamp_track_id = re.sub('[^0-9]','', this_comment)
			bandcamp_track_type = 'album'
			bandcamp_links.append({"link":album_link,"id":bandcamp_track_id,"type":"album"})
			break
		elif "track id" in this_comment:
			bandcamp_track_id = re.sub('[^0-9]','', this_comment)
			bandcamp_track_type = 'track'
			bandcamp_links.append({"link":album_link,"id":bandcamp_track_id,"type":"track"})
			break


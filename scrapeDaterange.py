import importlib
import datetime
from geopy.geocoders import Nominatim
import json

bandcampScrape = importlib.import_module("bandcampScrape")
beatScrape = importlib.import_module("beatScrape")

#scrape a page of the gig guide to get gig links, gig genres
beat_url = "http://www.beat.com.au/"

#scrape between a date range
start_date = datetime.date(2018,7,1)
end_date = datetime.date(2018,7,6)

delta = end_date - start_date

allGigs = []
#maintain an overall list of venues, headline artists and support artists so those only get scraped once
allHeadlineArtist = []
allSupportArtist=[]
allVenue=[]

for j in range(delta.days):
    this_date = start_date + datetime.timedelta(j)
    this_link = beat_url + "gig-guide/" + this_date.strftime("%Y-%m-%d")
    print(this_link)
    gigGuideGigs = beatScrape.BeatGigGuideScrape(this_link)
    #loop through and get the gig details
    for i in range(len(gigGuideGigs)):
    #for i in range(1):
        gig_link = gigGuideGigs[i].get("gigLink")
        print(gig_link)
        gigDetails = beatScrape.BeatGigScrape(beat_url + gig_link)
        gigGuideGigs[i]["gigPrice"] = gigDetails.get("gigPrice")
        gigGuideGigs[i]["gigHeadlineArtist"] = gigDetails.get("gigHeadlineArtist")
        gigGuideGigs[i]["gigSupportArtist"] = gigDetails.get("gigSupportArtist")
        gigGuideGigs[i]["gigVenue"] = gigDetails.get("gigVenue")
        gigGuideGigs[i]["gigDatetime"] = gigDetails.get("gigDatetime")
        #append to the overall arrays
        allHeadlineArtist.extend(gigDetails.get("gigHeadlineArtist"))
        allSupportArtist.extend(gigDetails.get("gigSupportArtist"))
        allVenue.append(gigDetails.get("gigVenue"))
    allGigs.extend(gigGuideGigs)

#reduce the all lists to unique values
allHeadlineArtist = list(set(allHeadlineArtist))
allSupportArtist = list(set(allSupportArtist))
allVenue = list(set(allVenue))

#perhaps should check which of these are new before scraping??

#maybe not, could be a chance to update reference information
#only artists who have gigs get updated then... hmmm..

#loop through the headline artists
headlineArtistPayload = []
for i in range(len(allHeadlineArtist)):
#for i in range(50,60):
    headlineArtistLink = beat_url + allHeadlineArtist[i]
    print(headlineArtistLink)
    beatArtist = beatScrape.BeatHeadlineArtistScrape(headlineArtistLink)
    bandcampArtist = bandcampScrape.BandcampBandSearch(beatArtist.get("artistName"))
    #append this new artist to the total payload
    headlineArtistPayload.append({
        "source":"beat-headline",
        "sourceId":allHeadlineArtist[i],
        "artistName":beatArtist.get("artistName"),
        "links":[
            {
                "linkSource":"bandcamp",
                "linkUrl":bandcampArtist.get("bandcampLink"),
                "linkAttributes":{
                    "bandcampTracks":bandcampArtist.get("bandcampTracks")
                }
            }
        ]
    })

#loop through support artists
supportArtistPayload = []
for i in range(len(allSupportArtist)):
#for i in range(50,60):
    artistLink = beat_url + allSupportArtist[i]
    print(artistLink)
    beatArtist = beatScrape.BeatHeadlineArtistScrape(artistLink)
    bandcampArtist = bandcampScrape.BandcampBandSearch(beatArtist.get("artistName"))
    #append this new artist to the total payload
    supportArtistPayload.append({
        "source":"beat-support",
        "sourceId":allSupportArtist[i],
        "artistName":beatArtist.get("artistName"),
        "links":[
            {
                "linkSource":"bandcamp",
                "linkUrl":bandcampArtist.get("bandcampLink"),
                "linkAttributes":{
                    "bandcampTracks":bandcampArtist.get("bandcampTracks")
                }
            }
        ]
    })

#loop through venues
venuePayload = []
geolocator = Nominatim()
for i in range(len(allVenue)):
    venueUrl=beat_url + allVenue[i]
    venueDetails = beatScrape.BeatVenueScrape(venueUrl)
    venueLocation = geolocator.geocode(venueDetails.get("venueAddress"))
    venuePayload.append({
        "source":"beat",
        "sourceId":allVenue[i],
        "venueName":venueDetails.get("venueName"),
        "venueAddress":venueDetails.get("venueAddress"),
        "lat":venueLocation.latitude,
        "lon":venueLocation.longitude
    })

#save data
with open('gigData.json', 'w') as outfile:
    json.dump(allGigs, outfile)

with open('headlineArtistPayload.json', 'w') as outfile:
    json.dump(headlineArtistPayload, outfile)

with open('supportArtistPayload.json', 'w') as outfile:
    json.dump(supportArtistPayload, outfile)

with open('venuePayload.json', 'w') as outfile:
    json.dump(venuePayload, outfile)


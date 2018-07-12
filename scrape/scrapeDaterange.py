import importlib
import datetime
from geopy.geocoders import Nominatim
import requests
import urllib.parse
from time import sleep

api_url = 'https://beat-magazine-map.herokuapp.com'
beat_url = "http://www.beat.com.au/"
n_days = 0


def PostPayload(objectId,payload, apiEndpoint):
    retry_max = 10
    retry_count = 0
    request_success = False
    this_endpoint = api_url + '/' + apiEndpoint + '/push/' + urllib.parse.quote_plus(objectId)
    while(request_success == False and retry_count < retry_max):
        try:
            r = requests.post(this_endpoint, json = payload)
            request_success = True
        except:
            print("Venue scrape - cannot find coordinates")
            retry_count += 1
            r = 'Failure'
            sleep(retry_count)
    return(r)

def GetAddressLatLon(address):
    retry_max = 10
    retry_count = 0
    request_success = False
    geolocator = Nominatim()
    returnObject = {
        "latitude":None,
        "longitude":None
    }
    while(request_success == False and retry_count < retry_max):
        try:
            location = geolocator.geocode(address)
            request_success = True
        except:
            print("Geolocator failed")
            retry_count += 1
            sleep(retry_count)
    if request_success == True:
        try:
            returnObject["latitude"] = location.latitude
            returnObject["longitude"] = location.longitude
        except:
            print("No lat lon for address " + address)
    return(returnObject)

bandcampScrape = importlib.import_module("bandcampScrape")
beatScrape = importlib.import_module("beatScrape")

#scrape a page of the gig guide to get gig links, gig genres

#scrape between a date range
start_date = datetime.datetime.now().date()
end_date = start_date + datetime.timedelta(n_days)

delta = end_date - start_date

allGigs = []
#maintain an overall list of venues, headline artists and support artists so those only get scraped once
allHeadlineArtist = []
allSupportArtist=[]
allVenue=[]

for j in range(delta.days + 1):
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
        gigGuideGigs[i]["gigDate"] = this_date.strftime('%Y-%m-%d')
        #append to the overall arrays
        allHeadlineArtist.extend(gigDetails.get("gigHeadlineArtist"))
        allSupportArtist.extend(gigDetails.get("gigSupportArtist"))
        allVenue.append(gigDetails.get("gigVenue"))
    allGigs.extend(gigGuideGigs)


#reduce the all lists to unique values
allHeadlineArtist = list(set(allHeadlineArtist))
allSupportArtist = list(set(allSupportArtist))
allVenue = list(set(allVenue))

allHeadlineArtist = [x for x in allHeadlineArtist if x is not None]
allSupportArtist = [x for x in allSupportArtist if x is not None]
allVenue = [x for x in allVenue if x is not None]
#perhaps should check which of these are new before scraping??

#maybe not, could be a chance to update reference information
#only artists who have gigs get updated then... hmmm..

#loop through the headline artists
for i in range(len(allHeadlineArtist)):
#for i in range(50,60):
    artistId = allHeadlineArtist[i]
    artistLinks = {}
    headlineArtistLink = beat_url + artistId
    print(artistId)
    beatArtist = beatScrape.BeatHeadlineArtistScrape(headlineArtistLink)
    try:
        bandcampArtist = bandcampScrape.BandcampBandSearch(beatArtist.get("artistName"))
        if bandcampArtist.get("bandcampLink") != None:
            artistLinks["bandcamp"] = {
                "bandcampPage":bandcampArtist.get("bandcampLink"),
                "bandcampTracks":{
                    "bandcampTracks":bandcampArtist.get("bandcampTracks")
                }
            }
    except:
        print("Bandcamp scrape failed")
    try:
        #append this new artist to the total payload
        payload = {
            "beatArtistType":"headline",
            "artistName":beatArtist.get("artistName"),
            "artistLinks":artistLinks
        }
        r = PostPayload(objectId = artistId,payload = payload, apiEndpoint = "artist")
    except:
        print("Artist " + artistId + " post failed")


#loop through support artists
for i in range(len(allSupportArtist)):
#for i in range(50,60):
    artistId = allSupportArtist[i]
    artistLinks = {}
    headlineArtistLink = beat_url + artistId
    print(artistId)
    beatArtist = beatScrape.BeatHeadlineArtistScrape(headlineArtistLink)
    try:
        bandcampArtist = bandcampScrape.BandcampBandSearch(beatArtist.get("artistName"))
        if bandcampArtist.get("bandcampLink") != None:
            artistLinks["bandcamp"] = {
                "bandcampPage":bandcampArtist.get("bandcampLink"),
                "bandcampTracks":{
                    "bandcampTracks":bandcampArtist.get("bandcampTracks")
                }
            }
    except:
        print("Bandcamp scrape failed")
    try:
        #append this new artist to the total payload
        payload = {
            "beatArtistType":"headline",
            "artistName":beatArtist.get("artistName"),
            "artistLinks":artistLinks
        }
        r = PostPayload(objectId = artistId,payload = payload, apiEndpoint = "artist")
    except:
        print("Artist " + artistId + " post failed")


#loop through venues
for i in range(len(allVenue)):
    venueId = allVenue[i]
    venueUrl=beat_url + venueId
    print(venueId)
    venueDetails = beatScrape.BeatVenueScrape(venueUrl)
    #try to use venueLocation
    #otherwise try to use google
    venueLocation = GetAddressLatLon(venueDetails.get("venueAddress"))
    lat = venueLocation.get("latitude")
    lon = venueLocation.get("longitude")
    try:
        #append this new artist to the total payload
        payload = {
            "venueName":venueDetails.get("venueName"),
            "venueAddress":venueDetails.get("venueAddress"),
            "lat":lat,
            "lon":lon
        }
        r = PostPayload(objectId = venueId,payload = payload, apiEndpoint = "venue")
    except:
        print("Venue " + venueId + " post failed")

#now finally post the gigs
for i in range(len(allGigs)):
    thisGig = allGigs[i]
    gigId = thisGig.get("gigLink")
    print(gigId)
    try:
        payload = {
            "gigGenre":thisGig.get("gigGenre"),
            "gigDatetime":thisGig.get("gigDatetime"),
            "venueId":thisGig.get("gigVenue"),
            "headlineArtist":thisGig.get("gigHeadlineArtist"),
            "supportArtist":thisGig.get("gigSupportArtist"),
            "gigPrice":thisGig.get("gigPrice")
        }
        r = PostPayload(objectId = gigId,payload = payload, apiEndpoint = "gig")
    except:
        print("Gig " + gigId + " post failed")

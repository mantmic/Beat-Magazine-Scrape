import importlib

bandcampScrape = importlib.import_module("bandcampScrape")
beatScrape = importlib.import_module("beatScrape")

#scrape a page of the gig guide to get gig links, gig genres
beat_url = "http://www.beat.com.au/"
gig_guide = "gig-guide/2018-07-01"

gigGuideGigs = beatScrape.BeatGigGuideScrape(beat_url + gig_guide)

#loop through and get the gig details
#maintain an overall list of venues, headline artists and support artists so those only get scraped once
allHeadlineArtist = []
allSupportArtist=[]
allVenue=[]

for i in range(len(gigGuideGigs)):
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
gigVenue = gigDetails.get("gigVenue")

venueDetails = beatScrape.BeatVenueScrape(beat_url + gigVenue)

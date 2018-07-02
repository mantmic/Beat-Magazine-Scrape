import importlib

bandcampScrape = importlib.import_module("bandcampScrape")
beatScrape = importlib.import_module("beatScrape")

#scrape a page of the gig guide to get gig links, gig genres
beat_url = "http://www.beat.com.au/"
gig_guide = "gig-guide/2018-07-01"

gigGuideGigs = beatScrape.BeatGigGuideScrape(beat_url + gig_guide)

gig_link = gigGuideGigs[0].get("gigLink")

gigDetails = beatScrape.BeatGigScrape(beat_url + gig_link)
gigHeadlineArtist = gigDetails.get("gigHeadlineArtist")
headlineArtistLink = beat_url + gigHeadlineArtist[0]
beatArtist = beatScrape.BeatHeadlineArtistScrape(headlineArtistLink)
bandcampArtist = bandcampScrape.BandcampBandSearch(beatArtist.get("artistName"))

gigVenue = gigDetails.get("gigVenue")

venueDetails = beatScrape.BeatVenueScrape(beat_url + gigVenue)

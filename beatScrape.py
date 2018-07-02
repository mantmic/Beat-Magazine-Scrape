from urllib import request
from bs4 import BeautifulSoup

def BeatHeadlineArtistScrape(headlineArtistLink):
    #scrape headlinining artists 
    page = request.urlopen(headlineArtistLink)
    soup = BeautifulSoup(page, "html5lib")
    return({
        "artistName":soup.find('h2', {"class":"node-title"}).text
    })


def BeatGigScrape(gigUrl):
    page = request.urlopen(gigUrl)
    soup = BeautifulSoup(page, "html5lib")
    gig_info = soup.find('div',{"class":"w-clearfix gigguide_gigdetail-details"})
    gig_details = gig_info.find_all('h5',{"class":"gigguide_node-summary-detail"})
    
    gigHeadlineArtist = []
    gigSupportArtist = []
    gigVenue = None
    gigPrice = None
    gigDatetime = None
    
    #determine what each thing is
    for i in range(len(gig_details)): 
        gig_detail = gig_details[i]
        #classify detail
        gig_link = gig_detail.find("a")
        gig_span = gig_detail.find("span")
        if gig_link is None:
            #not a venue or artist
            #check if there is a date
            if gig_span is None:
                if "$" in gig_detail.text:
                    gigPrice = gig_detail.text
            else:
                #this the date 
                gigDatetime = gig_span.text
        else:
            href = gig_link.get("href")
            if "artist/" in href:
                gigHeadlineArtist.append(href)
            elif "support" in href:
                gigSupportArtist.append(href)
            elif "venue" in href:
                gigVenue = href
    return({
        "gigHeadlineArtist":gigHeadlineArtist,
        "gigSupportArtist":gigSupportArtist,
        "gigVenue":gigVenue,
        "gigPrice":gigPrice,
        "gigDatetime":gigDatetime
    })

#scrape location information 
def BeatVenueScrape(venueUrl):
    venueName = None
    venueAddress = None
    page = request.urlopen(venueUrl)
    soup = BeautifulSoup(page, "html5lib")
    
    location_detail=soup.find('div',{"class":"w-clearfix gigguide_gigdetail-details"})
    
    #get name 
    venueName = soup.find('h1',{"class":"article_title"}).text
    
    field_labels = location_detail.find_all('h5',{"class":"gigguide_gigdetail-field-label"})
    
    for i in range(len(field_labels)):
        	if 'address' in field_labels[i].text.lower():
        		venueAddress = field_labels[i].findNext('h5').text
        		if venueAddress != None:
        			break
    return({
        "venueName":venueName,
        "venueAddress":venueAddress
    })

def BeatGigGuideScrape(gigGuideUrl):
    page = request.urlopen(gigGuideUrl)
    soup = BeautifulSoup(page, "html5lib")
    
    gigs = soup.find_all("h3", {"class":"archive_node-summary-title"})
    
    gigGuideGigs = []
    
    for i in range(len(gigs)):
        gig = gigs[i]
        gigName=gig.text
        gigLink=gig.find("a").get("href")
        gigGenre=gigs[0].parent.parent.parent.parent.find("a").text
        #remove the brackets and number
        gigGuideGigs.append({
            "gigName":gigName,
            "gigLink":gigLink,
            "gigGenre":gigGenre
        })
    return(gigGuideGigs)

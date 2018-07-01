# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib
from bs4 import BeautifulSoup

beat_url = "http://www.beat.com.au/"

gig_guide = "gig-guide/2018-07-01"

page = urllib.request.urlopen(beat_url + gig_guide)
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



#now scrape a single gig
page = urllib.request.urlopen(beat_url + gig_link)
soup = BeautifulSoup(page)

soup.prettify()

#get gig info
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

#now we have artists to scrape as well 
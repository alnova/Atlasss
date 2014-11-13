import json
import urllib2
import re
import string

from StringIO import StringIO
from BeautifulSoup import BeautifulSoup
from atlas.models import RealObject


#Global selections for payloads
api_key = ''
tags = list()

goodReads_api_key = 'jYJwJLt5hGjtMustaWaS9Q'
goodReads_api_secret = '99F7SX3ZDCVemUvgTISkUqVLKCxd7NSK39cV38rw'

etsy_api_key = 'iqz5tb9wzxg18xd91e8f8yj1'
etsy_api_secret = '8oexal01qs'

''' A helper function, to find a string containing spaces. 
    i.e. it will find "the red fish" or 
    if you search for "red" it will find it 
    but not "adhered" 
'''

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def searchEtsy(phrase,maxNumber):
    try:
        query = phrase.phrase
        query = '+'.join(query.split()) #replace spaces with '+' for url format
        urlFormatSearch = 'https://openapi.etsy.com/v2/listings/active?keywords=' + query +'&limit=12&includes=Images:1&api_key='+etsy_api_key
        url = urllib2.urlopen(urlFormatSearch)
        chunk = url.read()
        io = StringIO( chunk )
        etsyItems = json.load(io)
        toRet = []
        for item in etsyItems['results']:
            newEtsy = RealObject()
            newEtsy.name = item['title']
            newEtsy.image = item['Images'][0]['url_170x135']
            newEtsy.title = phrase.title
            newEtsy.id = phrase.id
            newEtsy.phrase = phrase.phrase
            newEtsy.source = "etsy"
            toRet.append(newEtsy)
        return toRet
    except Exception as e:
        print e
        return []
    

def makeInstructable(soup):
    """Given a BeautifulSoup object from an instructables page,
	create and return an instructables object. Return None on error."""

    try:
        instr = RealObject()

        meta = soup.findAll('meta')
        meta = [x for x in meta if x.get('property') is not None]
        #print meta
        #print "********************before for loop*************"
        for x in meta:
            #print x.get('property'), x.get('content')
            if "og:title" in x.get('property'):
                instr.name = x.get('content')
		    #elif "og:type" in x.get('property'):
		    #	otype = x.get('content')
            elif "og:url" in x.get('property'):
                instr.url = x.get('content')
            elif "og:image" in x.get('property'):
                # print "image is %s" % x.get('content')
                instr.image = x.get('content')
            elif "og:description" in x.get('property'):
                instr.description = x.get('content')
        return instr
    except Exception as e:
        print e
        return None

def instructablesSearch(phrase, maxNumber, detailed=False,returnType='dictionary' ):
    """Given a string search query, return a list of Instructables objects.
	The list will contain no more than 'maxNumber' items and can be empty.
	If 'detailed' is set to False, each object has only the title, image, and
	url (no description), but returns quickly. If true, each object also has
	description populated, but requires fetching a new html page for every
	object."""

    try:
        query = phrase.phrase
        query = '+'.join(query.split()) #replace spaces with '+' for url format
        soup = BeautifulSoup(urllib2.urlopen("http://www.instructables.com/tag/type-id/featured-true/?sort=none&q=" + query)) # soup object of search results page
        res = soup.find(id="infinite-search-results")
        res = res.findAll('li')
        if (maxNumber < len(res)):
		    res = res[:maxNumber]

        toRet = []

        if not detailed:
            for x in res:
                instr = RealObject()
                instr.name = x.a.get('title') # ISSUE: this will cut off titles with
                    # quotes. Can use #instr.name = x.div.div.a.get_text() instead,
                    # but this will cut off titles that are longer than the two-line
				    # instructables title space...
                instr.image = x.a.img.get('src')
                instr.url = "http://www.instructables.com" + x.a.get('href')
                instr.description = None
                instr.title = phrase.title
                instr.id = phrase.id
                instr.phrase = phrase.phrase
                instr.source = "instructables"
                toRet.append(instr)

        elif detailed:
		    for x in res:
			    soup = BeautifulSoup(urllib2.urlopen("http://www.instructables.com" + x.a.get('href')))
			    toRet.append(makeInstructable(soup))

        toRet = [x for x in toRet if x is not None]
        return toRet

    except Exception as e:
        print e
        return []

def getThingiverse(url):
    """Given a url for a Thingiverse page, extract content and return
    Thingiverse idea. Return None on error."""
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))

        newThing = RealObject()

        newThing.url = url
        newThing.name = soup.find('h1').string
        newThing.image = soup.find(attrs={"class": "thing-page-image featured"}).img.get('src')
        s = soup.find(id="description")
        s = str(s)
        start = string.find(s,">")
        end = string.find(s,"</div>",start)
        s = s[start+1:end]

        while string.find(s,'<') is not -1:
            start = string.find(s,'<')
            end = string.rfind(s,'>')
            s = s.replace(s[start:end+1],"")

        newThing.description = s.strip()
        newThing.source = "thingiverse"
        return newThing

    except Exception as e:
        print e
        return None

def searchThingiverse(phrase, number, detailed=False):
    """Search query on Thingiverse, returning a list of a maximum of number
    Thingiverse objects. The list can be empty. If detailed is False,
    the descriptions will be ommitted from each object, but the search will
    return faster."""

    try:
        query = phrase.phrase
        query = '+'.join(query.split())
        baseurl = "http://www.thingiverse.com/search/prolific/things/page:"
        endurl = "?q="
        allThings = []
    
        try:
            for i in range(1, int(number - 1) / 12 + 2):
                soup = BeautifulSoup(urllib2.urlopen(baseurl + str(i) + endurl + query))
                results = soup.findAll(attrs={"data-thing-id": True})
                if detailed:
                    for x in results:
                        allThings.append(getThingiverse("http://www.thingiverse.com" + x.div.a.get('href')))
    
                elif not detailed:
                    for x in results:
                        newThing = RealObject()
                        newThing.name = x.get('title')
                        newThing.url = "http://www.thingiverse.com/thing:" + x.get('data-thing-id')
                        newThing.image = x.img.get('src')
                        newThing.id = phrase.id
                        newThing.title = phrase.title
                        newThing.phrase = phrase.phrase
                        newThing.source = "thingiverse"
                        allThings.append(newThing)
    
            allThings = [x for x in allThings if x is not None]
            return allThings[:number]
        except:
            return []
    except:
        return []


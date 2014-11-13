import json

from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from atlas.forms import *
from atlas.models import *
from atlas import searchclient

MEMCACHE_GREETINGS = 'greetings'
MEMCACHE_STORY = 'story'

def list_stories(request):
    mode = int ( request.GET.get('mode', '0') )
    participantID = int( request.GET.get('id', '222') )
    story = cache.get(MEMCACHE_STORY)
    if story is None:
        story = Story.objects.all().order_by('-date')
    imageList = []
    numImages = 48
    i = 0
    while i < numImages:
        imageList.append( { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
        i += 1
    return direct_to_template(request, 'atlas/stories.html',
                              {'stories': story,
                               'imageList': imageList,
                               'mode':mode,
                               'participantID':participantID

     } )

def Content_Art_Object_Time(request,title):
    allStories = Story.objects.all().filter(url=title).order_by('-date')
    print allStories
    response_data = {}
    content = []
    imageInfo = []
    for each in allStories:
        content = each.content.split()
        realObj = RealObject.objects.all().filter(title=each.title).order_by('-date')
        try:
            realObjFirstTime = realObj[0].date
            realObjEndTime = realObj[len(realObj)-1].date
            realObjTotalTime = realObjFirstTime -realObjEndTime
            #from datetime import timedelta
            # d = timedelta(microseconds=-1)
            # >>> (d.days, d.seconds, d.microseconds)
            for item in realObj:
                imageInfo.append([ float( ( realObjFirstTime-item.date).seconds / realObjTotalTime.total_seconds() ), item.image, item.phrase])
        except:
            pass
    response_data['message'] = 'From Django, transmission is working...'
    return direct_to_template(request, 'atlas/Content_Art_Object_Time.html',
                              {'content': content,
                              'imageInfo': imageInfo
     } )

def d3Pattern(request):
    return direct_to_template(request, 'atlas/d3Patterns.html',
                              {} )

def ImageVote(request):
    if request.method == 'POST':
        sent = request.POST
        sentID = sent['name']
        success = sentID
        try:
            query = RealObject.objects.get(id=sentID)
            query.score += 1
            query.save()
            success = 1
        except:
            success = sentID
            fallBack(sentID);
        return HttpResponse({ success } )

def fallBack(sentID):
    try:
        query = RealObject.objects.get(id=sentID)
        query.score += 1
        #query.save()
        success = 1
    except:
        success = sentID

def show_preselected_images(request,terms):
    #print request.method
    mode = int ( request.GET.get('mode', '0') )
    participantID = int( request.GET.get('id', '222') )
    images = RealObject.objects.all().filter(title=terms).order_by('-score')
    imageList = []
    nameList = []
    numImages = 48
    i = 0
    # duplicate out existing images for new story
    for each in images:
        if ( len(imageList) < numImages ):
            newRealObject = RealObject()
            # if request.user.is_authenticated():
            #     newRealObject.title = request.user.username
            # else:
            #     newRealObject.title = 'untitled'
            newRealObject.title = participantID
            newRealObject.image = each.image
            newRealObject.name = each.name
            newRealObject.phrase = each.phrase
            newRealObject.source = each.source
            newRealObject.url = each.url
            newRealObject.score = 0
            newRealObject.save()
            imageList.append( { 'image': newRealObject.image , 'id':newRealObject.id } )
            i += 1
        else:
            break
    while i < numImages:
        imageList.append( { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
        i += 1
    page = 'atlas/index.html'
    if (mode == 1):
        imageList = []
        i = 0;
        while i < numImages:
            imageList.append(  { 'image': '../media/images/whiteSquare.png' , 'id':'' } )
            i += 1
        page = 'atlas/indexNoneImg.html'
    if (mode == 2):
        imageList = []
        i = 0;
        while i < numImages:
            imageList.append(  { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
            i += 1
        page = 'atlas/indexStatic.html'
    if (mode == 3):
        page = 'atlas/nature.html'
    return direct_to_template(request, page ,
                                  {'form': CreateStoryForm(),
                                   'imageList': imageList, 'mode':mode, 'participantID':participantID
                                    } )

def mainPage(request):
    #print request.method
    mode = int ( request.GET.get('mode', '1') )
    participantID = int( request.GET.get('id', '222') )
    # story = cache.get(MEMCACHE_STORY)
    # if story is None:
    #     story = Story.objects.all().order_by('-date')[0]

    imageList = []
    nameList = []
    numImages = 48
    page = 'atlas/index.html'
    if (mode == 1):
        i = 0
        # duplicate out existing images for new story
        images = RealObject.objects.all().order_by('-score')
        for each in images:
            if ( len(imageList) < numImages ):
                newRealObject = RealObject()
                # if request.user.is_authenticated():
                #     newRealObject.title = request.user.username
                # else:
                #     newRealObject.title = 'untitled'
                newRealObject.title = participantID
                newRealObject.image = each.image
                newRealObject.name = each.name
                newRealObject.phrase = each.phrase
                newRealObject.source = each.source
                newRealObject.url = each.url
                newRealObject.score = 0
                newRealObject.save()
                imageList.append( { 'image': newRealObject.image , 'id':newRealObject.id } )
                i += 1
            else:
                break
        while i < numImages:
            imageList.append( { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
            i += 1
        page = 'atlas/index.html'
    if (mode == 2):
        i = 0
        images = RealObject.objects.all().filter(title='Nature').order_by('-score')
        for each in images:
            if ( len(imageList) < numImages ):
                newRealObject = RealObject()
                # if request.user.is_authenticated():
                #     newRealObject.title = request.user.username
                # else:
                #     newRealObject.title = 'untitled'
                newRealObject.title = participantID
                newRealObject.image = each.image
                newRealObject.name = each.name
                newRealObject.phrase = each.phrase
                newRealObject.source = each.source
                newRealObject.url = each.url
                newRealObject.score = 0
                newRealObject.save()
                imageList.append( { 'image': newRealObject.image , 'id':newRealObject.id } )
                i += 1

        page = 'atlas/indexStatic.html'
    if (mode == 3):
        # Static mode, Between Tech
        imageList = []
        i = 0;
        # Static mode, Robots
        while i < numImages:
            imageList.append(  { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
            i += 1

        page = 'atlas/indexStatic.html'

    if (mode == 4):
        imageList = []
        i = 0;
        while i < numImages:
            imageList.append(  { 'image': '../media/images/whiteSquare.png' , 'id':'' } )
            i += 1
        page = 'atlas/indexNoneImg.html'
    if (mode == 5):
        imageList = []
        story = Story.objects.all().order_by('-date')[0]
        images = RealObject.objects.all().filter(title=story.title).order_by('-score')
        for each in images:
            if ( len(imageList) < numImages ):
                imageList.append( { 'image': each.image , 'id':'' } )
        page = 'atlas/indexReadStatic.html'
        return direct_to_template(request, page ,
                                  {'content':story.content,
                                   'imageList': imageList, 'mode':mode, 'participantID':participantID
                                    } )
    if (mode == 6):
        imageList = []
        story = Story.objects.all().order_by('-date')[0]
        page = 'atlas/indexReadNoneImg.html'
        return direct_to_template(request, page ,
                                  {'content':story.content,
                                   'imageList': imageList, 'mode':mode, 'participantID':participantID
                                    } )
    if (mode == 7):
        i = 0
        # duplicate out existing images for new story
        images = RealObject.objects.all().order_by('-score')
        numImages = 12
        for each in images:
            if ( len(imageList) < numImages ):
                newRealObject = RealObject()
                # if request.user.is_authenticated():
                #     newRealObject.title = request.user.username
                # else:
                #     newRealObject.title = 'untitled'
                newRealObject.title = participantID
                newRealObject.image = each.image
                newRealObject.name = each.name
                newRealObject.phrase = each.phrase
                newRealObject.source = each.source
                newRealObject.url = each.url
                newRealObject.score = 0
                newRealObject.save()
                imageList.append( { 'image': newRealObject.image , 'id':newRealObject.id } )
                i += 1
            else:
                break
        while i < numImages:
            imageList.append( { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
            i += 1
        page = 'atlas/indexStyleBS.html'
    if (mode == 8):
        i = 0
        # duplicate out existing images for new story
        images = RealObject.objects.all().order_by('-score')
        numImages = 12
        for each in images:
            if ( len(imageList) < numImages ):
                newRealObject = RealObject()
                # if request.user.is_authenticated():
                #     newRealObject.title = request.user.username
                # else:
                #     newRealObject.title = 'untitled'
                newRealObject.title = participantID
                newRealObject.image = each.image
                newRealObject.name = each.name
                newRealObject.phrase = each.phrase
                newRealObject.source = each.source
                newRealObject.url = each.url
                newRealObject.score = 0
                newRealObject.save()
                imageList.append( { 'image': newRealObject.image , 'id':newRealObject.id } )
                i += 1
            else:
                break
        while i < numImages:
            imageList.append( { 'image': 'http://robohash.org/karie' +str(i)+ 'fury.png', 'id':'' } )
            i += 1
        page = 'atlas/indexStyleIS.html'
    # return normal index page ( write mode...)
    return direct_to_template(request, page ,
                                  {'form': CreateStoryForm(),
                                   'imageList': imageList, 'mode':mode, 'participantID':participantID
                                    } )

def screenedSelection():
    return()
# def create_greeting(request):
#     mode = int ( request.GET.get('mode', '') )
#     participantID = int( request.GET.get('id', '') )
#     if request.method == 'POST':
#         form = CreateGreetingForm(request.POST)
#         if form.is_valid():
#             greeting = form.save(commit=False)
#             if request.user.is_authenticated():
#                 greeting.author = request.user
#             greeting.save()
#             cache.delete(MEMCACHE_GREETINGS)
#     print 'mode ' + mode
#     return HttpResponseRedirect('/atlas/')

def Reset(request):
    RealObject.objects.all().delete()
    query0 = KeywordPhrase.objects.all().delete()
    query1 = Greeting.objects.all().delete()
    query2 = Story.objects.all().delete()
    query3 = Author.objects.all().delete()
    return HttpResponseRedirect('/atlas/')

def create_story(request):
    mode = int ( request.GET.get('mode', '') )
    participantID = int( request.GET.get('id', '') )
    if request.method == 'POST':
        form = CreateStoryForm(request.POST)
        # print 'here'
        #print form
        if form.is_valid():
            story = form.save(commit=False)
            story.url = story.title.replace(" ", "")
            story.timeToWrite = story.timeToWrite
            story.authorName = participantID
            story.mode = mode
            if request.user.is_authenticated():
                story.authorID = request.user
                story.authorName = request.user.username
            story.save()
        # cache.delete(MEMCACHE_STORY)
        else:
            print 'eat a plant and go to hell'
        realObjectsInStory = RealObject.objects.filter(title=participantID)
        for each in realObjectsInStory:
            each.title = story.title
            each.save()
    return HttpResponseRedirect('https://ucsbltsc.qualtrics.com/SE/?SID=SV_6JYyy92DKPxdIq1&mode='+str(mode)+'&id='+str(participantID))

def rate_story(request):
    mode = int ( request.GET.get('mode', '') )
    participantID = int( request.GET.get('id', '') )
    return HttpResponseRedirect('https://ucsbltsc.qualtrics.com/SE/?SID=SV_6JYyy92DKPxdIq1&mode='+str(mode)+'&id='+str(participantID))


def create_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/atlas/')
    else:
        form = UserCreationForm()
    return direct_to_template(request, 'atlas/user_create_form.html',
        {'form': form})

def occurance(request):
    return direct_to_template(request, 'atlas/occuranceOfFreqWords.html',
        {})

def singleStoryView(request, titleS):
    singleStory = Story.objects.all().filter(url=titleS)[0]
    allRealObjects = RealObject.objects.all().filter(title=singleStory.title)
    story = {"story":singleStory,"realObjects": allRealObjects }
    return direct_to_template(request, 'atlas/d3Patterns.html', {"story":story} )

def graph(request):
    return direct_to_template(request, 'atlas/graph.html',
        {})

def PhysicalModelView(request,terms,title):
    # print terms
    # Make Physical Model View a more involved process.
    if not ( searchclient.isStopWord(terms) ):
        queryPhrase = KeywordPhrase()
        queryPhrase.title = title
        queryPhrase.phrase = terms
        # queryPhrase.save()

        searchResults = []
        searchResults.append( searchclient.instructablesSearch( queryPhrase, 3 ) )
        searchResults.append( searchclient.searchThingiverse( queryPhrase, 3 ) )
        searchResults.append( searchclient.searchEtsy( queryPhrase, 3 ) )
        response_data = {}
        response_data['images'] = []
        response_data['id'] = []
        for each in searchResults:
            # Check and see if already in db..
            for item in each:
                newRealObject = RealObject()
                newRealObject.title = title
                newRealObject.image = item.image
                newRealObject.name = item.name
                newRealObject.phrase = terms
                newRealObject.source = item.source
                newRealObject.url = item.url
                newRealObject.score = 0
                newRealObject.save()
                response_data['images'].append(newRealObject.image)
                response_data['id'].append(newRealObject.id)


        response_data['message'] = 'From Django, transmission is working...'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['message'] = 'From Django, transmission is working...'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def instSearch(request,terms,title):
    # print terms
    # Make Physical Model View a more involved process.
    if not ( searchclient.isStopWord(terms) ):
        queryPhrase = KeywordPhrase()
        queryPhrase.title = title
        queryPhrase.phrase = terms
        # queryPhrase.save()

        searchResults = []
        searchResults.append( searchclient.instructablesSearch( queryPhrase, 4 ) )
        searchResults.append( searchclient.searchThingiverse( queryPhrase, 4 ) )
        response_data = {}
        response_data['images'] = []
        response_data['id'] = []
        for each in searchResults:
            # Check and see if already in db..
            for item in each:
                newRealObject = RealObject()
                newRealObject.title = title
                newRealObject.image = item.image
                newRealObject.name = item.name
                newRealObject.phrase = terms
                newRealObject.source = item.source
                newRealObject.url = item.url
                newRealObject.score = 0
                newRealObject.save()
                response_data['images'].append(newRealObject.image)
                response_data['id'].append(newRealObject.id)


        response_data['message'] = 'From Django, transmission is working...'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['message'] = 'From Django, transmission is working...'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def Stories(request):
    # print terms
    allStories = Story.objects.all().order_by('-date')
    allRealObjects = RealObject.objects.all()
    response_data = {}
    response_data['stories'] = []
    response_data['realObjects'] = []
    for each in allStories:
        jsonStory = {}
        jsonStory['authorName'] = each.authorName
        jsonStory['title'] = each.title
        jsonStory['content'] = each.content
        response_data['stories'].append(jsonStory)
    for each in allRealObjects:
        jsonRealObj = {}
        jsonRealObj['title'] = each.title
        jsonRealObj['date'] = each.date.isoformat()
        jsonRealObj['image'] = each.image
        jsonRealObj['source'] = each.source
        jsonRealObj['score'] = each.score
        jsonRealObj['phrase'] = each.phrase
        jsonRealObj['name'] = each.name
        response_data['realObjects'].append(jsonRealObj)
    response_data['message'] = 'From Django, transmission is working...'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def storyTitle(request,titleS):
    # print terms
    allStories = Story.objects.all().filter(title=titleS)
    allRealObjects = RealObject.objects.all().filter(title=titleS)
    response_data = {}
    response_data['stories'] = []
    response_data['realObjects'] = []
    for each in allStories:
        jsonStory = {}
        jsonStory['authorName'] = each.authorName
        jsonStory['title'] = each.title
        jsonStory['content'] = each.content
        response_data['stories'].append(jsonStory)
    for each in allRealObjects:
        jsonRealObj = {}
        jsonRealObj['title'] = each.title
        jsonRealObj['date'] = each.date.isoformat()
        jsonRealObj['url'] = each.url
        jsonRealObj['image'] = each.image
        jsonRealObj['source'] = each.source
        jsonRealObj['score'] = each.score
        jsonRealObj['phrase'] = each.phrase
        jsonRealObj['name'] = each.name
        response_data['realObjects'].append(jsonRealObj)
    response_data['message'] = 'From Django, transmission is working...'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def imageSearch(request,word):
    response_data = searchclient.gSearch(word,10)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def TypeOfWord(request,word):
    response_data = searchclient.wolframAlphaSearch(word,10)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

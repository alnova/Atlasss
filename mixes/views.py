import json

from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from atlas.forms import CreateGreetingForm
from atlas.models import *
from atlas import searchclient

MEMCACHE_GREETINGS = 'greetings'
MEMCACHE_STORY = 'story'

def list_greetings(request):
    greetings = cache.get(MEMCACHE_GREETINGS)
    story = cache.get(MEMCACHE_STORY)
    if greetings is None:
        greetings = Greeting.objects.all().order_by('-date')[:10]
        cache.add(MEMCACHE_GREETINGS, greetings)
    if story is None:
        story = Story.objects.all().order_by('-date')[:1]
    imageList = []
    numImages = 48
    i = 0
    while i < numImages:
        imageList.append('http://robohash.org/karie' +str(i)+ 'fury.png')
        i += 1
    return direct_to_template(request, 'atlas/index.html',
                              {'greetings': greetings,
                               'form': CreateGreetingForm(),
                               'imageList': imageList } )

def create_greeting(request):
    if request.method == 'POST':
        form = CreateGreetingForm(request.POST)
        if form.is_valid():
            greeting = form.save(commit=False)
            if request.user.is_authenticated():
                greeting.author = request.user
            greeting.save()
            cache.delete(MEMCACHE_GREETINGS)
    return HttpResponseRedirect('/atlas/')

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

def PhysicalModelView(request,terms):
    # print terms

    queryPhrase = KeywordPhrase()
    queryPhrase.color = "keyWord"
    queryPhrase.title = "title"
    queryPhrase.phrase = terms
    queryPhrase.save()

    searchResults = []
    searchResults.append( searchclient.instructablesSearch( queryPhrase, 3 ) )
    searchResults.append( searchclient.searchThingiverse( queryPhrase, 3 ) )
    searchResults.append( searchclient.searchEtsy( queryPhrase, 3 ) )
    for each in searchResults:
        # Check and see if already in db..
        for item in each:
            newRealObject = RealObject()
            newRealObject.image = item.image
            newRealObject.name = item.name
            newRealObject.phrase = queryPhrase
            newRealObject.source = item.source
            newRealObject.url = item.url
            newRealObject.save()
    response_data = {}
    response_data['images'] = []
    for each in searchResults:
        for item in each:
            response_data['images'].append(item.image)

    response_data['message'] = 'From Django, transmission is working...'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def Stories(request):
    # print terms
    greetings = cache.get(MEMCACHE_GREETINGS)
    if greetings is None:
        greetings = Greeting.objects.all().order_by('-date')[:10]
        cache.add(MEMCACHE_GREETINGS, greetings)

    response_data = {}
    response_data['greeting'] = []
    for each in greetings:
        response_data['greeting'].append(each.content)
    response_data['message'] = 'From Django, transmission is working...'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


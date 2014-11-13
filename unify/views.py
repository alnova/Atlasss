import json

from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from atlas.forms import *
from atlas.models import *

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
    page = 'unify/index.html'
    # return normal index page ( write mode...)
    return direct_to_template(request, page , {} )


def create_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/unify/')
    else:
        form = UserCreationForm()
    return direct_to_template(request, 'unify/user_create_form.html',
        {'form': form})


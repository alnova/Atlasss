from django.conf.urls.defaults import *

urlpatterns = patterns('atlas.views',
    (r'^$', 'list_greetings'),
    (r'^sign$', 'create_greeting'),
    (r'^model/(?P<terms>[A-z]+)/$', 'PhysicalModelView'),
    (r'^json/stories/$', 'Stories'),
)

import os
from django.conf.urls.defaults import *
from django.contrib.auth.forms import AuthenticationForm

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',

    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/unify/', }),
    (r'^unify/', include('unify.urls')),
    #(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/atlas/', }),
    (r'^atlas/', include('atlas.urls')),
    url(r'^unify/assets/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'templates/unify/assets/')}),
    (r'^accounts/create_user/$', 'atlas.views.create_new_user'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'atlas/login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/atlas/',}),
)

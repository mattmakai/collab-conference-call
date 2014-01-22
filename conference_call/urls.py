from django.conf.urls import patterns, url

urlpatterns = patterns('conference_call.views',
    url(r'^$', 'selection', name='selections'),
    url(r'add-participant/$', 'add_participant', name='add_participant'),
    url(r'^dial/$', 'dial', name='dial'),
    url(r'^postback/$', 'conference_postback', name='postback'),
)

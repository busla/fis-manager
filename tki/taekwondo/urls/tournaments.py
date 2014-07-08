from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from taekwondo.views import ClubList, ClubDetail, NewsList, NewsDetail, TournamentList, TournamentDetail
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^(?P<slug>[-_\w]+)/$', ClubDetail.as_view(), name='club-detail'),
    url(r'^$', TournamentList.as_view(), name='tournament_list'),
    url(r'^(?P<slug>[-_\w]+)/$', TournamentDetail.as_view(), name='tournament_detail'),
)
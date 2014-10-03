from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from taekwondo.views import *
from django.contrib import admin
admin.autodiscover()
'''
urlpatterns = patterns('taekwondo.views',
    url(r'^$', 'api_root'),
    url(r'^idkendur/$', ApiMemberList.as_view()),
    url(r'^idkendur/(?P<slug>[-_\w]+)/$', ApiMemberDetail.as_view()),
    url(r'^felog/$', ApiClubList.as_view()),
    url(r'^felog/(?P<slug>[-_\w]+)/$', ApiClubDetail.as_view()),
)
'''
urlpatterns = patterns('taekwondo.views',
    url(r'^$', 'api_root'),
    url(r'^mot/$', ApiTournamentList.as_view(), name='tournament-list'),
    url(r'^mot/(?P<pk>[0-9]+)/$', ApiTournamentDetail.as_view(), name='tournament-detail'),
    url(r'^idkendur/$', ApiMemberList.as_view(), name='member-list'),
    url(r'^idkendur/(?P<pk>[0-9]+)/$', ApiMemberDetail.as_view(), name='member-detail'),
    url(r'^bardagar/$', ApiFightList.as_view(), name='fight-list'),
    url(r'^bardagar/(?P<pk>[0-9]+)/$', ApiFightDetail.as_view(), name='fight-detail'),
    url(r'^felog/$', ApiClubList.as_view(), name='club-list'),
    url(r'^felog/(?P<pk>[0-9]+)/$', ApiClubDetail.as_view(), name='club-detail'),
    url(r'^beltagradur/$', ApiGradeRequirementList.as_view(), name='graderequirement-list'),
    url(r'^beltagradur/(?P<pk>[0-9]+)/$', ApiGradeRequirementDetail.as_view(), name='graderequirement-detail'),
    #url(r'^beltagradur/(?P<pk>[0-9]+)/(?P<grade>[0-9]+)/$', ApiGradeRequirementItemDetail.as_view(), name='graderequirementitem-detail'),
)

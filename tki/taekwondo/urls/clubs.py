from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from taekwondo.views import ClubList, ClubDetail
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^(?P<slug>[-_\w]+)/$', ClubDetail.as_view(), name='club-detail'),
    url(r'^$', ClubList.as_view(), name='club_list'),
    url(r'^(?P<slug>[-_\w]+)/$', ClubDetail.as_view(), name='club_detail'),
    #url(r'^(?P<slug>[-_\w]+)/beltakrofur/$', GradeList.as_view(), name='grade_list'),
    #url(r'^(?P<slug>[-_\w]+)/beltakrofur/(?P<grade>[-_\w]+)/$', GradeDetail.as_view(), name='grade_detail'),
    
)
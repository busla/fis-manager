from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from taekwondo.views import MemberList, MemberDetail, FightList
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('taekwondo.views',
    url(r'^idkendur/$', 'member_list'),
    url(r'^idkendur/(?P<slug>[-_\w]+)/$', 'member_detail'),
)
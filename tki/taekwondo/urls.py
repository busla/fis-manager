from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from taekwondo import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^news/', include('news.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
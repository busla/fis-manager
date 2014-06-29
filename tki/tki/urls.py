from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from taekwondo import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^felog/', include('taekwondo.urls.clubs')),
    url(r'^frettir/', include('taekwondo.urls.news')),
    url(r'^mot/', include('taekwondo.urls.tournaments')),
    (r'^summernote/', include('django_summernote.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
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

    url(r'^mot/', include('taekwondo.urls.tournaments')),
    url(r'^idkendur/', include('taekwondo.urls.members')),
    url(r'^frettir/', include('zinnia.urls')),
    url(r'^athugasemdir/', include('django.contrib.comments.urls')),
    url(r'^', include('zinnia.urls.capabilities')),
    url(r'^search/', include('zinnia.urls.search')),
    url(r'^sitemap/', include('zinnia.urls.sitemap')),
    url(r'^trackback/', include('zinnia.urls.trackback')),
    url(r'^efni/merkimidar/', include('zinnia.urls.tags')),
    url(r'^efni/efnisveita/', include('zinnia.urls.feeds')),
    url(r'^efni/handahof/', include('zinnia.urls.random')),
    url(r'^efni/pennar/', include('zinnia.urls.authors')),
    url(r'^efni/flokkar/', include('zinnia.urls.categories')),
    url(r'^efni/athugasemdir/', include('zinnia.urls.comments')),
    url(r'^efni/', include('zinnia.urls.entries')),
    url(r'^efni/', include('zinnia.urls.archives')),
    url(r'^efni/', include('zinnia.urls.shortlink')),
    url(r'^efni/', include('zinnia.urls.quick_entry')),
    (r'^summernote/', include('django_summernote.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import RedirectView
from googleappsauth import urls as google_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/admin/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^googleapps/', include(google_urls)),
)
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/admin/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^callback_googleappsauth/', 'googleappsauth.views.callback'),
)
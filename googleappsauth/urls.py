from django.conf.urls import patterns, url

urlpatterns = patterns('googleappsauth.views',
    url(r'^login/$', 'login', name='googleapps-login'),
    url(r'^login_callback/$', 'callback', name='googleapps-callback')
)
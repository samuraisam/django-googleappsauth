#!/usr/bin/env python
# encoding: utf-8
"""
googleappsauth/views.py - 

Created by Axel Schlüter on 2009-12
Copyright (c) 2009, 2010 HUDORA GmbH. All rights reserved.
"""

import types

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
import django.contrib.auth as djauth
import googleappsauth.openid

_google_apps_domain = getattr(settings, 'GOOGLE_APPS_DOMAIN', None)
_google_openid_endpoint = getattr(settings, 'GOOGLE_OPENID_ENDPOINT', None)
_google_openid_realm = getattr(settings, 'GOOGLE_OPENID_REALM', None)
_oauth_consumer_key = getattr(settings, 'GOOGLE_APPS_CONSUMER_KEY', None)
_oauth_consumer_secret = getattr(settings, 'GOOGLE_APPS_CONSUMER_SECRET', None)
_google_api_scope = getattr(settings, 'GOOGLE_API_SCOPE', None)


_login_url = getattr(settings, 'LOGIN_URL', None)

def login(request, redirect_field_name=REDIRECT_FIELD_NAME, redirect_url=None):
    login_domain = None
    # If we go over a post-request came in the Method
    # We assume that the user previously for domain login
    # Has selected. Otherwise, s is a mistake.
    if request.method == 'POST':
        login_domain = request.POST.get('domain')
        if not login_domain:
            raise Http404('invalid or missing login domain!')

    # Otherwise it's a login attempt, so we first determine where
    # After a successful login will be redirected to the app
    # If we have more than one configured Apps domain and yet
    # Was chosen not out of the log-domain POST request then
    # We now show first a selection box for the
    # Desired login to domain.

    else:
        login_domain = None
        if not redirect_url:
            redirect_url = request.REQUEST.get(redirect_field_name)
            if not redirect_url:
                redirect_url =  getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        request.session['redirect_url'] = redirect_url

        # jetzt bauen wir uns die URL fuer den Callback zusammen, unter
        # dem wir von Google aufgerufen werden moechten nach dem Login
        callback_url = request.build_absolute_uri(reverse(callback))
        request.session['callback_url'] = callback_url
        

    # wenn wir mehr als eine Apps-Domain konfiguriert haben und noch 
    # keine Login-Domain aus dem POST-Request ausgewaehlt wurde dann
    # dann zeigen wir jetzt zuerst noch eine Auswahlbox fuer die 
    # gewuenschte Login-Domain an.
    if not login_domain:
        if type(_google_apps_domain) == types.ListType:
            return render_to_response('googleappsauth/domains.html', 
                                      { 'login_url': request.get_full_path(), 'domains': _google_apps_domain})
        else:
            login_domain = _google_apps_domain 

    if not redirect_url:
        redirect_url = request.REQUEST.get(redirect_field_name)
        if not redirect_url:
            redirect_url =  getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        
    request.session['redirect_url'] = redirect_url

    # Now we build us the URL for the callback together, under
    # We want to be called from Google after login
    callback_url = request.build_absolute_uri(reverse(callback))
    request.session['callback_url'] = callback_url

    # Now we have certainly a domain over which we logTo 
    #. To provide compatibility with older versions (where the Settings
    # Parameters 'GOOGLE_OPENID_ENDPOINT' already full endpoint URL
    # Include has domain including login) does not break, we catch are possible
    # Type of error (if the parameter is not precisely matching '% s' contains) from.
    openid_endpoint = _google_openid_endpoint
    try:
        openid_endpoint = openid_endpoint % login_domain
    except TypeError:
        pass

    # And finally we build out the Google OpenID
    # Endpoint URL to which we then redirect the user
    url = googleappsauth.openid.build_login_url(
            openid_endpoint, _google_openid_realm,
            callback_url, _oauth_consumer_key, _google_api_scope)
    return HttpResponseRedirect(url)


def callback(request):
    # We have a successful login? If we do not go
    # Back immediately, without a user login
    callback_url = request.session.get('callback_url', '/')
    identifier = googleappsauth.openid.parse_login_response(request, callback_url)
    if not identifier:
        # TODO: was ist hier los?
        return HttpResponseRedirect('/')
    
    # Now we get the remaining data from the login
    attributes = {
        'email': googleappsauth.openid.get_email(request),
        'language': googleappsauth.openid.get_language(request),
        'firstname': googleappsauth.openid.get_firstname(request),
        'lastname': googleappsauth.openid.get_lastname(request)}


    # If we do get an OAuth request token we
    # Now it still afloat an access token
    request_token = googleappsauth.openid.get_oauth_request_token(request)
    #if request_token:
    #    attributes['access_token'] = None
    #    raise Exception('access token handling not yet implemented!')
    
    # Finally, we report the user and its attributes on
    # Of Django auth system, then back to the actual app
    redirect_url = request.session['redirect_url']
    
    domain = _is_valid_domain(googleappsauth.openid.get_email(request))

    if domain:
        
        user = djauth.authenticate(attributes=attributes)
        if not user:
            # For some reason I do not fully understand we get back a "None"" coasionalty - retry.
            user = djauth.authenticate(identifier=username, attributes=attributes)
            if not user:
                # die Authentifizierung ist gescheitert
                raise RuntimeError("Authentication Error: %s|%s|%s" % (username, identifier, attributes))
                
        djauth.login(request, user)
        request.session.set_expiry(300)
        return HttpResponseRedirect(redirect_url)
    
    else:
        return HttpResponseRedirect("/error-googleappsauth")
    

def logout(request):
    djauth.logout(request)
    del request.session['last_touch']
    del request.session['redirect_url']
    return HttpResponseRedirect('https://www.google.com/a/%s/Logout' % _google_apps_domain)

def login_error(request):
    return render_to_response('googleappsauth/login_error.html')

def _is_valid_domain(email):
    print email, _google_apps_domain
    domain = email.split("@")[1]
    if domain in _google_apps_domain:
        return True
    else:
        return False
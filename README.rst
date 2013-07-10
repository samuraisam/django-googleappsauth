====================================================
Authentication agains Google Apps Domains for Django
====================================================

*googleappsauth* allows you to authenticate your `Django <http://www.djangoproject.com/>`_  users
against an Google `Apps <http://www.google.com/apps/>`_ domain.
This means you basically get a single sign-on solution, provided that all users of your django application
also have Accounts in Google Apps for your Domain.


Usage
=====

To use googleappsauth, configuration in `settings.py` should look like this::

    GOOGLE_APPS_DOMAIN = 'example.com'
    GOOGLE_APPS_CONSUMER_KEY = 'example.com'
    GOOGLE_APPS_CONSUMER_SECRET = '*sekret*'
    # domain where your application is running
    GOOGLE_OPENID_REALM = 'http://*.hudora.biz/'
	GOOGLE_OPENID_ENDPOINT = 'https://www.google.com/accounts/o8/ud'

If you want to choose from a list of Google apps domains on a login-by-login basis
you can configure an array of apps domains::

    GOOGLE_APPS_DOMAIN = ['example.com', 'foobar.com', 'carcdr.de']

You also can tell googleappsauth where to go after successfull authentication, in case
the redirect_url had not been set. `LOGIN_REDIRECT_URL` defaults to `/`.
::

    LOGIN_REDIRECT_URL = '/admin'

To activate googleappsauth, set the appropriate Authentication backend and include a callback view.
::

    settings.py:
    AUTHENTICATION_BACKENDS = ('googleappsauth.backends.GoogleAuthBackend',)
    
    urls.py:
    (r'^callback_googleappsauth/', 'googleappsauth.views.callback'),


Using a special middleware which is included in the package, you can block access to a compete site.
::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'googleappsauth.middleware.GoogleAuthMiddleware',
    )

In addition you can set `AUTH_PROTECTED_AREAS` to authenticate only access to certain parts of a site, e.g.
::

    AUTH_PROTECTED_AREAS = ['/admin']
    
If you wish, you can add `AUTH_EXCLUDED_AREAS` to remove authentication from sub-folders of your protected areas, e.g.
::

    AUTH_EXCLUDED_AREAS = ['/admin/public']

Download
========

Get it at the `Python Cheeseshop <http://pypi.python.org/pypi/googleappsauth/>`_ or at
`GitHub <http://github.com/hudora/django-googleappsauth>`_.

See also
========

 * Tim Garthwaite: `Google Apps Auth Backend for Django <http://techblog.appirio.com/2008/10/google-apps-auth-backend-for-django.html>`_
 * http://github.com/flashingpumpkin/django-socialregistration/
 * http://github.com/uswaretech/Django-Socialauth/
 * http://bitbucket.org/benoitc/django-authopenid/
 * http://djangosnippets.org/snippets/913/
 * http://pkropf.blogspot.com/2009/05/django-google-apps-authentication.html
 * http://github.com/adieu/python-openid/ - patched for Google Apps

Notes
-----

You might need to enable the OAuth+OpenID support in your Google Apps domain
at http://www.google.com/a/cpanel/<your-domain>/SetupIdp

You might need to register at http://code.google.com/apis/accounts/docs/RegistrationForWebAppsAuto.html
Might look like this: http://static.23.nu/md/Pictures/ZZ6F76B85B.png

If google claims "invalid page" check GOOGLE_OPENID_REALM.

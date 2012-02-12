import os, platform

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3' 
DATABASE_NAME = 'test.db'

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

MEDIA_URL = '/media'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'a1wyygkm7g&6u3xx47ohe&4yh^47w39wr0$73jq9_y*59-=mt&'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'googleappsauth.middleware.GoogleAuthMiddleware', #Google Apps Auth Testing
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

LOGIN_REDIRECT_URL = '/admin'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
)

#Google Apps Auth Settings
GOOGLE_APPS_DOMAIN = 'example.com'
GOOGLE_APPS_CONSUMER_KEY = 'example.com'
GOOGLE_APPS_CONSUMER_SECRET = '*sekret*'
GOOGLE_OPENID_REALM = 'http://localhost:8000/'
GOOGLE_OPENID_ENDPOINT = 'https://www.google.com/a/%s/o8/ud?be=o8' % GOOGLE_APPS_DOMAIN
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend','googleappsauth.backends.GoogleAuthBackend',)
AUTH_PROTECTED_AREAS = ['/admin']
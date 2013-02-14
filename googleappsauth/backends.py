#!/usr/bin/env python
# encoding: utf-8
"""
googleauth/backends.py - Django authentication backend connecting to Google Apps

Created by Axel Schlüter on 2009-12
Copyright (c) 2009 HUDORA GmbH. All rights reserved.
"""

from datetime import datetime
from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Group, SiteProfileNotAvailable
from django.contrib.contenttypes.models import ContentType
from django.db import models
import re

# from googleappsauth.utils import _apps_domain


class GoogleAuthBackend(ModelBackend):
    def authenticate(self, identifier=None, attributes=None):
        # Because we get a user name of Google we first try
        # To accept the first part of the email address. If we do not have email
        # Then only remains of the OpenID identifier as the username
        email = attributes.get('email', '')
        username = email
        
        users = User.objects.filter(username=username)
        if len(users) > 1:
            raise RuntimeError("duplicate user %s" % email)
        elif len(users) < 1:
            # only allow users under our domain

            # for some reason it seems this code branch is never executed ?!?
            user = User.objects.create(email=email, username=username)
            # fuer einen neuen Benutzer erzeugen wir hier ein Zufallspasswort,
            # sodass er sich nicht mehr anders als ueber Google Apps einloggen kann
            user.set_unusable_password()
            # note creation in log
            LogEntry.objects.log_action(1, ContentType.objects.get_for_model(User).id,
                                    user.id, unicode(User),
                                    ADDITION, "durch googleauth automatisch erzeugt")
             
        else:
            user = users[0]
        # jetzt aktualisieren wir die Attribute des Benutzers mit den neuesten 
        # Werten von Google, falls sich da was geaendert haben sollte
        user.first_name = attributes.get('firstname')
        user.last_name = attributes.get('lastname')
        user.username = username
        user.is_staff = True
        if not user.password:
            user.set_unusable_password()
            
        user.save()
        
        # schliesslich speichern wir das Access Token des Benutzers in seinem
        # User Profile.
        try:
            profile = self._get_or_create_user_profile(user)
            profile.language = attributes.get('language')
            profile.access_token = attributes.get('access_token', '')
            profile.save()
        except SiteProfileNotAvailable:
            pass
        
        return user

    def set_group(self, username):
        domain = email.split('@')[1]

        try:
            group = Group.object.get(name = domain)
        except DoesNotExist:
            group = Group(name = domain)
            group.save()
        
        users = User.objects.filter(username=username)
        users.groups.add(group)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _get_or_create_user_profile(self, user):
        profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', False)
        if not profile_module:
            raise SiteProfileNotAvailable
        app_label, model_name = profile_module.split('.')
        model = models.get_model(app_label, model_name)
        try: 
            return user.get_profile()
        except model.DoesNotExist:
            profile = model()
            profile.user = user
            return profile

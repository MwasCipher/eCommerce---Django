# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from analytics.models import ObjectViewed, UserSession

admin.site.register(ObjectViewed)

admin.site.register(UserSession)
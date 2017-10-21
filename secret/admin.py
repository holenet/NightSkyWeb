# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from secret.models import Log, Watch, Piece

admin.site.register(Log)
admin.site.register(Piece)
admin.site.register(Watch)

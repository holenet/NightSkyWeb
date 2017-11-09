# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from judge.models import Problem, Submission

admin.site.register(Problem)
admin.site.register(Submission)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from django.utils import timezone


class Problem(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    title = models.TextField()
    testcase = models.IntegerField()

    def __unicode__(self):
        return u'%s' % self.title


def file_path(instance, filename):
    return os.path.join('Judge', filename)


class Submission(models.Model):
    submitted_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User')
    problem = models.ForeignKey('judge.Problem', related_name='submissions')
    code_file = models.FileField(upload_to=file_path)
    status = models.TextField()

    def __unicode__(self):
        return u'%s-%d-%s' % (self.problem, self.pk, self.author)

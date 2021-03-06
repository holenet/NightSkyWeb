# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from django.utils import timezone


def weekday_to_str(wd):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][wd]


def image_path(instance, filename):
    return os.path.join('NightSky', 'secret', 'image', instance.author.username, filename)


class Log(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)
    author = models.ForeignKey('auth.User')
    type = models.TextField()
    text = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to=image_path)
    watch = models.ForeignKey('secret.Watch', related_name='logs', on_delete=models.DO_NOTHING, null=True)

    def __unicode__(self):
        return u'%d [%s] -%s' % (self.id, self.type, self.created_at)

    def notify_modified(self):
        self.modified_at = timezone.now()

    def created_at_with_weekday(self):
        return u'%s [%s]' % (self.created_at.date(), weekday_to_str(self.created_at.weekday()))


class Piece(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.TextField()
    comment = models.TextField(default='', blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    def started_at(self):
        if self.watches.count()>0:
            return self.watches.order_by('date')[0].date
        return None

    def ended_at(self):
        if self.watches.count()>0:
            return self.watches.order_by('-date')[0].date
        return None

    def get_count_watch(self):
        count = []
        for watch in self.watches.order_by('-end'):
            if watch.etc is not None:
                continue
            s = watch.start
            e = watch.end
            if len(count)<=e:
                count += [0]*(e-len(count)+1)
            for i in range(s, e+1):
                count[i] += 1
        return count


class Watch(models.Model):
    author = models.ForeignKey('auth.User')
    piece = models.ForeignKey('secret.Piece', related_name='watches', on_delete=models.SET_NULL, null=True)
    start = models.PositiveSmallIntegerField(null=True, blank=True)
    end = models.PositiveSmallIntegerField(null=True, blank=True)
    etc = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        if self.etc is not None:
            return u'%s [%s]' % (self.piece, self.etc)
        elif self.start==self.end:
            return u'%s [%d]' % (self.piece, self.start)
        else:
            return u'%s [%d-%d]' % (self.piece, self.start, self.end)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes
import os
import urllib
from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import dateparse, timezone

from secret.forms import TextLogForm, ImageLogForm, PieceForm, PieceCommentForm, WatchEditForm, WatchAddForm
from secret.models import Log, Piece, Watch


class HttpSuccess(HttpResponse):
    def __init__(self, pk=None):
        if pk:
            super(HttpSuccess, self).__init__('Success '+str(pk))
        else:
            super(HttpSuccess, self).__init__('Success')


def log_to_dict(log):
    item = dict(pk=log.pk, type=log.type, created_at=log.created_at, modified_at=log.modified_at, watch_pk=log.watch_id)
    if log.type == 'text':
        item.update(dict(text=log.text))
    elif log.type == 'image':
        item.update(dict(image_path=log.image.name))
    return item


@login_required
def log_list(request, date):
    if date is not None:
        try:
            date = dateparse.parse_date(date)
        except ValueError as ve:
            print(ve)
            raise Http404()
    if date is None:
        logs = Log.objects.filter(author=request.user).order_by('created_at')
    else:
        logs = Log.objects.filter(author=request.user, created_at__contains=date).order_by('created_at')
    data = []
    for log in logs:
        data.append(log_to_dict(log))
    return JsonResponse(data, safe=False)


@login_required
def log_date_list(request):
    dates = set()
    for log in Log.objects.filter(author=request.user):
        dates.add(log.created_at_with_weekday())
    return JsonResponse(sorted(list(dates)), safe=False)


@login_required
def log_new_text(request):
    if request.method == 'POST':
        form = TextLogForm(request.POST)
        if form.is_valid():
            text_log = form.save(commit=False)
            text_log.author = request.user
            text_log.type = 'text'
            text_log.save()
            return JsonResponse(log_to_dict(text_log), safe=False)
    else:
        form = TextLogForm()
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def log_new_image(request):
    if request.method == 'POST':
        form = ImageLogForm(request.POST, request.FILES)
        if form.is_valid():
            image_log = form.save(commit=False)
            image_log.author = request.user
            image_log.type = 'image'
            image_log.save()
            return JsonResponse(log_to_dict(image_log), safe=False)
    else:
        form = ImageLogForm()
    return render(request, 'secret/file_upload.html', {'form': form})


@login_required
def log_edit_text(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk, type='text', author=request.user)
    if request.method == 'POST':
        form = TextLogForm(request.POST, instance=log)
        if form.is_valid():
            log = form.save(commit=False)
            print(log.pk)
            log.pk = log_pk
            print(log_pk)
            log.notify_modified()
            log.save()
            return HttpSuccess()
    else:
        form = TextLogForm(instance=log)
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def log_delete(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk, author=request.user)
    if log.watch:
        log.watch.delete()
    if log.type == 'image':
        path = log.image.path
        try:
            os.remove(path)
        except Exception as e:
            print(e)
    log.delete()
    return HttpSuccess(pk=log_pk)


@login_required
def log_download_image(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk, type='image', author=request.user)
    image_name = os.path.basename(log.image.name)
    image_path = log.image.path
    wrapper = FileWrapper(file(image_path, 'rb'))
    mimetype = mimetypes.guess_type(image_path)
    response = HttpResponse(wrapper, content_type=mimetype)
    response['X-Sendfile'] = image_path
    response['Content-Length'] = os.stat(image_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % urllib.quote(image_name.encode('utf-8'))
    return response


@login_required
def log_cut_watch(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk, author=request.user)
    log.watch = None
    log.save()
    return JsonResponse(log_to_dict(log), safe=False)


def piece_to_dict(piece):
    info = dict(
        pk=piece.pk,
        title=piece.title,
        comment=piece.comment,
        watchs=[dict(start=watch.start, end=watch.end) if watch.etc is None else dict(etc=watch.etc) for watch in piece.watches.all()],
        counts=piece.get_count_watch(),
    )
    started = piece.started_at()
    if started:
        info['started_at'] = started
    ended = piece.ended_at()
    if ended:
        info['ended_at'] = ended
    return info


@login_required
def piece_list(request):
    pieces = Piece.objects.filter(author=request.user)
    pieces = sorted(pieces, key=lambda x: x.started_at() if x.started_at() else timezone.now(), reverse=True)
    data = []
    for piece in pieces:
        data.append(piece_to_dict(piece))
    return JsonResponse(data, safe=False)


@login_required
def piece_new(request):
    if request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            piece = form.save(commit=False)
            piece.author = request.user
            piece.save()
            return JsonResponse(piece_to_dict(piece), safe=False)
    else:
        form = PieceForm()
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def piece_edit(request, piece_pk):
    piece = get_object_or_404(Piece, pk=piece_pk, author=request.user)
    if request.method == 'POST':
        form = PieceForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return HttpSuccess()
    else:
        form = PieceForm(instance=piece)
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def piece_comment_edit(request, piece_pk):
    piece = get_object_or_404(Piece, pk=piece_pk, author=request.user)
    if request.method == 'POST':
        form = PieceCommentForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return HttpSuccess()
    else:
        form = PieceCommentForm(instance=piece)
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def piece_delete(request, piece_pk):
    piece = get_object_or_404(Piece, pk=piece_pk, author=request.user)
    piece.delete()
    return HttpSuccess()


def watch_to_dict(watch):
    info = dict(
        pk=watch.pk,
        piece_pk=watch.piece_id,
        date=watch.date,
        logs=[dict(pk=log.pk, summary=str(log)) for log in watch.logs.all()],
    )
    if watch.etc is None:
        info.update(dict(start=watch.start, end=watch.end))
    else:
        info.update(etc=watch.etc)
    return info


@login_required
def watch_list(request, piece_pk):
    if piece_pk:
        piece = get_object_or_404(Piece, pk=piece_pk, author=request.user)
        watches = piece.watches.order_by('date')
    else:
        watches = Watch.objects.filter(author=request.user).order_by('-date')
    data = []
    for watch in watches:
        data.append(watch_to_dict(watch))
    return JsonResponse(data, safe=False)


@login_required
def watch_new(request):
    if request.method == 'POST':
        form = WatchEditForm(request.POST)
        if form.is_valid():
            watch = form.save(commit=False)
            watch.author = request.user
            watch.piece = form.cleaned_data['piece']
            if watch.etc=='':
                watch.etc = None
            watch.save()
            for log in form.cleaned_data['logs']:
                log.watch = watch
                log.save()
            return JsonResponse(watch_to_dict(watch), safe=False)
    else:
        form = WatchEditForm()
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def watch_edit(request, watch_pk):
    watch = get_object_or_404(Watch, pk=watch_pk, author=request.user)
    if request.method == 'POST':
        form = WatchEditForm(request.POST, instance=watch)
        if form.is_valid():
            watch = form.save(commit=False)
            watch.piece = form.cleaned_data['piece']
            if watch.etc=='':
                watch.etc = None
            watch.save()
            for log in form.cleaned_data['logs']:
                log.watch = watch
                log.save()
            return JsonResponse(watch_to_dict(watch), safe=False)
    else:
        form = WatchEditForm(instance=watch)
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def watch_add_logs(request, watch_pk):
    watch = get_object_or_404(Watch, pk=watch_pk, author=request.user)
    if request.method == 'POST':
        form = WatchAddForm(request.POST)
        if form.is_valid():
            for log in form.cleaned_data['logs']:
                log.watch = watch
                log.save()
            return JsonResponse(watch_to_dict(watch), safe=False)
    else:
        form = WatchAddForm()
    return render(request, 'secret/standard_edit.html', {'form': form})


@login_required
def watch_delete(request, watch_pk):
    watch = get_object_or_404(Watch, pk=watch_pk, author=request.user)
    for log in watch.logs:
        log.watch = None
        log.save()
    watch.delete()
    return HttpSuccess()

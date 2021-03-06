from django.conf.urls import url
from . import views

app_name = 'secret'
urlpatterns = [
    url(r'^log/list/((?P<date>[0-9\-]{8,10})/)?$', views.log_list, name='log_list'),
    url(r'^log/date/list/$', views.log_date_list, name='log_list'),
    url(r'^log/new/text/$', views.log_new_text, name='log_new_text'),
    url(r'^log/new/image/$', views.log_new_image, name='log_new_image'),
    url(r'^log/edit/text/(?P<log_pk>[0-9]+)/$', views.log_edit_text, name='log_edit_text'),
    url(r'^log/delete/(?P<log_pk>[0-9]+)/$', views.log_delete, name='log_delete'),
    url(r'^log/download/image/(?P<log_pk>[0-9]+)/$', views.log_download_image, name='log_download_image'),
    url(r'^log/cut/watch/(?P<log_pk>[0-9]+)/$', views.log_cut_watch, name='log_cut_watch'),

    url(r'^piece/list/$', views.piece_list, name='piece_list'),
    url(r'^piece/new/$', views.piece_new, name='piece_new'),
    url(r'^piece/edit/(?P<piece_pk>[0-9]+)/$', views.piece_edit, name='piece_edit'),
    url(r'^piece/comment/edit/(?P<piece_pk>[0-9]+)/$', views.piece_comment_edit, name='piece_comment_edit'),
    url(r'^piece/delete/(?P<piece_pk>[0-9]+)/$', views.piece_delete, name='piece_delete'),

    url(r'^watch/list/((?P<piece_pk>[0-9]+)/)?$', views.watch_list, name='watch_list'),
    url(r'^watch/new/$', views.watch_new, name='watch_new'),
    url(r'^watch/edit/(?P<watch_pk>[0-9]+)/$', views.watch_edit, name='watch_edit'),
    url(r'^watch/add/logs/(?P<watch_pk>[0-9]+)/$', views.watch_add_logs, name='watch_add_logs'),
    url(r'^watch/delete/(?P<watch_pk>[0-9]+)/$', views.watch_delete, name='watch_delete'),
]

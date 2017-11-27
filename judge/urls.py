from django.conf.urls import url
from . import views

app_name = 'judge'
urlpatterns = [
    url(r'^$', views.problem_list, name='problem_list'),
    url(r'^problem/new/$', views.problem_new, name='problem_new'),
    url(r'^problem/(?P<problem_pk>[0-9]+)/testcase/add$', views.add_testcase, name='add_testcase'),
    url(r'^problem/(?P<problem_pk>[0-9]+)/testcase/list', views.testcase_list, name='testcase_list'),
    url(r'^problem/(?P<problem_pk>[0-9]+)/testcase/(?P<testcase_index>[0-9]+)/$', views.testcase_detail, name='testcase_detail'),
    url(r'^problem/(?P<problem_pk>[0-9]+)/testcase/(?P<file_name>[a-z0-9\\.]+)/$', views.testcase_download, name='testcase_download'),

    url(r'^submit/(?P<problem_pk>[0-9]+)/$', views.submit, name='submit'),
    url(r'^submission/status/(?P<submission_pk>[0-9]+)/$', views.submission_status, name='submission_status'),
    url(r'^submission/status/(?P<submission_pk>[0-9]+)/ajax/$', views.submission_status_ajax, name='submission_status_ajax')
]

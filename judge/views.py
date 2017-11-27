# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes

import re

import os
import urllib
from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from judge.forms import SubmitForm, ProblemForm, TestcaseAddForm
from judge.models import Problem, Submission

JUDGE_ROOT = os.path.join(settings.MEDIA_ROOT, 'Judge')


@login_required
def problem_list(request):
    problems = Problem.objects.order_by('-created_at')
    return render(request, 'judge/problem_list.html', {'problems': problems})


@login_required
def problem_new(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = Problem()
            problem.title = form.cleaned_data['title']
            testcases = form.files.getlist('testcases')
            problem.testcase = len(testcases)/2
            problem.save()
            tc = JUDGE_ROOT+'/testcase/{}'.format(problem.pk)
            if not os.path.exists(tc):
                os.makedirs(tc)
            for f in testcases:
                with open('{}/{}'.format(tc, f.name), 'wb+') as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
            return redirect('judge:problem_list')
    else:
        form = ProblemForm()
    return render(request, 'judge/problem_new.html', {'form': form})


@login_required
def add_testcase(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    if request.method == 'POST':
        form = TestcaseAddForm(request.POST, request.FILES)
        if form.is_valid():
            testcases = form.files.getlist('testcases')
            problem.testcase += len(testcases)
            problem.save()
            tc = JUDGE_ROOT+'/testcase/{}'.format(problem.pk)
            if not os.path.exists(tc):
                os.makedirs(tc)
            for f in testcases:
                with open('{}/{}'.format(tc, f.name), 'wb+') as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
            return redirect('judge:problem_list')
    else:
        form = TestcaseAddForm()
    return render(request, 'judge/add_testcase.html', {'problem': problem, 'form': form})


@login_required
def testcase_list(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    mx = -1
    for x in os.listdir(JUDGE_ROOT+'/testcase/{}'.format(problem_pk)):
        if 'input' in x or 'output' in x:
            index = x[5 if 'input' in x else 6:-4]
            mx = max(mx, int(index))
    indices = [i for i in range(0, mx+1)]
    return render(request, 'judge/testcase_list.html', {'problem': problem, 'indices': indices})


@login_required
def testcase_detail(request, problem_pk, testcase_index):
    problem = get_object_or_404(Problem, pk=problem_pk)
    try:
        input_txt = open(JUDGE_ROOT+'/testcase/{}/input{}.txt'.format(problem_pk, testcase_index), 'r')
        output_txt = open(JUDGE_ROOT+'/testcase/{}/output{}.txt'.format(problem_pk, testcase_index), 'r')
    except Exception as e:
        print(e)
        raise Http404()
    max_text = 1000

    input_str = ''
    while True:
        line = input_txt.readline()
        if line=='':
            break
        input_str += line
        if len(input_str)>max_text:
            input_str = input_str[:max_text]+'\n....'
            break
    input_txt.close()

    output_str = ''
    while True:
        line = output_txt.readline()
        if line=='':
            break
        output_str += line
        if len(output_str)>max_text:
            output_str = output_str[:max_text]+'\n....'
            break
    output_txt.close()

    context = {'problem': problem, 'testcase_index': testcase_index,
               'input': input_str, 'output': output_str,
               'input_file': 'input{}.txt'.format(testcase_index),
               'output_file': 'output{}.txt'.format(testcase_index),
               }
    return render(request, 'judge/testcase_detail.html', context)


@login_required
def testcase_download(request, problem_pk, file_name):
    get_object_or_404(Problem, pk=problem_pk)
    file_path = JUDGE_ROOT+'/testcase/{}/{}'.format(problem_pk, file_name)
    try:
        io_file = open(file_path, 'r')
    except Exception as e:
        print(e)
        raise Http404()
    file_name = os.path.basename(io_file.name)
    file_wrapper = FileWrapper(file(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s'%urllib.quote(file_name.encode('utf-8'))
    return response


@login_required
def submit(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.author = request.user
            submission.problem = problem
            submission.save()

            tc = JUDGE_ROOT+'/testcase/{}'.format(problem.pk)
            an = JUDGE_ROOT+'/answer/{}'.format(submission.pk)
            rs = JUDGE_ROOT+'/result'
            if not os.path.exists(an):
                os.makedirs(an)
            if not os.path.exists(rs):
                os.makedirs(rs)
            os.system('python3 {root}/check.py {jar} {pk} {testcase} {tc} {an} {rs} &'
                    .format(root=os.path.join(settings.BASE_DIR, 'judge'),
                            jar=submission.code_file.path,
                            pk=submission.pk,
                            testcase=problem.testcase,
                            tc=tc, an=an, rs=rs,
                    )
            )

            return redirect('judge:submission_status', submission_pk=submission.pk)
    else:
        form = SubmitForm()
    return render(request, 'judge/submit.html', {'problem': problem, 'form': form})


@login_required
def submission_status(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk, author=request.user)
    try:
        result = open(JUDGE_ROOT+'/result/{}.txt'.format(submission.pk), 'r')
        status = result.readline()
        result.close()
    except Exception as e:
        print(e)
        status = 'Prepare'
    submission.status = status
    print(status)
    submission.save()
    context = dict(problem_pk=submission.problem.pk, submission=submission)
    if 'Wrong' in status or 'Error' in status:
        if len(re.findall(r'\((.*):', status))>0:
            context['wrong'] = re.findall(r'\((.*):', status)[0]
    return render(request, 'judge/submission_status.html', context)


def submission_status_ajax(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    try:
        result = open(JUDGE_ROOT+'/result/{}.txt'.format(submission.pk), 'r')
        status = result.readline()
        result.close()
    except Exception as e:
        print(e)
        status = 'Prepare'
    return HttpResponse(status)

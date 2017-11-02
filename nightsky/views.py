import os
from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render


def register(request):
    if request.user.is_authenticated():
        logout(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cloud:post_list')
            else:
                return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def course_check(request):
    if request.user.username != 'holenet':
        raise Http404()
    image_data = open(settings.STATIC_ROOT+os.path.sep+'check_course.png', "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def course_time(request):
    if request.user.username != 'holenet':
        raise Http404()
    time = open(settings.STATIC_ROOT+os.path.sep+'check_time.txt', "r")
    return time.readline()

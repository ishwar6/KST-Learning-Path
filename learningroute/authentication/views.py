# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import hashlib
import datetime
import smtplib

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/assess/main/')
        else:
            return HttpResponse('You havent registered or password entered is wrong')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/assess/main/')
        else:
            return render(request, 'login.html', {"profile": None})


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('/auth/login/')




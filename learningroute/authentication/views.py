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
            return HttpResponseRedirect('/authentication/main/')
        else:
            return HttpResponse('You havent registered')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/authentication/main/')
        else:
            return render(request, 'login.html', {"profile": None})


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('/authentication/login/')


def index(request):
	global counter, score
	if request.user.is_authenticated:
		pr = User.objects.get(username=request.user)
		#print(pr.first_name)

	#print("counter="+str(counter))

	#print(topics)
		return render(request, 'index.html')
    #return HttpResponse("Hello, world. You're at the main_test index.")
	else:
		return HttpResponse('Some Probem occured')	
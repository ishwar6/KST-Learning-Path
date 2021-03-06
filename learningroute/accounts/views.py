from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, FormView
from .forms import (RegisterForm, LoginForm, VerifyForm,
                    TempRegisterForm, SetPasswordForm)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse, Http404
from learningroute.utils import unique_otp_generator
from django.contrib.auth import get_user_model
import requests
import random
User = get_user_model()
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework import viewsets, response, permissions
from django.views.decorators.csrf import csrf_exempt
from .models import OTP
from profiles.models import LoginDetail

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('account:login')
   



class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('account:profile')
    template_name = 'account/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('assess:initial-assess')
        return super().dispatch(*args, **kwargs)



    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=phone, password=password)

        if user is not None:
            login(request, user)
            login_detail = LoginDetail.objects.filter(user= request.user)
            if login_detail.exists():
                login_detail_obj                 = login_detail.first()
                counts_                          = login_detail_obj.logged_in_count 
                login_detail_obj.logged_in_count = counts_ + 1
                login_detail_obj.save()
                if login_detail_obj.first_count ==0:
                    return redirect('profile:edit')
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)

            else:
                return redirect('content:dashboard')
        return super(LoginView, self).form_invalid(form)


# class TempRegisterView(CreateView):
#     form_class = TempRegisterForm
#     template_name = 'account/phone.html'
#     success_url  = reverse_lazy('account:verify-otp')

#     def form_valid(self, form):
#         request = self.request
#         phone = form.cleaned_data.get('phone')
#         request.session['phone'] = phone
#         return super(TempRegisterView, self).form_valid(form)
@csrf_exempt
def send_otp(request):
    if request.user.is_authenticated:
        return redirect('account:profile')
    
    if request.method == 'POST':
        token = 0
        phone = request.session.get('phone', '6666')
        otp_given_ = OTP.objects.filter(phone = phone)
        print(otp_given_)
        if otp_given_.exists():
            otp_given = otp_given_.first()
            token     = otp_given.match 
        print(token)
        form = TempRegisterForm(request.POST or None)
        if form.is_valid():
            if token == 1:
                print('here token is 0ne')
                return redirect('account:set-password')
        else:
            if token:
                del request.session['token']
            return redirect('account:register')
    else:
        form = TempRegisterForm()
    return render(request, 'account/phone.html', {'form': form})

def register_new(request):
    if request.user.is_authenticated:
        return redirect('account:profile')
    form = TempRegisterForm()
    return render(request, 'account/phone.html', {'form': form})





@csrf_exempt
def validate_phone(request):
    phone = request.GET.get('phone', None)
    data = {
        'is_taken': User.objects.filter(phone__iexact=phone).exists()
    }
    data['phone'] = phone,
    print('working')

    if data['is_taken']:
        data['error_message'] = 'This Phone Number already exists.',
    else:
        request.session['phone'] = phone
        send_activation(request, phone)
    return redirect('account:check-otp')

@csrf_exempt
def send_activation(request, phone):
    phone = request.session.get('phone', '6666')
    key = random.randint(1, 999999)
    previous = OTP.objects.filter(phone = phone)
    if previous.exists():
        previous.first.delete()

    OTP.objects.create(
        phone = phone,
        otp = key
    )
    print('step 1')
    request.session['key'] = key
    
    phone = str(phone)
    key = str(key)
    # link = 'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=26183928-e9fe-11e7-a328-0200cd936042&to=' + \
    #     phone+'&from=HTadka&templatename=Firstlogin&var1='+key
    print(key)
    # result = requests.get(link)
    # end = len(result.text)
    # return result.ok
    return True



def validate_otp(request):
    phone = request.session.get('phone', '6666')
    otp = int(request.GET.get('otp', None))
    otp_given_ = OTP.objects.filter(phone = phone)
    if otp_given_.exists():
        otp_given = otp_given_.first().otp

    data = {
        'matches': False
    }
    if otp == otp_given:
        otp_given_ = OTP.objects.filter(phone = phone)
        if otp_given_.exists():
            otp_given = otp_given_.first()
            otp_given.match = 1
            otp_given.save()
            print('saved 2', otp_given)
        data = {
            'matches': True
        }
    if not data['matches']:
        data['error_message'] = 'This otp is not valid.',
    print(data)
    return JsonResponse(data)


def set_password(request):
    phone = request.session.get('phone', '6666')
    otp_given_ = OTP.objects.filter(phone = phone)
    if otp_given_.exists():
            otp_given = otp_given_.first()
            token     = otp_given.match 
    print(token)
    if token == 1:
        if request.method == 'POST':
            form = SetPasswordForm(request.POST or None)
            if form.is_valid():
                password = form.cleaned_data.get("password")
                password2 = form.cleaned_data.get("password2")
                if password != password2:
                    messages.error(request, 'Password do not match')
                    return redirect('account:set-password')
                else:
                    User.objects.create_user(phone, password)
                    
                    otp_given_ = OTP.objects.filter(phone = phone)
                    if otp_given_.exists():
                        otp_given = otp_given_.first().delete()
            

                    user = authenticate(
                        request, username=phone, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('profile:edit')
                    else:
                        return redirect('account:register')
            else:
                return redirect('account:set-password')
        else:
            form = SetPasswordForm()
    else:
        return redirect('account:register')
    return render(request, 'account/set-password.html', {'form': form})


def profile(request):
    return render(request, 'account/profile.html', {})


def send_otp_password_reset(request):
    if request.user.is_authenticated:
        return redirect('account:profile')
    if request.method == 'POST':
        form = TempRegisterForm(request.POST or None)
        if form.is_valid():
            token = request.session.get('token', None)
            if token:
                messages.error(
                    request, 'Please set new password for your account')
                return redirect('account:reset-password')
        else:
            return redirect('account:password-reset')
    else:
        form = TempRegisterForm()
    return render(request, 'account/password-reset.html', {'form': form})


def validate_phone_reset(request):
    phone = request.GET.get('phone', None)
    data = {
        'is_taken': User.objects.filter(phone__iexact=phone).exists()
    }
    data['phone'] = phone,

    if data['is_taken']:
        data['error_message'] = 'This Phone Number exists and otp has been sent.',
        request.session['phone_reset'] = phone
        send_activation_reset(request, phone)
    else:
        data['error_message'] = 'This Phone Number do not exists.',
    return JsonResponse(data)


def send_activation_reset(request, phone):
    phone = request.session.get('phone_reset', '6666')
    key = random.randint(1, 999999)
    request.session['key_reset'] = key
    phone = str(phone)
    key = str(key)
    link = 'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=26183928-e9fe-11e7-a328-0200cd936042&to=' + \
        phone+'&from=HTadka&templatename=Firstlogin&var1='+key
    print(link)
    result = requests.get(link)
    end = len(result.text)
    return result.ok


def validate_otp_reset(request):
    otp = int(request.GET.get('otp', None))
    otp_given = int(request.session.get('key_reset', '6666'))
    data = {
        'matches': False
    }
    print(otp_given)
    request.session['token'] = False
    if otp == otp_given:
        request.session['token'] = True
        data = {
            'matches': True
        }
    if not data['matches']:
        data['error_message'] = 'This otp is not valid.',
    print(data)
    print(request.session['token'])
    return JsonResponse(data)


def reset_password(request):
    if request.user.is_authenticated:
        return redirect('account:profile')
    token = request.session.get('token', None)
    phone = request.session.get('phone_reset', None)
    if phone and token:
        if request.method == 'POST':
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                user = user.first()
                form = SetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data.get("password")
                    password2 = form.cleaned_data.get("password2")
                    if password != password2:
                        messages.error(request, 'Password do not match')
                        return redirect('account:reset-password')
                    else:
                        user.set_password(password)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(
                            request, 'Your password was successfully updated!')
                        return redirect('account:profile')
        else:
            form = SetPasswordForm()
    else:
        return redirect('account:password-reset')
    return render(request, 'account/set-password.html', {'form': form})
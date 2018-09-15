from django.conf.urls import url, include
from .views import (
    RegisterView,
    LoginView,
    set_password,
    send_otp,
    validate_otp,
    validate_phone,
    profile,
    send_otp_password_reset,
    validate_otp_reset,
    validate_phone_reset,
    reset_password,
    # TempRegisterView
)

app_name = 'account'
urlpatterns = [

    url(r'^register/$', send_otp, name='register'),
    url(r'^password-reset/$', send_otp_password_reset, name='password-reset'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^set-password/$', set_password, name='set-password'),
    url(r'^reset-password/$', reset_password, name='reset-password'),
    url(r'^ajax/validate_otp/$', validate_otp, name='validate-otp'),
    url(r'^ajax/validate_phone/$', validate_phone, name='validate-phone'),
    url(r'^ajax/validate_otp/reset/$',
        validate_otp_reset, name='validate-otp-reset'),
    url(r'^ajax/validate_phone/reset/$',
        validate_phone_reset, name='validate-phone-reset'),
]

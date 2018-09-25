from django.shortcuts import render, redirect
from .models import Profile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['name', 'email', 'standard', 'city']
    template_name = 'profiles/edit.html'
    login_url = reverse_lazy('account:login')
    success_url = reverse_lazy('account:profile')

    
    def get_object(self):
        return Profile.objects.filter(user = self.request.user).first()


    def form_valid(self, form):
        standard = form.cleaned_data['standard']
        a    = Profile.objects.filter(user = self.request.user).first()
        c    = a.count
        if c == 0 and standard is not None:
            a.count = 1
            a.save()
            print('set the class of student')
            user = User.objects.filter(phone = self.request.user.phone).first()
            user.standard = standard
            user.save()
        return super(ProfileUpdate, self).form_valid(form)

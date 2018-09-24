from django.shortcuts import render
from .models import Profile
from django.views.generic.edit import UpdateView
from django.urls    import reverse_lazy

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['name', 'email', 'standard', 'city']
    template_name = 'profiles/edit.html'
    success_url = reverse_lazy('account:profile')



    def get_object(self):
        if not self.request.user.is_authenticated:
            return redirect('account:login')

        return Profile.objects.filter(user = self.request.user).first()
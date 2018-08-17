from django.shortcuts import render

from .models import State
def myview(request):
  return render(request, 'states/states.html', {'q': State.objects.all() })
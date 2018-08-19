from django.shortcuts import render

from .models import State, Node, Edge


def myview(request):
  return render(request, 'states/states.html', {'q': State.objects.all() })


def nodes(request):
    edges =  Edge.objects.all()
    return render(request, 'states/states.html', {'q': Node.objects.all(), 'e': edges })

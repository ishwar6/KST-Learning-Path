from django.shortcuts import render
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

base = importr('base')
utils = importr('utils')
kst = importr('kst')


from .models import State, Node, Edge


def myview(request):
  return render(request, 'states/states.html', {'q': State.objects.all() })


def nodes(request):
    kst = importr('kst')
    edges =  Edge.objects.all()
    n = Node.objects.all()
    r = robjects.r
    set_ = r.set( r.set('a', 'b', 'c'), r.set('a') , r.set('b'), r.set('a', 'd') )
    ks = kst.kstructure(set_)
    print(ks)
    print(kst.kdomain(ks))
    kspace = kst.kspace(ks)
    print(kspace)

#     ksp<-kspace(ks)
# kstructure_is_kspace(ksp)
#
# #now lp have learning path
# lp <-lpath(ksp)



    return render(request, 'states/states.html', {'q': n, 'e': edges })

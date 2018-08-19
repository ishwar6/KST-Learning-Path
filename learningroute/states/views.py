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
    r = robjects.r
    kst = importr('kst')
    r.sets_options('quote', False)
    edges =  Edge.objects.all()
    n = Node.objects.all()
    print(n)



    i = 0
    set = {}
    # making dictionary of individual state_nodes in set variable
    for node in n:
        set[i] = ','.join(str(i.title) for i in node.state_node.all())
        i = i+1
    print(set)
    # r_set = {}
    # #converting the dictionary in R SET's
    # for key, value in set.items():
    #     value = value.replace("{","").replace("}", "")
    #     r_set[key] = r.set(value)


    # converting the python SET's dictionary of sets :- (to) set of set
    a = r.set('')
    for key, value in set.items():

        b = r.set(value)
        a = r.set_union(a, b)
    # making the knowledge space from above set of strings

    ks = kst.kstructure(a)

    # print(ks)
    # print('asdf')
    ksp = kst.kspace(ks)
    print(ksp)
    #print(kst.kdomain(ks))
    print(kst.kstructure_is_kspace(ks))

    #print(kspace)
    lp = kst.lpath(ksp)





    return render(request, 'states/states.html', {'q': n, 'e': edges })

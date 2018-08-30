import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

r= robjects.r
kst= importr('kst')


def node2kstate(node):  # db node -> set(db state)
    
    temp= r.set()
    r.sets_options('quote', False)
    j= 0
    for st in node.state_node.all():
        j=j+1
        if j==1:
            temp= r.set(st)
            continue
        temp= r.set_union(temp, r.set(st))
    
    return temp


def nodes2kstructure(nodes): # queryset(db node) -> kstructure(which is set(set(db state)))
    r.sets_options('quote', False)
    i= 0
    temp_set= r.set()
    for nd in nodes:
        i= i+1
        if i==1:
            temp_set= r.set(node2kstate(nd))
            print(temp_set)
            continue
        temp_set= r.set_union(temp_set, r.set(node2kstate(nd)))
        print(temp_set)
    return kst.kstructure(temp_set)

def num_items_in_domain(kstr): # gives number of states in the domain node
    return kst.domain(kstr)

def number_optimum(num):
    if num<=20:
        return num//3
    elif num in range(20,30):
        return num//4
    elif num in range(30,50):
        return num//6
    elif num>50 & num<100:
        return num//10
    elif num>100:
        return min(num//15, 30)

def outer_fringe(kstr, node):  # gives outer fringe in consumable format
    r.sets_options('quote', False)
    size= node.state_node.all().count()
    kstate= node2kstate(node)
    fringe_outer= list()
    for padosi in kst.kneighbourhood(kstr, r.set(kstate)):
        num_sett=0
        for sett in padosi:
            num_sett= num_sett+ 1
        if num_sett > size:
            fringe_outer.append(kstate_to_node(padosi))
    return fringe_outer


def inner_fringe(kstr, node):  #gives the inner fringe in a consumable format
    r.sets_options('quote', False)
    size= node.state_node.all().count()
    kstate= node2kstate(node)
    fringe_inner= list()
    for padosi in kst.kneighbourhood(kstr, r.set(kstate)):
        num_sett=0
        for sett in padosi:
            num_sett= num_sett+ 1
        if num_sett < size:
            fringe_inner.append(kstate_to_node(padosi))
    return fringe_inner

def kstate_to_node(kstate): # set(db state) -> db node
    list_of_states=list()
    for st in kstate:
        list_of_states.append(st)
    nd= Node.objects.get(state_node=list_of_states)
    return nd

def surplus_state(smaller_node, larger_node):  # db_node1, db_node2 -> db_state(in larger_node which is not present in smaller_node)
    sm= node2kstate(smaller_node)
    lg= node2kstate(larger_node)
    for kitem in r.set_symdiff(r.set(sm), r.set(lg)):
        return kitem

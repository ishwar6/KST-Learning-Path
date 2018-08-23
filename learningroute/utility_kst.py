import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

r= robjects.r
kst= importr('kst')


def node2kstate(node):
    
    temp= r.set()
    r.sets_options('quote', False)
    j= 0
    for st in node.state_node.all():
        j=j+1
        if j==1:
            temp= r.set(st.title)
            continue
        temp= r.set_union(temp, st.title)
    
    return temp


def nodes2kstructure(nodes):
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
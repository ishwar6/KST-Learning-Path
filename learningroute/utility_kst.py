import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from states.models import Node, State

r= robjects.r
kst= importr('kst')


def node2kstate(node):  # db node -> set(db state)
    
    temp= r.set()
    r.sets_options('quote', False)
    j= 0
    for st in node.state_node.all():
        j=j+1
        if j==1:
            temp= r.set(st.id)
            continue
        temp= r.set_union(temp, r.set(st.id))
    
    return temp


def nodes2kstructure(nodes): # queryset(db node) -> kstructure(which is set(set(db state)))
    r.sets_options('quote', False)
    i= 0
    temp_set= r.set()
    for nd in nodes:
        i= i+1
        if i==1:
            temp_set= r.set(node2kstate(nd))
            
            continue
        temp_set= r.set_union(temp_set, r.set(node2kstate(nd)))
        
    return kst.kstructure(temp_set)

def num_items_in_domain(kstr): # gives number of states in the domain node
    return r.length(kst.kdomain(kstr))[0]


def outer_fringe(chap, node):  # gives outer fringe in consumable format
    size= node.state_node.all().count()
    
    fringe_outer= list()
    ch_nodes= Node.objects.filter(state_node__topic__chapter__title=chap).distinct()  # take all nodes E chapter
    for nd in ch_nodes:
        if nd.state_node.all().count()== size+1:  # select ony those whos state count is one more than curr nodes state count
            a_match=1
            for st_curr in node.state_node.all():     # check whether every state E curr_node in potential next_node
                st_matches=0
                for st_next in nd.state_node.all():
                    if st_curr.id == st_next.id:
                        st_matches=1
                if st_matches== 0:
                    a_match=0
            if a_match ==1:
                fringe_outer.append(nd)
    '''neigh= kst.kneighbourhood(kstr, r.set(kstate))
    print("inside of funcn")
    print(str(neigh))
    for padosi in neigh:
    
        num_sett=0
        for sett in padosi:
            num_sett= num_sett+ 1
        if num_sett > size:
            fringe_outer.append(kstate_to_node(padosi))
    '''
    return fringe_outer


def inner_fringe(chap, node):  #gives the inner fringe in a consumable format
    r.sets_options('quote', False)
    print("node is "+str(node)) #################################################
    size= node.state_node.all().count()
    fringe_inner= list()
    ch_nodes= Node.objects.filter(state_node__topic__chapter__title=chap).distinct()  # take all nodes E chapter
    for nd in ch_nodes:
        if nd.state_node.all().count()== size-1:  # select ony those whos state count is one more than curr nodes state count
            a_match=1
            for st_next in nd.state_node.all():     # check whether every state E curr_node in potential next_node
                st_matches=0
                for st_curr in node.state_node.all():
                    if st_curr.id == st_next.id:
                        st_matches=1
                if st_matches== 0:
                    a_match=0
            if a_match ==1:
                fringe_inner.append(nd)
    print(fringe_inner) ###############################################################
    '''kstate= node2kstate(node)
    for padosi in kst.kneighbourhood(kstr, r.set(kstate)):
        num_sett=0
        for sett in padosi:
            num_sett= num_sett+ 1
        if num_sett < size:
            fringe_inner.append(kstate_to_node(padosi))
    '''
    return fringe_inner

def kstate_to_node(kstate): # set(db state) -> db node
    nodes_of_chapter= Node.objects.all()
    size_of_set= r.length(kstate)[0]
    match=1
    for nd in nodes_of_chapter:
        if nd.state_node.all().count()== size_of_set:
            for state in nd.state_node.all():
                if state.id not in kstate:
                    match=0
        if match == 1:
            return nd

def surplus_state(source_node, dest_node):  # db_node1, db_node2 -> db_state(in dest_node which is not present in source_node)
    sm= node2kstate(source_node)
    lg= node2kstate(dest_node)
    print("am in %s.. going to %s"%(str(source_node), str(dest_node))) #**************************************************
    for kitem in r.set_symdiff(sm,lg):
        return int(kitem[0])

def domain_kstate(kstr): # takes a knowledge structure as i/p and returns its domain kstate(final node)
    return kstate_to_node(kst.kdomain(kstr))

def atom(kstr, st):     #takes a k struct and an item(state) and gives its atom
    return kstate_to_node(kst.katoms(kstr, r.set(st.id)))
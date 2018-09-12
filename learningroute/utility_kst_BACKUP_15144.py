from states.models import Node, State
from chapters.models import Chapter, Topic

def outer_fringe(node):  # gives outer fringe in consumable format
    
    ch= Chapter.objects.get(topic__state=node.state_node.all()[0])
    size= node.state_node.all().count()
    
    fringe_outer= list()
    ch_nodes= Node.objects.filter(state_node__topic__chapter=ch).distinct()  # take all nodes E chapter
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

    return fringe_outer



<<<<<<< HEAD
=======
def outer_fringe_id(chap, node):  # gives outer fringe in consumable format
    size= node.state_node.all().count()
    
    
    fringe_outer= list()
    ch_nodes= Node.objects.filter(state_node__topic__chapter__title=chap).distinct()  # take all nodes E chapter
    for nd in ch_nodes:
      
        if nd.state_node.all().count()== size+1:  # select ony those whos state count is one more than curr nodes state count
            a_match=1
            for st_curr in node.state_node.all(): 
                # check whether every state E curr_node in potential next_node
                st_matches=0
                for st_next in nd.state_node.all():
                
                    if st_curr.id == st_next.id:
                       
                        st_matches=1
                if st_matches== 0:
                    a_match=0
            if a_match ==1:
                fringe_outer.append(nd.id)

    
    return fringe_outer
>>>>>>> 24b149fa29a618b0ec90b0d56d2494b2908b6bbc



def inner_fringe(node):  #gives the inner fringe in a consumable format
    ch= Chapter.objects.get(topic__state=node.state_node.all()[0])
    size= node.state_node.all().count()
    
    fringe_inner= list()
<<<<<<< HEAD
    ch_nodes= Node.objects.filter(state_node__topic__chapter=ch).distinct()  # take all nodes E chapter
=======
    ch_nodes= Node.objects.filter(state_node__topic__chapter__title=chap).distinct()
      # take all nodes E chapter
>>>>>>> 24b149fa29a618b0ec90b0d56d2494b2908b6bbc
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
<<<<<<< HEAD
    print(fringe_inner) #********************************************************
=======
    ###############################################################
   
    return fringe_inner


def inner_fringe_id(chap, node):  #gives the inner fringe in a consumable format
    r.sets_options('quote', False)
    print("node is "+str(node)) #################################################
    size= node.state_node.all().count()
    fringe_inner= list()
    ch_nodes= Node.objects.filter(state_node__topic__chapter__title=chap).distinct()
      # take all nodes E chapter
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
                fringe_inner.append(nd.id)
    ###############################################################
   
>>>>>>> 24b149fa29a618b0ec90b0d56d2494b2908b6bbc
    return fringe_inner





# takes 2 nodes which are adjuscent to each other. returns the state which is extra is the larger node.

def surplus_state(source_node, dest_node):  
    sl= source_node.state_node.all().count()
    dl= dest_node.state_node.all().count()
    (smaller, larger)= (source_node, dest_node) if sl<dl else (dest_node, source_node)
    print("am in %s.. going to %s"%(str(source_node), str(dest_node))) #**************************************************
    for lg_st in larger.state_node.all():          
        matched=0
        for sm_st in smaller.state_node.all():   # matching each state of larger node with all states of smaller one. The state which doesnt matches is the result
            if sm_st.id == lg_st.id:
                matched=1
        if matched == 0:
            return lg_st



def domain_kstate(chapter,  standard=11): # takes a chapter and returns the domain node and domain node length both 
    nodes= Node.objects.filter(state_node__topic__chapter=chapter)
    largest_node=None
    node_len=0
    for node in nodes:
        curr_len= node.state_node.all().count()
        if curr_len > node_len:
            node_len= curr_len
            largest_node= node
    return (largest_node, node_len)



<<<<<<< HEAD

def outer_fringe_states(node):   # gives a list of states from current node to go forward to
    fringe= outer_fringe(node)
    state_list= []
    for nd in fringe:
        state_list.append(node, nd)
    
    return state_list


def inner_fringe_states(node): # gives a list of states from current node to go backward to
    fringe= inner_fringe(node)
    state_list= []
    for nd in fringe:
        state_list.append(surplus_state(node, nd))
    
    return state_list
=======
def atom(kstr, st):     #takes a k struct and an item(state) and gives its atom
    return kstate_to_node(kst.katoms(kstr, r.set(st.id)))







>>>>>>> 24b149fa29a618b0ec90b0d56d2494b2908b6bbc

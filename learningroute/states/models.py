from django.db import models
from django.db.models.signals import pre_save,post_save
from chapters.models import Topic
import string
import random


# score_of_i tells the score of illustrations needed to complete illustrations for a particular state

class State(models.Model):
    title = models.CharField(max_length = 120, blank = False, null = False)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    rate  = models.IntegerField(default=2, help_text='Difficulty of the state')
    time  = models.IntegerField(default=0, help_text='approx time needed to solve this state fully')
    tag   = models.CharField( max_length = 15, blank = True, null = True  )



    def __str__(self):
        return str(self.title)

    def score_of_i(self):
        rate = self.rate
        if rate == 1:
            return 2
        if rate == 2:
            return 2
        if rate == 3:
            return 4
        if rate == 4:
            return 5
        else:
            return 7

    def score_of_q(self):
        rate = self.rate
        if rate == 1:
            return 3
        if rate == 2:
            return 6
        if rate == 3:
            return 9
        if rate == 4:
            return 11
        else:
            return 14



class Node(models.Model):
    state_node  = models.ManyToManyField(State)
    description = models.TextField(blank = True)
    credit      = models.IntegerField(default = 0)

    def __str__(self):
        return ",".join(p.title for p in self.state_node.all())


class Edge(models.Model):
    first  = models.ForeignKey(Node, on_delete = models.CASCADE, related_name = 'first_node')
    second = models.ForeignKey(Node, on_delete = models.CASCADE, related_name = 'second_node')
    weight = models.IntegerField(default = 0)
    time   = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.first) + '  ' + str(self.second)



def id_generator(state_number, size=6, chars=string.ascii_uppercase + string.digits):
    state_number = str(state_number)
    return state_number + '-' + ''.join(random.choice(chars) for _ in range(size))

def rl_pre_save_receiver(sender,instance, *args, **kwargs):
        state_number = int(State.objects.filter(topic__title__iexact = instance.topic).count()) + 1
        if not instance.tag:
            instance.tag = id_generator(state_number)

pre_save.connect(rl_pre_save_receiver, sender= State)

from django.db import models
from django.db.models.signals import pre_save,post_save
import string
import random


class State(models.Model):
    title = models.CharField(max_length = 120, blank = False, null = False)
    topic = models.CharField(max_length = 222)
    rate  = models.IntegerField()
    time  = models.IntegerField()
    tag   = models.CharField( max_length = 15, blank = True, null = True  )


    def __str__(self):
        return self.title + ' - for the topic - ' + self.topic


class Node(models.Model):
    state_node  = models.ManyToManyField(State)
    description = models.TextField(blank = True)
    credit      = models.IntegerField(default = 0)

    def __str__(self):
        return ",".join(p.tag for p in self.state_node.all())


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
        state_number = int(State.objects.filter(topic__iexact = instance.topic).count()) + 1
        if not instance.tag:
            instance.tag = id_generator(state_number)

pre_save.connect(rl_pre_save_receiver, sender= State)

from django.db import models
from states.models import State


class Content(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False, null=False)
    text = models.TextField()
    rate = models.IntegerField()
    time = models.IntegerField()
    tag = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return  str(self.title) + ' - for the state - ' + str(self.state)
